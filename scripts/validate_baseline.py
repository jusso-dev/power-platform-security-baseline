#!/usr/bin/env python3
"""Validate baseline item YAML front matter against baseline-item.schema.json."""

from __future__ import annotations

import json
import pathlib
import re
import sys

import jsonschema
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE_DIR = REPO_ROOT / "baseline"
SCHEMA_PATH = BASELINE_DIR / "schema" / "baseline-item.schema.json"
TEMPLATE_PATH = BASELINE_DIR / "_template.md"

ITEM_DIRS = [
    BASELINE_DIR / "tenant",
    BASELINE_DIR / "environment",
    BASELINE_DIR / "copilot-studio",
]
EXAMPLE_DIR = BASELINE_DIR / "examples"

REQUIRED_HEADINGS = [
    "## Setting and recommended value",
    "## Rationale",
    "## ISM and Essential Eight mapping",
    "## How to configure",
    "## How to verify",
    "## References",
]

FRONT_MATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", re.S)


def parse_markdown_item(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError("Missing YAML front matter delimited by '---'")
    raw_yaml, body = match.group(1), match.group(2)
    data = yaml.safe_load(raw_yaml)
    if not isinstance(data, dict):
        raise ValueError("YAML front matter must be a mapping")
    return data, body


def validate_item(
    path: pathlib.Path,
    validator: jsonschema.Draft202012Validator,
    is_template: bool = False,
) -> tuple[dict | None, list[str]]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    errors: list[str] = []
    try:
        data, body = parse_markdown_item(path)
    except Exception as exc:
        return None, [f"{rel}: {exc}"]

    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{rel}: front matter '{loc}': {err.message}")

    if data.get("automated") is True and not data.get("assessor_check_id"):
        errors.append(f"{rel}: automated items must define a non-null assessor_check_id")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            errors.append(f"{rel}: missing required section '{heading}'")

    if not is_template:
        item_id = data.get("id", "")
        if item_id and path.stem != item_id:
            errors.append(f"{rel}: filename stem '{path.stem}' must match front matter id '{item_id}'")

    return data, errors


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"Schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )

    all_errors: list[str] = []
    checked_count = 0

    if not TEMPLATE_PATH.exists():
        all_errors.append("baseline/_template.md is missing")
    else:
        _, errs = validate_item(TEMPLATE_PATH, validator, is_template=True)
        all_errors.extend(errs)
        checked_count += 1

    if EXAMPLE_DIR.exists():
        for path in sorted(EXAMPLE_DIR.glob("*.md")):
            _, errs = validate_item(path, validator, is_template=False)
            all_errors.extend(errs)
            checked_count += 1

    seen_ids: dict[str, str] = {}
    seen_checks: dict[str, str] = {}
    for directory in ITEM_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            data, errs = validate_item(path, validator, is_template=False)
            all_errors.extend(errs)
            checked_count += 1
            if data:
                item_id = data.get("id")
                if item_id:
                    if item_id in seen_ids:
                        all_errors.append(f"{rel}: duplicate id '{item_id}' (also in {seen_ids[item_id]})")
                    seen_ids[item_id] = rel
                check_id = data.get("assessor_check_id")
                if check_id:
                    if check_id in seen_checks:
                        all_errors.append(
                            f"{rel}: duplicate assessor_check_id '{check_id}' (also in {seen_checks[check_id]})"
                        )
                    seen_checks[check_id] = rel

    if all_errors:
        print("Baseline validation failed:", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"Baseline validation passed ({checked_count} files validated).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
