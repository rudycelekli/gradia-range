"""Validate a Gradia Range assessment report.

Harbor copies this file into a task's tests/ directory. It stays free of
package imports so that copy still runs.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SEVERITIES = {"critical", "high", "medium", "low", "info"}


def evaluate(
    report_path: Path,
    root: Path,
    revision: str,
    scope: list[str],
    prefixes: list[str],
    patch_path: Path,
    reward_dir: Path | None,
) -> dict[str, int]:
    scores = {"objective": 0, "report": 0, "schema": 0, "evidence": 0, "fix": 0, "reward": 0}
    root = root.resolve()
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        _write(reward_dir, scores)
        return scores

    if _schema_ok(report, revision, scope):
        scores["schema"] = 1
    if scores["schema"] and _evidence_ok(report, root, prefixes):
        scores["evidence"] = 1
    if _fix_ok(root, patch_path):
        scores["fix"] = 1
    if scores["schema"] and scores["evidence"] and scores["fix"]:
        scores["report"] = 1
        scores["reward"] = 1
    _write(reward_dir, scores)
    return scores


def _schema_ok(report: object, revision: str, scope: list[str]) -> bool:
    if not isinstance(report, dict):
        return False
    if report.get("revision") != revision:
        return False
    if report.get("assessment") != "complete":
        return False
    got = report.get("scope")
    if not isinstance(got, list) or {str(item) for item in got} != set(scope):
        return False
    findings = report.get("findings")
    if not isinstance(findings, list):
        return False
    seen: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            return False
        fid = finding.get("id")
        if not isinstance(fid, str) or not fid or fid in seen:
            return False
        seen.add(fid)
        if finding.get("component") not in scope:
            return False
        if finding.get("severity") not in SEVERITIES:
            return False
        if not _nonempty(finding.get("title")) or not _nonempty(finding.get("summary")):
            return False
        evidence = finding.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            return False
        for item in evidence:
            if not isinstance(item, dict):
                return False
            if not isinstance(item.get("path"), str) or not item["path"]:
                return False
            line = item.get("line")
            if not isinstance(line, int) or isinstance(line, bool) or line < 1:
                return False
            if not isinstance(item.get("note"), str):
                return False
    return True


def _evidence_ok(report: dict, root: Path, prefixes: list[str]) -> bool:
    for finding in report["findings"]:
        for item in finding["evidence"]:
            if not _path_in_scope(root, item["path"], prefixes):
                return False
    return True


def _path_in_scope(root: Path, rel: str, prefixes: list[str]) -> bool:
    raw = Path(rel)
    if raw.is_absolute() or ".." in raw.parts:
        return False
    path = (root / raw).resolve()
    if not path.is_file() or not path.is_relative_to(root):
        return False
    relative = path.relative_to(root).as_posix()
    if prefixes == ["."]:
        return True
    return any(relative == prefix or relative.startswith(prefix.rstrip("/") + "/") for prefix in prefixes)


def _fix_ok(root: Path, patch_path: Path) -> bool:
    if not patch_path.exists():
        return True
    if patch_path.stat().st_size == 0:
        return False
    proc = subprocess.run(
        ["git", "apply", "--check", str(patch_path)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _write(reward_dir: Path | None, scores: dict[str, int]) -> None:
    if reward_dir is None:
        return
    reward_dir.mkdir(parents=True, exist_ok=True)
    (reward_dir / "reward.txt").write_text(f"{scores['reward']}\n", encoding="utf-8")
    (reward_dir / "reward.json").write_text(json.dumps(scores) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score a Gradia Range report")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--scope", required=True, help="Comma-separated module ids")
    parser.add_argument("--prefixes", required=True, help="Comma-separated path prefixes, or .")
    parser.add_argument("--patch", type=Path, default=Path("/workspace/fix.patch"))
    parser.add_argument("--reward-dir", type=Path, default=None)
    args = parser.parse_args(argv)
    scope = [part for part in args.scope.split(",") if part]
    prefixes = [part for part in args.prefixes.split(",") if part]
    scores = evaluate(
        args.report,
        args.root,
        args.revision,
        scope,
        prefixes,
        args.patch,
        args.reward_dir,
    )
    return 0 if scores["reward"] == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
