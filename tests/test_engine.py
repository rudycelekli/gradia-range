"""System 0 episode: published account, verifier hook, and both rewards."""

import json
from pathlib import Path

from gradia_range.episode import run

_HIDDEN = ("synthetic", "generated", "population", "seed")
_MEMBERS = ("watch", "sense", "confirm", "close", "tell")


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def test_boot_walks_signup_login_activity(tmp_path: Path) -> None:
    result = run(tmp_path, oracle=False)
    kinds = {row["kind"] for row in _rows(result["trace"])}
    assert {"signup", "login", "activity", "login_failed"} <= kinds


def test_views_hide_generation(tmp_path: Path) -> None:
    run(tmp_path, oracle=False)
    seat = tmp_path / "runs" / "system0"
    for name in ("product-view.json", "operator-view.json"):
        text = (seat / name).read_text(encoding="utf-8").lower()
        for word in _HIDDEN:
            assert word not in text


def test_oracle_clears_inside_window(tmp_path: Path) -> None:
    result = run(tmp_path, oracle=True)
    assert result["product_reward"] == 1
    assert result["operator_reward"] == 1
    handoffs = [row for row in _rows(result["trace"]) if row.get("kind") == "handoff"]
    assert handoffs
    named = {row["frm"] for row in handoffs} | {row["to"] for row in handoffs}
    assert set(_MEMBERS) <= named


def test_operator_ungraded_without_entry(tmp_path: Path) -> None:
    result = run(tmp_path, oracle=False)
    body = json.loads((tmp_path / "runs" / "system0" / "reward-operator.json").read_text(encoding="utf-8"))
    assert result["operator_graded"] is False
    assert result["operator_reward"] is None
    assert body["graded"] is False
    assert body["blocked_in_time"] is None
