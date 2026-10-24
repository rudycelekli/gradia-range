"""Engine-emitted journey task: the oracle scores 1 and a miss scores 0."""

import json
import os
import subprocess
import sys
from pathlib import Path

from gradia_range.emit_journey import emit_journey
from gradia_range.journey import grade, observe, write_report

_HIDDEN = ("synthetic", "generated", "population", "seed", "mara@")


def test_reference_report_scores_one(tmp_path: Path) -> None:
    body = observe()
    assert grade(body)["reward"] == 1
    assert body["findings"]
    assert len(body["journey"]) > 20
    scores = write_report(tmp_path / "report.json")
    assert scores["reward"] == 1
    assert scores["journey"] == 1
    assert scores["burst"] == 1
    assert scores["review"] == 1


def test_a_missing_row_scores_zero(tmp_path: Path) -> None:
    path = tmp_path / "report.json"
    write_report(path)
    body = json.loads(path.read_text(encoding="utf-8"))
    body["journey"].pop()
    scores = grade(body)
    assert scores["reward"] == 0
    assert scores["journey"] == 0


def test_a_wrong_finding_scores_zero() -> None:
    body = observe()
    body["findings"][0]["email"] = "ada@example.test"
    assert grade(body)["reward"] == 0


def test_emitted_oracle_passes_and_instruction_hides_the_address(tmp_path: Path) -> None:
    task = emit_journey(tmp_path)
    instruction = (task / "instruction.md").read_text(encoding="utf-8").lower()
    for word in _HIDDEN:
        assert word not in instruction
    toml = (task / "task.toml").read_text(encoding="utf-8")
    assert 'schema_version = "1.4"' in toml
    assert 'difficulty = "hard"' in toml
    app = task / "environment" / "app"
    assert not (app / "universe.py").exists()
    state = (app / "state.json").read_text(encoding="utf-8").lower()
    for word in ("seed", "synthetic", "generated", "population", "ada-pass"):
        assert word not in state
    report = tmp_path / "report.json"
    logs = tmp_path / "logs"
    logs.mkdir()
    env = os.environ.copy()
    env["RANGE_APP"] = str(task / "environment" / "app")
    env["RANGE_REPORT"] = str(report)
    env["RANGE_STATE"] = str(tmp_path / "state.json")
    env["RANGE_PYTHON"] = sys.executable
    solved = subprocess.run(
        ["bash", str(task / "solution" / "solve.sh")],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert solved.returncode == 0, solved.stderr
    env["RANGE_TESTS"] = str(task / "tests")
    env["PYTHONPATH"] = str(task / "tests")
    graded = subprocess.run(
        [
            sys.executable,
            str(task / "tests" / "grade_journey.py"),
            str(report),
            str(logs / "reward.json"),
            str(logs / "reward.txt"),
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert graded.returncode == 0, graded.stderr
    assert (logs / "reward.txt").read_text(encoding="utf-8").strip() == "1"
    scores = json.loads((logs / "reward.json").read_text(encoding="utf-8"))
    assert scores == {"journey": 1, "burst": 1, "review": 1, "assessment": 1, "reward": 1}

    broken = json.loads(report.read_text(encoding="utf-8"))
    broken["journey"] = broken["journey"][:-1]
    report.write_text(json.dumps(broken), encoding="utf-8")
    graded_miss = subprocess.run(
        [
            sys.executable,
            str(task / "tests" / "grade_journey.py"),
            str(report),
            str(logs / "reward.json"),
            str(logs / "reward.txt"),
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert graded_miss.returncode == 0, graded_miss.stderr
    assert (logs / "reward.txt").read_text(encoding="utf-8").strip() == "0"
    _watch_oracle(tmp_path, task.parent / "watch")


def _watch_oracle(tmp_path: Path, task: Path) -> None:
    instruction = (task / "instruction.md").read_text(encoding="utf-8").lower()
    for word in _HIDDEN:
        assert word not in instruction
    assert not (task / "environment" / "app" / "universe.py").exists()
    report = tmp_path / "handoff.json"
    logs = tmp_path / "watch-logs"
    logs.mkdir()
    env = os.environ.copy()
    env["RANGE_APP"] = str(task / "environment" / "app")
    env["RANGE_REPORT"] = str(report)
    env["RANGE_STATE"] = str(tmp_path / "watch-state.json")
    env["RANGE_PYTHON"] = sys.executable
    env["RANGE_TESTS"] = str(task / "tests")
    env["PYTHONPATH"] = str(task / "tests")
    solved = subprocess.run(
        ["bash", str(task / "solution" / "solve.sh")],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert solved.returncode == 0, solved.stderr
    graded = subprocess.run(
        [sys.executable, str(task / "tests" / "grade_watch.py"), str(report), str(logs / "reward.json"), str(logs / "reward.txt")],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert graded.returncode == 0, graded.stderr
    assert (logs / "reward.txt").read_text(encoding="utf-8").strip() == "1"
    late = json.loads(report.read_text(encoding="utf-8"))
    late[0]["t"] = late[0]["t"] + 1
    report.write_text(json.dumps(late), encoding="utf-8")
    graded_miss = subprocess.run(
        [sys.executable, str(task / "tests" / "grade_watch.py"), str(report), str(logs / "reward.json"), str(logs / "reward.txt")],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert graded_miss.returncode == 0, graded_miss.stderr
    assert (logs / "reward.txt").read_text(encoding="utf-8").strip() == "0"
