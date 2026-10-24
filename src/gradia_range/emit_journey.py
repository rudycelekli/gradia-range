"""Write the System 0 journey as a Harbor task the engine can emit."""

from __future__ import annotations

import json
import stat
from hashlib import sha256
from pathlib import Path

from gradia_range.emit_journey_text import (
    CLIENT,
    DOCKERFILE,
    GRADER,
    INSTRUCTION,
    SOLVE,
    TASK_TOML,
    TEST,
    WATCH_GRADER,
    WATCH_INSTRUCTION,
    WATCH_SOLVE,
    WATCH_TEST,
    WATCH_TOML,
)


def emit_journey(root: Path) -> Path:
    """Write tasks/system0/journey and return that directory."""
    task = Path(root) / "tasks" / "system0" / "journey"
    app = task / "environment" / "app"
    tests = task / "tests"
    app.mkdir(parents=True, exist_ok=True)
    (task / "solution").mkdir(parents=True, exist_ok=True)
    tests.mkdir(parents=True, exist_ok=True)
    (task / "instruction.md").write_text(INSTRUCTION, encoding="utf-8")
    (task / "task.toml").write_text(TASK_TOML, encoding="utf-8")
    (task / "environment" / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    source = Path(__file__).resolve().parent
    _copy_module(source / "universe.py", tests / "universe.py")
    _copy_module(source / "journey.py", tests / "journey.py")
    (app / "client.py").write_text(CLIENT, encoding="utf-8")
    _write_state(app / "state.json")
    _script(task / "solution" / "solve.sh", SOLVE)
    _script(tests / "test.sh", TEST)
    (tests / "grade_journey.py").write_text(GRADER, encoding="utf-8")
    _emit_watch(task.parent, source)
    index = {
        "slug": "system0",
        "tasks": ["journey", "watch"],
        "difficulty": "hard",
        "reward": "1 only when every required check matches the host",
    }
    (task.parent / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return task


def _emit_watch(parent: Path, source: Path) -> Path:
    task = parent / "watch"
    app = task / "environment" / "app"
    tests = task / "tests"
    app.mkdir(parents=True, exist_ok=True)
    (task / "solution").mkdir(parents=True, exist_ok=True)
    tests.mkdir(parents=True, exist_ok=True)
    (task / "instruction.md").write_text(WATCH_INSTRUCTION, encoding="utf-8")
    (task / "task.toml").write_text(WATCH_TOML, encoding="utf-8")
    (task / "environment" / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    (app / "client.py").write_text(CLIENT, encoding="utf-8")
    _write_state(app / "state.json")
    for name in ("universe.py", "defender.py", "handoff.py"):
        _copy_module(source / name, tests / name)
    _script(task / "solution" / "solve.sh", WATCH_SOLVE)
    _script(tests / "test.sh", WATCH_TEST)
    (tests / "grade_watch.py").write_text(WATCH_GRADER, encoding="utf-8")
    return task


def _copy_module(source: Path, dest: Path) -> None:
    text = source.read_text(encoding="utf-8")
    text = text.replace("from gradia_range.", "from ")
    dest.write_text(text, encoding="utf-8")


def _write_state(path: Path) -> None:
    """Boot the host and store a seat-facing snapshot. No account generator."""
    from gradia_range.universe import Universe

    host = Universe(1)
    host.boot()
    raw = host.dump()
    body = {
        "series": raw["seed"],
        "clock": raw["clock"],
        "events": raw["events"],
        "password": {
            email: sha256(password.encode()).hexdigest() for email, password in raw["password"].items()
        },
        "session": {},
        "minted": raw["minted"],
    }
    path.write_text(json.dumps(body), encoding="utf-8")


def _script(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
