"""Watch task: the operator handoff chain after the review is on the clock."""

from __future__ import annotations

import json
from pathlib import Path

from gradia_range.defender import tick
from gradia_range.universe import Universe

_ACCOUNT = "ada@example.test"
_PASSWORD = "ada-pass"
_ACTIVITY = "review"


def expected(seed: int = 1) -> list[dict]:
    """Handoffs for the sign-in burst after the published review."""
    universe = Universe(seed)
    universe.boot()
    opened = universe.login(_ACCOUNT, _PASSWORD)
    if not opened.get("ok"):
        raise RuntimeError("published account did not open")
    done = universe.activity(opened["token"], _ACTIVITY)
    if not done.get("ok"):
        raise RuntimeError("review was not recorded")
    return [dict(row) for row in tick(universe) if row.get("gap") == "login_burst"]


def grade(report: object, seed: int = 1) -> dict:
    """Reward is 1 only when the handoff list matches the host."""
    match = 1 if report == expected(seed) else 0
    return {"reward": match, "handoff": match}


def write_report(path: Path, seed: int = 1) -> dict:
    """Reference solution."""
    body = expected(seed)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return grade(body, seed)
