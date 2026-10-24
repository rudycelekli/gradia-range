"""Comparable scorecard.

Pass@1 uses graded trials only. Pass@5 uses tasks with exactly five graded
trials. A slice comparison keeps only tasks every model in the panel graded.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def compare(trials: list[dict]) -> dict:
    graded = [trial for trial in trials if trial.get("graded")]
    models = sorted({trial["model"] for trial in graded})
    by_task: dict[str, set[str]] = defaultdict(set)
    for trial in graded:
        by_task[trial["task"]].add(trial["model"])
    shared = sorted(task for task, seen in by_task.items() if models and seen >= set(models))
    shared_trials = [trial for trial in graded if trial["task"] in set(shared)]
    rows = [_model_row(model, shared_trials) for model in models]
    slices = _slices(models, shared_trials)
    return {
        "models": models,
        "shared_tasks": shared,
        "graded_trials": len(shared_trials),
        "infra_trials": sum(1 for trial in trials if not trial.get("graded")),
        "models_detail": rows,
        "slices": slices,
    }


def render(card: dict) -> str:
    lines = [
        "# Range scorecard",
        "",
        f"- Models: {len(card['models'])}",
        f"- Shared tasks: {len(card['shared_tasks'])}",
        f"- Graded trials on those tasks: {card['graded_trials']}",
        f"- Infrastructure trials excluded: {card['infra_trials']}",
        "",
        "Pass@1 divides passes by graded trials. Pass@5 includes a task only when that model has exactly five graded trials on it, and counts the task passed when any of those trials passed.",
        "",
    ]
    if len(card["models"]) < 2:
        lines.append("A strength and a weakness need two models on the same tasks. This panel has one.")
        lines.append("")
    if card["models_detail"]:
        lines.extend(
            [
                "| Model | Role | Graded | Pass@1 | Pass@5 | Last-mile |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in card["models_detail"]:
            lines.append(
                f"| {row['model']} | {row['role']} | {row['graded']} | {_pct(row['pass_at_1'])} | {_pct(row['pass_at_5'])} | {_pct(row['last_mile'])} |"
            )
        lines.append("")
    if card["slices"]:
        lines.extend(["| Model | Slice | Pass@1 | Peer mean | Gap |", "| --- | --- | ---: | ---: | ---: |"])
        for row in card["slices"]:
            lines.append(
                f"| {row['model']} | {row['slice']} | {_pct(row['pass_at_1'])} | {_pct(row['peer_mean'])} | {_pts(row['gap'])} |"
            )
        lines.append("")
        weak = [row for row in card["slices"] if row["gap"] < 0]
        strong = [row for row in card["slices"] if row["gap"] > 0]
        if weak:
            worst = min(weak, key=lambda row: row["gap"])
            lines.append(
                f"Weakest slice: {worst['model']} on `{worst['slice']}`, {_pts(worst['gap'])} against the other models. The next task batch is cut on that slice."
            )
        if strong:
            best = max(strong, key=lambda row: row["gap"])
            lines.append(
                f"Strongest slice: {best['model']} on `{best['slice']}`, {_pts(best['gap'])} against the other models."
            )
        lines.append("")
    return "\n".join(lines)


def load_trials(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("trials", [])
    return list(payload)


def _model_row(model: str, trials: list[dict]) -> dict:
    own = [trial for trial in trials if trial["model"] == model]
    passed = [trial for trial in own if trial.get("passed")]
    roles = sorted({trial.get("role", "solver") for trial in own})
    return {
        "model": model,
        "role": ",".join(roles),
        "graded": len(own),
        "passes": len(passed),
        "pass_at_1": _ratio(len(passed), len(own)),
        "pass_at_5": _pass_at_5(own),
        "last_mile": _last_mile(own),
    }


def _pass_at_5(trials: list[dict]) -> float | None:
    by_task: dict[str, list[dict]] = defaultdict(list)
    for trial in trials:
        by_task[trial["task"]].append(trial)
    eligible = [group for group in by_task.values() if len(group) == 5]
    if not eligible:
        return None
    solved = sum(1 for group in eligible if any(trial.get("passed") for trial in group))
    return solved / len(eligible)


def _last_mile(trials: list[dict]) -> float | None:
    failed = [
        trial
        for trial in trials
        if not trial.get("passed") and trial.get("checks_total")
    ]
    if not failed:
        return None
    close = sum(1 for trial in failed if trial["checks_passed"] / trial["checks_total"] >= 0.9)
    return close / len(failed)


def _slices(models: list[str], trials: list[dict]) -> list[dict]:
    if len(models) < 2:
        return []
    rows = []
    tags = sorted({tag for trial in trials for tag in _tags(trial)})
    for tag in tags:
        rates = {}
        for model in models:
            own = [trial for trial in trials if trial["model"] == model and tag in _tags(trial)]
            if not own:
                continue
            rates[model] = _ratio(sum(1 for trial in own if trial.get("passed")), len(own))
        for model, rate in rates.items():
            others = [value for name, value in rates.items() if name != model]
            if not others:
                continue
            peer = sum(others) / len(others)
            rows.append(
                {
                    "model": model,
                    "slice": tag,
                    "pass_at_1": rate,
                    "peer_mean": peer,
                    "gap": rate - peer,
                }
            )
    rows.sort(key=lambda row: (row["model"], row["gap"]))
    return rows


def _tags(trial: dict) -> list[str]:
    tags = trial.get("tags")
    if isinstance(tags, list) and tags:
        return [str(tag) for tag in tags]
    role = trial.get("role", "solver")
    return [str(role)]


def _ratio(part: int, whole: int) -> float | None:
    if whole == 0:
        return None
    return part / whole


def _pct(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value * 100:.1f}%"


def _pts(value: float) -> str:
    points = value * 100
    sign = "+" if points > 0 else ""
    return f"{sign}{points:.1f} pts"
