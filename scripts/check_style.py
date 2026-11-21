#!/usr/bin/env python3
"""Check repository files for banned characters and basic secret patterns.

Enforces CONTRIBUTING.md style rules:
- No em dashes (U+2014)
- No emojis
- No accidental private keys or GitHub personal access tokens
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
    ".pytest_cache",
    ".ruff_cache",
}

EXCLUDED_FILES = {
    "LICENSE",
    "LICENSE-docs",
    "docs/research/pp-sentinel-research.tsx",
}

TEXT_EXTENSIONS = {
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".jsonc",
    ".toml",
    ".py",
    ".ps1",
    ".psm1",
    ".psd1",
    ".kql",
    ".bicep",
    ".txt",
    ".sh",
    ".csv",
}

# Em dash
EM_DASH = "\u2014"

# Common Unicode emoji ranges and modifiers
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F680-\U0001F6FF"  # Transport and Map
    "\U0001F700-\U0001F77F"  # Alchemical Symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U0001F1E0-\U0001F1FF"  # Regional Indicator Symbols (flags)
    "\U00002600-\U000026FF"  # Misc Symbols
    "\U00002700-\U000027BF"  # Dingbats
    "\U0000FE0F"             # Variation Selector-16
    "]"
)

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private key header", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub classic token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]


def iter_files(root: pathlib.Path) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if rel in EXCLUDED_FILES:
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        files.append(path)
    return files


def check_file(path: pathlib.Path, root: pathlib.Path) -> list[str]:
    rel = path.relative_to(root).as_posix()
    errors: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return errors

    for line_no, line in enumerate(content.splitlines(), start=1):
        if EM_DASH in line:
            errors.append(f"{rel}:{line_no}: banned character em dash (U+2014) found")
        match = EMOJI_RE.search(line)
        if match:
            cp = f"U+{ord(match.group(0)):04X}"
            errors.append(f"{rel}:{line_no}: banned emoji or symbol character ({cp}) found")
        if rel != "scripts/check_style.py":
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    errors.append(f"{rel}:{line_no}: potential secret detected ({label})")
    return errors


def main() -> int:
    all_errors: list[str] = []
    files = iter_files(REPO_ROOT)
    for path in files:
        all_errors.extend(check_file(path, REPO_ROOT))

    if all_errors:
        print("Style check failed:", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"Style check passed ({len(files)} files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
