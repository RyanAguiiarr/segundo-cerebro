"""Canonical vault-scanning policy: which directories every tool skips.
Part of OKM (Open Knowledge Metabolism).
"""

from __future__ import annotations
import re

BASE_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git",
    ".obsidian",
    ".trash",
    "_trash",
    "_export",
    "__pycache__",
    "node_modules",
    ".claude",
    ".agents",
    ".codex",
    ".gemini",
    ".opencode",
    "templates",
})

EXPORT_ONLY_EXCLUDES: frozenset[str] = frozenset({"excalidraw"})
STATS_ONLY_EXCLUDES: frozenset[str] = frozenset({"raw", "references"})

def excluded_dirs(*extra: str) -> frozenset[str]:
    return frozenset(d.lower() for d in (*BASE_EXCLUDE_DIRS, *extra))

def is_excluded(parts, excludes: frozenset[str]) -> bool:
    return any(str(p).lower() in excludes for p in parts)

FRONTMATTER_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", re.DOTALL)

def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("﻿"):
        text = text[1:]
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]
