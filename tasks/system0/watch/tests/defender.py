"""Operator swarm tick. One pass, five members, handoffs on the same clock."""

from __future__ import annotations

from universe import Universe

_STREAM = frozenset({"signup", "login", "login_failed", "activity"})
_CHAIN = (
    ("watch", "sense"),
    ("sense", "confirm"),
    ("confirm", "close"),
    ("close", "tell"),
)


def tick(universe: Universe, window: int = 5) -> list[dict]:
    """One defender pass. Members in order: watch, sense, confirm, close, tell.

    Sense reads operator_view events of kind signup, login, login_failed, activity.
    Three login_failed events for one email are a login_burst gap. A held
    objective is an objective gap. Each gap yields watch->sense, sense->confirm,
    confirm->close, close->tell.

    clear() runs when the objective is held and the latest event t is at most
    `window` after the objective event t. A login_burst gap leaves that flag
    as it is. Handoffs are returned for the caller to record. Objective t
    comes from events() of kind objective. Handoff t is that latest t, or 0.
    """
    noted = watch(universe)
    burst = sense(universe)
    gaps = confirm(noted["held"], burst)
    close(universe, gaps, noted["objective_t"], noted["t"], window)
    return tell(noted["t"], gaps)


def watch(universe: Universe) -> dict:
    """Read the audit clock: held flag, objective t, and the latest event t."""
    log = universe.events()
    objective_t: int | None = None
    for event in log:
        if event.get("kind") == "objective":
            objective_t = int(event["t"])
    clock = int(log[-1]["t"]) if log else 0
    return {"held": bool(universe.objective_held()), "objective_t": objective_t, "t": clock}


def sense(universe: Universe) -> bool:
    """True when one email has three failed logins on the product stream."""
    counts: dict[str, int] = {}
    for event in universe.operator_view():
        if event.get("kind") not in _STREAM:
            continue
        if event.get("kind") != "login_failed":
            continue
        email = event.get("email")
        if not isinstance(email, str) or not email:
            continue
        counts[email] = counts.get(email, 0) + 1
    return any(count >= 3 for count in counts.values())


def confirm(held: bool, burst: bool) -> list[str]:
    """Gaps present on this pass, burst first, then a held objective."""
    gaps: list[str] = []
    if burst:
        gaps.append("login_burst")
    if held:
        gaps.append("objective")
    return gaps


def close(
    universe: Universe,
    gaps: list[str],
    objective_t: int | None,
    clock: int,
    window: int,
) -> None:
    """Clear a held objective still inside the window. A burst alone does not."""
    if "objective" not in gaps or objective_t is None:
        return
    if clock - objective_t > window:
        return
    universe.clear()


def tell(clock: int, gaps: list[str]) -> list[dict]:
    """Four handoffs per gap, stamped with the clock from watch."""
    handoffs: list[dict] = []
    for gap in gaps:
        for frm, to in _CHAIN:
            handoffs.append(
                {
                    "t": clock,
                    "kind": "handoff",
                    "seat": "operator",
                    "frm": frm,
                    "to": to,
                    "gap": gap,
                }
            )
    return handoffs
