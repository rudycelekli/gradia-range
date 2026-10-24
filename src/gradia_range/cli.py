"""gradia-range command line."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from gradia_range.adopt import adopt
from gradia_range.attempt import attempt
from gradia_range.card import compare, load_trials, render
from gradia_range.emit import emit
from gradia_range.episode import run as run_episode


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="gradia-range")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="cmd", required=True)

    adopt_cmd = sub.add_parser("adopt", help="Pin a repository")
    adopt_cmd.add_argument("source")
    adopt_cmd.add_argument("--refresh", action="store_true")

    emit_cmd = sub.add_parser("emit", help="Write Harbor tasks from a catalog entry")
    emit_cmd.add_argument("slug")

    attempt_cmd = sub.add_parser("attempt", help="Record the house report-contract attempt")
    attempt_cmd.add_argument("slug")

    report_cmd = sub.add_parser("report", help="Write a comparable strength and weakness card")
    report_cmd.add_argument("trials", type=Path)

    engine_cmd = sub.add_parser("engine", help="Boot the System 0 host and write both rewards")
    engine_cmd.add_argument("--seed", type=int, default=1)
    engine_cmd.add_argument("--oracle", action="store_true")
    engine_cmd.add_argument("--window", type=int, default=5)

    sub.add_parser("list", help="List catalog entries")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.cmd == "adopt":
        catalog = adopt(args.source, root, refresh=args.refresh)
        print(
            json.dumps(
                {
                    "slug": catalog["slug"],
                    "revision": catalog["revision"],
                    "modules": len(catalog["modules"]),
                    "checkout": catalog["checkout"],
                },
                indent=2,
            )
        )
        return
    if args.cmd == "emit":
        catalog = _load(root, args.slug)
        paths = emit(catalog, root)
        print("\n".join(str(path) for path in paths))
        return
    if args.cmd == "attempt":
        catalog = _load(root, args.slug)
        witness = attempt(catalog, root)
        reports = [item["scores"]["report"] for item in witness["results"]]
        print(json.dumps({"steps": len(reports), "report": min(reports), "fix_offered": witness["fix_offered"]}, indent=2))
        return
    if args.cmd == "report":
        card = compare(load_trials(args.trials))
        print(render(card))
        return
    if args.cmd == "engine":
        summary = run_episode(root, seed=args.seed, oracle=args.oracle, window=args.window)
        summary["trace"] = str(summary["trace"])
        print(json.dumps(summary, indent=2))
        return
    if args.cmd == "list":
        catalog_dir = root / "catalog"
        if not catalog_dir.exists():
            return
        for path in sorted(catalog_dir.glob("*.json")):
            print(path.stem)


def _load(root: Path, slug: str) -> dict:
    path = root / "catalog" / f"{slug}.json"
    if not path.exists():
        raise SystemExit(f"no catalog entry: {slug}")
    return json.loads(path.read_text(encoding="utf-8"))
