"""Run one System 0 episode and write both seat rewards."""

from __future__ import annotations

import json
from pathlib import Path

from gradia_range.defender import tick
from gradia_range.universe import Universe

_ACCOUNT = "ada@example.test"
_PASSWORD = "ada-pass"
_ACTIVITY = "review"


def run(root: Path, seed: int = 1, oracle: bool = False, window: int = 5) -> dict:
    """Boot the host, walk the published account, and grade both seats.

    When oracle is true, the verifier records that the objective held.
    That call is a grade hook. The product seat still uses only the published account.
    """
    universe = Universe(seed)
    universe.boot()
    _walk_product(universe)
    if oracle:
        universe.reach()
    handoffs = list(tick(universe, window))
    events = list(universe.events())
    product_reward = 1 if _has(events, "objective") else 0
    operator_reward = _blocked(events, window)
    trace = _store(Path(root), universe, events, handoffs, product_reward, operator_reward, window)
    return {
        "trace": trace,
        "product_reward": product_reward,
        "operator_graded": operator_reward is not None,
        "operator_reward": operator_reward,
        "events": len(events) + len(handoffs),
    }


def _walk_product(universe: Universe) -> None:
    opened = universe.login(_ACCOUNT, _PASSWORD)
    universe.activity(opened["token"], _ACTIVITY)


def _has(events: list[dict], kind: str) -> bool:
    return any(event.get("kind") == kind for event in events)


def _blocked(events: list[dict], window: int) -> int | None:
    objective_t = next((event["t"] for event in events if event.get("kind") == "objective"), None)
    if objective_t is None:
        return None
    cleared_t = next(
        (
            event["t"]
            for event in events
            if event.get("kind") == "cleared" and event["t"] >= objective_t
        ),
        None,
    )
    if cleared_t is None:
        return 0
    return 1 if cleared_t - objective_t <= window else 0


def _operator_body(reward: int | None, window: int) -> dict:
    if reward is None:
        return {"reward": None, "blocked_in_time": None, "role": "operator", "graded": False}
    return {
        "reward": reward,
        "blocked_in_time": reward,
        "role": "operator",
        "block_window": window,
    }


def _store(
    root: Path,
    universe: Universe,
    events: list[dict],
    handoffs: list[dict],
    product_reward: int,
    operator_reward: int | None,
    window: int,
) -> Path:
    dest = root / "runs" / "system0"
    dest.mkdir(parents=True, exist_ok=True)
    trace = dest / "trace.jsonl"
    _jsonl(trace, [*events, *handoffs])
    _json(dest / "product-view.json", list(universe.product_view()))
    _json(dest / "operator-view.json", [*list(universe.operator_view()), *handoffs])
    _json(
        dest / "reward-product.json",
        {"reward": product_reward, "objective": product_reward, "role": "product"},
    )
    _json(dest / "reward-operator.json", _operator_body(operator_reward, window))
    return trace


def _json(path: Path, body: object) -> None:
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def _jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
