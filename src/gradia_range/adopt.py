"""Pin a repository as a catalog entry."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from gradia_range.scan import scan_paths, scan_tree


def slug_from_source(source: str) -> str:
    cleaned = source.removesuffix(".git").rstrip("/")
    if cleaned.startswith("https://github.com/"):
        owner_repo = cleaned.removeprefix("https://github.com/")
        return owner_repo.replace("/", "-").lower()
    return Path(cleaned).name.lower().replace(" ", "-")


def adopt(source: str, root: Path, refresh: bool = False) -> dict:
    root = root.resolve()
    slug = slug_from_source(source)
    catalog_path = root / "catalog" / f"{slug}.json"
    if catalog_path.exists() and not refresh:
        return json.loads(catalog_path.read_text(encoding="utf-8"))
    if source.startswith("https://github.com/"):
        catalog = _adopt_github(source, root, slug)
    else:
        catalog = _adopt_local(Path(source), root, slug)
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    return catalog


def _adopt_local(path: Path, root: Path, slug: str) -> dict:
    if not path.exists():
        raise SystemExit(f"source does not exist: {path}")
    dest = root / "twins" / slug
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", str(path), str(dest)], check=True)
    revision = subprocess.check_output(["git", "-C", str(dest), "rev-parse", "HEAD"], text=True).strip()
    scanned = scan_tree(dest)
    return _catalog(slug, str(path), revision, scanned, checkout="local")


def _adopt_github(source: str, root: Path, slug: str) -> dict:
    owner_repo = source.removesuffix(".git").removeprefix("https://github.com/")
    free = shutil.disk_usage(root).free
    dest = root / "twins" / slug
    if free >= 2_000_000_000:
        if dest.exists():
            shutil.rmtree(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", source, str(dest)], check=True)
        revision = subprocess.check_output(["git", "-C", str(dest), "rev-parse", "HEAD"], text=True).strip()
        scanned = scan_tree(dest)
        return _catalog(slug, source, revision, scanned, checkout="local")
    revision = _gh(["repos/" + owner_repo + "/commits/HEAD", "--jq", ".sha"]).strip().strip('"')
    listing = _gh([f"repos/{owner_repo}/git/trees/{revision}?recursive=1"])
    tree = json.loads(listing)
    paths = [item["path"] for item in tree.get("tree", []) if item.get("type") == "blob"]
    interesting = [
        path
        for path in paths
        if path.endswith("package.json") or path.endswith("pyproject.toml") or "docker-compose" in path
    ]
    texts: dict[str, str] = {}
    for path in interesting:
        if path.count("/") > 2:
            continue
        if not path.endswith("package.json") and not path.endswith("pyproject.toml"):
            continue
        texts[path] = _file_text(owner_repo, revision, path)
    scanned = scan_paths(interesting, texts)
    note = (
        f"Pinned {revision} from the GitHub tree. A working copy was not unpacked: "
        f"{free} bytes free, under the 2GB checkout floor."
    )
    return _catalog(slug, source, revision, scanned, checkout="pinned-remote", note=note)


def _file_text(owner_repo: str, revision: str, path: str) -> str:
    payload = json.loads(_gh([f"repos/{owner_repo}/contents/{path}?ref={revision}"]))
    if payload.get("encoding") != "base64":
        return ""
    import base64

    return base64.b64decode(payload["content"]).decode("utf-8", errors="replace")


def _gh(args: list[str]) -> str:
    return subprocess.check_output(["gh", "api", *args], text=True)


def _catalog(slug: str, source: str, revision: str, scanned: dict, checkout: str, note: str = "") -> dict:
    modules = scanned["modules"]
    if not modules:
        modules = [{"id": "repo", "path": ".", "language": "unknown"}]
    return {
        "slug": slug,
        "source": source,
        "revision": revision,
        "checkout": checkout,
        "note": note,
        "modules": modules,
        "integrations": scanned["integrations"],
        "grant": "open",
    }
