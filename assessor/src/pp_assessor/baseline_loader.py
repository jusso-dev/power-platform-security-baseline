"""Load security baseline items from YAML front matter in baseline/."""

from __future__ import annotations

import pathlib
import re

import yaml

from pp_assessor.models import BaselineItem, BaselineReference

FRONT_MATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)
SUBDIRS = ("tenant", "environment", "copilot-studio")


def default_baseline_dir() -> pathlib.Path:
    """Locate the repository baseline/ directory relative to this package."""
    current = pathlib.Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "baseline"
        if candidate.is_dir() and (candidate / "schema").is_dir():
            return candidate
    return pathlib.Path.cwd() / "baseline"


def load_baseline_items(baseline_dir: pathlib.Path | None = None) -> list[BaselineItem]:
    """Read and parse all baseline Markdown items under baseline/."""
    root = baseline_dir or default_baseline_dir()
    items: list[BaselineItem] = []

    for sub in SUBDIRS:
        folder = root / sub
        if not folder.is_dir():
            continue
        for md_file in sorted(folder.glob("*.md")):
            if md_file.name.lower() == "readme.md":
                continue
            text = md_file.read_text(encoding="utf-8")
            match = FRONT_MATTER_RE.match(text)
            if not match:
                continue
            data = yaml.safe_load(match.group(1))
            if not isinstance(data, dict):
                continue
            refs = [
                BaselineReference(title=str(r["title"]), url=str(r["url"]))
                for r in data.get("references", [])
                if isinstance(r, dict) and "title" in r and "url" in r
            ]
            items.append(
                BaselineItem(
                    id=str(data["id"]),
                    title=str(data["title"]),
                    scope=str(data["scope"]),
                    workload=str(data["workload"]),
                    severity=str(data["severity"]),
                    recommended_value=str(data["recommended_value"]),
                    rationale=str(data["rationale"]),
                    ism_controls=[str(c) for c in data.get("ism_controls", [])],
                    essential_eight=[str(e) for e in data.get("essential_eight", [])],
                    configure_summary=str(data["configure_summary"]),
                    verify_summary=str(data["verify_summary"]),
                    assessor_check_id=data.get("assessor_check_id"),
                    automated=bool(data.get("automated", False)),
                    sentinel_rules=[str(r) for r in data.get("sentinel_rules", [])],
                    references=refs,
                    last_verified=str(data.get("last_verified", "")),
                )
            )
    return items
