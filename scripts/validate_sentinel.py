#!/usr/bin/env python3
"""Validate Microsoft Sentinel analytics rules, hunting queries, KQL tests, workbooks and ARM templates."""

from __future__ import annotations

import json
import pathlib
import re
import sys

import jsonschema
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SENTINEL_DIR = REPO_ROOT / "sentinel"
RULE_SCHEMA_PATH = SENTINEL_DIR / "schemas" / "analytic-rule.schema.json"
HUNT_SCHEMA_PATH = SENTINEL_DIR / "schemas" / "hunting-query.schema.json"

RETIRED_TABLES = (
    "PowerAppsActivity",
    "PowerPlatformConnectorActivity",
    "PowerPlatformDlpActivity",
    "Dynamics365Activity",
    "LLMActivity",
    "AIAgentsInfo",
)

ISM_RE = re.compile(r"\bISM-[0-9]{4}\b")


def _strip_kql_comments_and_strings(kql: str) -> str:
    """Remove string literals first (preserving URLs), then strip single-line // comments."""
    out: list[str] = []
    for line in kql.splitlines():
        # Strip quoted strings before // comments so https:// inside strings is preserved
        code = re.sub(r'@?"(?:[^"\\]|\\.)*"', '""', line)
        code = re.sub(r"@?'(?:[^'\\]|\\.)*'", "''", code)
        code = code.split("//", 1)[0]
        out.append(code)
    return "\n".join(out)


def check_kql_hygiene(kql: str, label: str) -> list[str]:
    errors: list[str] = []
    for retired in RETIRED_TABLES:
        if re.search(rf"\b{retired}\b", kql):
            errors.append(f"{label}: references retired or legacy table '{retired}'")

    cleaned = _strip_kql_comments_and_strings(kql)
    if "|" not in cleaned:
        errors.append(f"{label}: KQL query must contain at least one pipe operator '|'")

    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in cleaned:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                errors.append(f"{label}: unbalanced delimiter '{ch}' in KQL query")
                break
            stack.pop()
    if stack:
        errors.append(f"{label}: unclosed delimiter(s) {stack} in KQL query")
    return errors


def validate_rules(validator: jsonschema.Draft202012Validator) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    seen_ids: dict[str, str] = {}
    rules_dir = SENTINEL_DIR / "analytics-rules"
    tests_dir = SENTINEL_DIR / "tests"

    if not rules_dir.exists():
        return 0, []

    for path in sorted(rules_dir.rglob("*.yaml")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        count += 1
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{rel}: YAML parse error: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel}: root YAML document must be a mapping")
            continue

        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            loc = ".".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{rel}: '{loc}': {err.message}")

        rule_id = str(data.get("id", ""))
        if rule_id:
            if rule_id in seen_ids:
                errors.append(f"{rel}: duplicate rule id '{rule_id}' (also in {seen_ids[rule_id]})")
            seen_ids[rule_id] = rel

        desc = str(data.get("description", ""))
        custom = data.get("customDetails", {})
        if not ISM_RE.search(desc) and not (isinstance(custom, dict) and "ISMControls" in custom):
            errors.append(f"{rel}: rule must map to at least one ASD ISM control (ISM-####)")

        query = str(data.get("query", ""))
        errors.extend(check_kql_hygiene(query, rel))

        # Check corresponding datatable KQL test exists
        sub_rel = path.relative_to(rules_dir).with_suffix(".kql")
        expected_test = tests_dir / sub_rel
        if not expected_test.is_file():
            errors.append(f"{rel}: missing KQL datatable test at sentinel/tests/{sub_rel.as_posix()}")

    return count, errors


def validate_hunting_queries(validator: jsonschema.Draft202012Validator) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    seen_ids: dict[str, str] = {}
    hunt_dir = SENTINEL_DIR / "hunting-queries"
    if not hunt_dir.exists():
        return 0, []

    for path in sorted(hunt_dir.rglob("*.yaml")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        count += 1
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{rel}: YAML parse error: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel}: root YAML document must be a mapping")
            continue

        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            loc = ".".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{rel}: '{loc}': {err.message}")

        qid = str(data.get("id", ""))
        if qid:
            if qid in seen_ids:
                errors.append(f"{rel}: duplicate hunting query id '{qid}' (also in {seen_ids[qid]})")
            seen_ids[qid] = rel

        errors.extend(check_kql_hygiene(str(data.get("query", "")), rel))

    return count, errors


def validate_kql_tests() -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    tests_dir = SENTINEL_DIR / "tests"
    if not tests_dir.exists():
        return 0, []

    for path in sorted(tests_dir.rglob("*.kql")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        count += 1
        content = path.read_text(encoding="utf-8")
        if "datatable(" not in content:
            errors.append(f"{rel}: KQL test must include synthetic datatable(...) test rows")
        errors.extend(check_kql_hygiene(content, rel))

    return count, errors


def validate_json_artefacts() -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0

    for folder_name in ("arm", "playbooks", "workbooks"):
        folder = SENTINEL_DIR / folder_name
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*.json")):
            rel = path.relative_to(REPO_ROOT).as_posix()
            count += 1
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"{rel}: invalid JSON: {exc}")
                continue
            if not isinstance(data, dict):
                errors.append(f"{rel}: JSON root must be an object")
                continue
            if folder_name in ("arm", "playbooks"):
                for req_key in ("$schema", "contentVersion", "resources"):
                    if req_key not in data:
                        errors.append(f"{rel}: ARM template missing required key '{req_key}'")
            elif folder_name == "workbooks" and not path.name.endswith(".arm.json"):
                if "version" not in data or "items" not in data:
                    errors.append(f"{rel}: Workbook JSON must contain 'version' and 'items'")

    return count, errors


def main() -> int:
    rule_schema = json.loads(RULE_SCHEMA_PATH.read_text(encoding="utf-8"))
    hunt_schema = json.loads(HUNT_SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(rule_schema)
    jsonschema.Draft202012Validator.check_schema(hunt_schema)

    rule_validator = jsonschema.Draft202012Validator(rule_schema)
    hunt_validator = jsonschema.Draft202012Validator(hunt_schema)

    all_errors: list[str] = []
    r_cnt, r_err = validate_rules(rule_validator)
    h_cnt, h_err = validate_hunting_queries(hunt_validator)
    t_cnt, t_err = validate_kql_tests()
    j_cnt, j_err = validate_json_artefacts()

    all_errors.extend(r_err)
    all_errors.extend(h_err)
    all_errors.extend(t_err)
    all_errors.extend(j_err)

    if all_errors:
        print("Sentinel validation failed:", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(
        f"Sentinel validation passed ({r_cnt} rules, {h_cnt} hunting queries, "
        f"{t_cnt} KQL tests, {j_cnt} JSON/ARM artefacts)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
