#!/usr/bin/env python3
"""Compile Microsoft Sentinel YAML analytics rules into deployable ARM templates."""

from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES_ROOT = REPO_ROOT / "sentinel" / "analytics-rules"
ARM_ROOT = REPO_ROOT / "sentinel" / "arm"

OPERATOR_MAP = {
    "gt": "GreaterThan",
    "lt": "LessThan",
    "eq": "Equal",
    "ne": "NotEqual",
}


def to_iso_duration(value: str) -> str:
    match = re.fullmatch(r"([0-9]+)([mhd])", value.strip())
    if not match:
        raise ValueError(f"Unsupported duration string: {value}")
    num, unit = match.group(1), match.group(2)
    if unit == "m":
        return f"PT{num}M"
    if unit == "h":
        return f"PT{num}H"
    return f"P{num}D"


def rule_to_arm_resource(rule: dict) -> dict:
    properties = {
        "displayName": rule["name"],
        "description": rule["description"].strip(),
        "severity": rule["severity"],
        "enabled": True,
        "query": rule["query"].strip(),
        "queryFrequency": to_iso_duration(rule["queryFrequency"]),
        "queryPeriod": to_iso_duration(rule["queryPeriod"]),
        "triggerOperator": OPERATOR_MAP[rule["triggerOperator"]],
        "triggerThreshold": int(rule["triggerThreshold"]),
        "suppressionDuration": "PT5H",
        "suppressionEnabled": False,
        "tactics": rule["tactics"],
        "techniques": rule["relevantTechniques"],
        "entityMappings": rule["entityMappings"],
        "incidentConfiguration": {
            "createIncident": True,
            "groupingConfiguration": {
                "enabled": False,
                "reopenClosedIncident": False,
                "lookbackDuration": "PT5H",
                "matchingMethod": "AllEntities",
            },
        },
    }
    if rule.get("customDetails"):
        properties["customDetails"] = rule["customDetails"]

    return {
        "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
        "apiVersion": "2023-11-01",
        "name": f"[concat(parameters('workspaceName'), '/Microsoft.SecurityInsights/{rule['id']}')]",
        "kind": "Scheduled",
        "properties": properties,
    }


def build_template(rules: list[dict], description: str) -> dict:
    return {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "description": description,
            "author": "power-platform-security-baseline",
        },
        "parameters": {
            "workspaceName": {
                "type": "string",
                "metadata": {
                    "description": "Name of the Microsoft Sentinel Log Analytics workspace."
                },
            }
        },
        "resources": [rule_to_arm_resource(rule) for rule in rules],
    }


def main() -> int:
    ARM_ROOT.mkdir(parents=True, exist_ok=True)
    generated = 0
    for subdir in sorted(p for p in RULES_ROOT.iterdir() if p.is_dir()):
        rules = [
            yaml.safe_load(f.read_text(encoding="utf-8"))
            for f in sorted(subdir.glob("*.yaml"))
        ]
        if not rules:
            continue
        template = build_template(
            rules,
            description=f"Microsoft Sentinel scheduled analytics rules for {subdir.name}.",
        )
        out_path = ARM_ROOT / f"{subdir.name}-rules.json"
        out_path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
        generated += 1
        print(f"Generated {out_path.relative_to(REPO_ROOT)} ({len(rules)} rules)")
    return 0 if generated >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
