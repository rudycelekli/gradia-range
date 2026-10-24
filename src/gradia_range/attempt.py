"""Record a house attempt against the report contract."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from gradia_range.check_report import evaluate


def attempt(catalog: dict, root: Path) -> dict:
    slug = catalog["slug"]
    index = json.loads((root / "tasks" / slug / "index.json").read_text(encoding="utf-8"))
    source_root = root / "twins" / slug
    if catalog.get("checkout") != "local":
        source_root.mkdir(parents=True, exist_ok=True)
    out = root / "engagements" / slug
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for task_name in index["tasks"]:
        task = root / "tasks" / slug / task_name
        if (task / "steps").is_dir():
            step_dirs = sorted(path for path in (task / "steps").iterdir() if path.is_dir())
        else:
            step_dirs = [task]
        for step in step_dirs:
            report_path = out / f"{task_name}-{step.name}-report.json"
            _write_oracle(step, report_path)
            scope, prefixes = _from_test(step / "tests" / "test.sh")
            reward_dir = out / "rewards" / task_name / step.name
            scores = evaluate(
                report_path,
                source_root,
                catalog["revision"],
                scope,
                prefixes,
                report_path.parent / "missing-fix.patch",
                reward_dir,
            )
            results.append({"task": task_name, "step": step.name, "scores": scores})
    witness = {
        "slug": slug,
        "revision": catalog["revision"],
        "source": catalog["source"],
        "solver": "house",
        "kind": "human",
        "grant": "open",
        "at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "objective_planted": False,
        "results": results,
        "fix_offered": False,
        "note": "Report contract witnessed. No finding was cited, so no fix is offered on this pass.",
    }
    (out / "attempt.json").write_text(json.dumps(witness, indent=2) + "\n", encoding="utf-8")
    (out / "report.md").write_text(_markdown(witness), encoding="utf-8")
    return witness


def _write_oracle(step: Path, dest: Path) -> None:
    script = (step / "solution" / "solve.sh").read_text(encoding="utf-8")
    start = script.index("<<'EOF'\n") + len("<<'EOF'\n")
    end = script.rindex("\nEOF")
    dest.write_text(script[start:end] + "\n", encoding="utf-8")


def _from_test(path: Path) -> tuple[list[str], list[str]]:
    scope: list[str] = []
    prefixes: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().strip("\\").split()
        if len(parts) >= 2 and parts[0] == "--scope":
            scope = [part for part in parts[1].split(",") if part]
        if len(parts) >= 2 and parts[0] == "--prefixes":
            prefixes = [part for part in parts[1].split(",") if part]
    return scope, prefixes or ["."]


def _markdown(witness: dict) -> str:
    lines = [
        f"# Range report: {witness['slug']}",
        "",
        f"- Revision: `{witness['revision']}`",
        f"- Source: {witness['source']}",
        f"- Solver: house",
        f"- Grant: open",
        f"- When: {witness['at']}",
        "",
        "The report contract was checked for each task step. The whole-twin objective is not planted on this revision, so `objective` is 0. That is a result about this pass.",
        "",
        "| Task | Step | report | objective |",
        "| --- | --- | --- | --- |",
    ]
    for result in witness["results"]:
        scores = result["scores"]
        lines.append(
            f"| {result['task']} | {result['step']} | {scores['report']} | {scores['objective']} |"
        )
    lines.extend(
        [
            "",
            "No finding was cited. A fix is not offered on this pass.",
            "",
            "Traces from this open twin may be used after a fix window. There is no finding to embargo.",
            "",
        ]
    )
    return "\n".join(lines)
