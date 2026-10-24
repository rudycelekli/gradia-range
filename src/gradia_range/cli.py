"""gradia-range command line."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from gradia_range.adopt import adopt
from gradia_range.attempt import attempt
from gradia_range.emit import emit


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
