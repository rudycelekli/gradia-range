"""Find modules and declared integrations in a tree or a path list."""

from __future__ import annotations

import os
import re
from pathlib import Path

SKIP = {
    ".git",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".venv",
    "venv",
    "target",
    "__pycache__",
    ".next",
    "coverage",
}

MANIFESTS = {
    "package.json": "node",
    "pyproject.toml": "python",
    "go.mod": "go",
    "Cargo.toml": "rust",
    "pom.xml": "java",
    "Gemfile": "ruby",
}

INTEGRATIONS = {
    "slack": ("slack", "@slack/"),
    "discord": ("discord",),
    "stripe": ("stripe",),
    "github": ("octokit", "pygithub"),
    "email": ("nodemailer", "sendgrid", "mailgun"),
    "object_store": ("boto3", "@aws-sdk/client-s3", "minio"),
    "postgres": ("psycopg", "postgresql", "asyncpg", "prisma"),
    "redis": ("ioredis", "redis"),
}

HTTP_SIMS = {"slack", "discord", "stripe", "github", "email", "object_store"}


def module_id(rel: str) -> str:
    if rel in {"", "."}:
        return "repo"
    slug = re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")
    return slug[:80] or "repo"


def scan_paths(paths: list[str], texts: dict[str, str] | None = None) -> dict:
    """Build modules from manifest paths. `texts` maps a path to file contents."""
    texts = texts or {}
    modules: list[dict] = []
    seen: set[str] = set()
    for path in sorted(paths):
        name = path.rsplit("/", 1)[-1]
        if name not in MANIFESTS:
            continue
        if any(part in SKIP for part in path.split("/")):
            continue
        parent = path.rsplit("/", 1)[0] if "/" in path else "."
        # Direct product packages, plus the repo root. Skip nested examples and fixtures.
        if parent != "." and parent.count("/") > 1:
            continue
        mid = module_id(parent)
        if mid in seen:
            continue
        seen.add(mid)
        modules.append({"id": mid, "path": parent, "language": MANIFESTS[name]})
    integrations = _integrations(texts, paths)
    return {"modules": modules, "integrations": integrations}


def scan_tree(root: Path) -> dict:
    paths: list[str] = []
    texts: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP]
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        depth = 0 if rel_dir == "." else rel_dir.count("/") + 1
        if depth > 2:
            dirnames.clear()
            continue
        for filename in filenames:
            if filename not in MANIFESTS and filename not in {"docker-compose.yml", "compose.yml", "compose.yaml"}:
                continue
            rel = filename if rel_dir == "." else f"{rel_dir}/{filename}"
            paths.append(rel)
            if filename in MANIFESTS:
                file_path = Path(dirpath) / filename
                if file_path.stat().st_size <= 1_000_000:
                    texts[rel] = file_path.read_text(encoding="utf-8", errors="replace")
    return scan_paths(paths, texts)


def _integrations(texts: dict[str, str], paths: list[str]) -> list[dict]:
    blob = "\n".join(texts.values()).lower()
    path_blob = "\n".join(paths).lower()
    found: list[dict] = []
    for name, needles in INTEGRATIONS.items():
        hit = any(needle in blob or needle in path_blob for needle in needles)
        if name == "slack" and "/slack/" in f"/{path_blob}/":
            hit = True
        if not hit:
            continue
        kind = "http" if name in HTTP_SIMS else "declared"
        found.append({"name": name, "kind": kind})
    return found
