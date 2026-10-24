"""Journey task: observe the live host and grade an exact report.

The reference solution walks the published account and reads the clock.
The grader accepts that report only when every check holds.
"""

from __future__ import annotations

import json
from pathlib import Path

from gradia_range.universe import Universe

_ACCOUNT = "ada@example.test"
_PASSWORD = "ada-pass"
_ACTIVITY = "review"
_KEYS = ("t", "kind", "email", "ok", "name")
_STREAM = frozenset({"signup", "login", "login_failed", "activity"})


def observe(seed: int = 1) -> dict:
    """Boot the host, record one review, and return the report that matches."""
    universe = Universe(seed)
    universe.boot()
    opened = universe.login(_ACCOUNT, _PASSWORD)
    if not opened.get("ok"):
        raise RuntimeError("published account did not open")
    done = universe.activity(opened["token"], _ACTIVITY)
    if not done.get("ok"):
        raise RuntimeError("review was not recorded")
    journey = [_row(event) for event in universe.operator_view() if event.get("kind") in _STREAM]
    return {
        "assessment": "complete",
        "journey": journey,
        "findings": _bursts(journey),
    }


def grade(report: object, seed: int = 1) -> dict:
    """Score the report. Reward is 1 only when every required check is 1."""
    expected = observe(seed)
    journey = report.get("journey") if isinstance(report, dict) else None
    findings = report.get("findings") if isinstance(report, dict) else None
    assessment = report.get("assessment") if isinstance(report, dict) else None
    scores = {
        "journey": 1 if journey == expected["journey"] else 0,
        "burst": 1 if findings == expected["findings"] else 0,
        "review": 1 if _review_holds(journey) else 0,
        "assessment": 1 if assessment == "complete" else 0,
    }
    scores["reward"] = 1 if all(scores.values()) else 0
    return scores


def write_report(path: Path, seed: int = 1) -> dict:
    """Reference solution. Writes the observed report and returns the grade."""
    body = observe(seed)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return grade(body, seed)


def _review_holds(journey: object) -> bool:
    if not isinstance(journey, list):
        return False
    matches = [
        row
        for row in journey
        if isinstance(row, dict)
        and row.get("kind") == "activity"
        and row.get("email") == _ACCOUNT
        and row.get("name") == _ACTIVITY
        and row.get("ok") is True
    ]
    return len(matches) == 1


def _bursts(journey: list[dict]) -> list[dict]:
    times: dict[str, list[int]] = {}
    for row in journey:
        if row.get("kind") != "login_failed":
            continue
        email = row.get("email")
        if not isinstance(email, str) or not email:
            continue
        times.setdefault(email, []).append(int(row["t"]))
    findings = []
    for email in sorted(times):
        hits = times[email]
        if len(hits) != 3:
            continue
        findings.append(
            {
                "id": "login-burst",
                "email": email,
                "severity": "high",
                "times": hits,
            }
        )
    return findings


def _row(event: dict) -> dict:
    return {key: event.get(key) for key in _KEYS}
