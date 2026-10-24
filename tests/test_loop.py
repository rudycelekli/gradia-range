import json
import subprocess
from pathlib import Path

from gradia_range.adopt import adopt
from gradia_range.attempt import attempt
from gradia_range.card import compare, render
from gradia_range.check_report import evaluate
from gradia_range.emit import emit


def _repo(tmp_path: Path) -> Path:
    src = tmp_path / "src"
    (src / "api").mkdir(parents=True)
    (src / "web").mkdir()
    (src / "api" / "package.json").write_text('{"dependencies": {"@slack/web-api": "1.0.0"}}', encoding="utf-8")
    (src / "web" / "package.json").write_text("{}", encoding="utf-8")
    (src / "api" / "index.js").write_text("export const ok = true\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=src, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=src, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=src, check=True)
    subprocess.run(["git", "add", "."], cwd=src, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=src, check=True)
    return src


def test_loop_on_local_repo(tmp_path: Path) -> None:
    src = _repo(tmp_path)
    root = tmp_path / "work"
    catalog = adopt(str(src), root)
    assert catalog["checkout"] == "local"
    assert any(item["name"] == "slack" for item in catalog["integrations"])
    emit(catalog, root)
    witness = attempt(catalog, root)
    assert witness["fix_offered"] is False
    assert witness["results"]
    assert all(item["scores"]["report"] == 1 for item in witness["results"])
    assert all(item["scores"]["objective"] == 0 for item in witness["results"])
    toml = (root / "tasks" / catalog["slug"] / "joined" / "task.toml").read_text(encoding="utf-8")
    assert 'schema_version = "1.4"' in toml
    assert "[[steps]]" in toml


def test_report_rejects_missing_evidence(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    report = tmp_path / "report.json"
    report.write_text(
        json.dumps(
            {
                "revision": "abc",
                "scope": ["api"],
                "assessment": "complete",
                "findings": [
                    {
                        "id": "F-1",
                        "title": "missing file",
                        "severity": "low",
                        "component": "api",
                        "summary": "cites a path that is not in the tree",
                        "evidence": [{"path": "../secret", "line": 1, "note": "no"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    scores = evaluate(report, root, "abc", ["api"], ["api"], tmp_path / "no.patch", None)
    assert scores["report"] == 0
    assert scores["objective"] == 0


def test_card_names_the_weak_slice_and_the_strong_slice() -> None:
    trials = []
    for index in range(5):
        trials.append({"task": f"db-{index}", "model": "alpha", "role": "solver", "graded": True, "passed": False, "tags": ["database"], "checks_passed": 9, "checks_total": 10})
        trials.append({"task": f"db-{index}", "model": "beta", "role": "solver", "graded": True, "passed": True, "tags": ["database"], "checks_passed": 10, "checks_total": 10})
        trials.append({"task": f"api-{index}", "model": "alpha", "role": "solver", "graded": True, "passed": True, "tags": ["api"]})
        trials.append({"task": f"api-{index}", "model": "beta", "role": "solver", "graded": True, "passed": False, "tags": ["api"]})
    trials.append({"task": "db-0", "model": "alpha", "role": "solver", "graded": False, "passed": False, "tags": ["database"]})
    card = compare(trials)
    assert card["infra_trials"] == 1
    assert card["shared_tasks"]
    text = render(card)
    assert "Weakest slice: alpha on `database`" in text
    assert "Strongest slice: alpha on `api`" in text
    alpha = next(row for row in card["models_detail"] if row["model"] == "alpha")
    assert alpha["pass_at_1"] == 0.5
    assert alpha["last_mile"] == 1.0
