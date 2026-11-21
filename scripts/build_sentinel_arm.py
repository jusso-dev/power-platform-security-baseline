#!/usr/bin/env python3
"""Compile Microsoft Sentinel YAML analytics rules and workbook into deployable ARM templates."""

from __future__ import annotations

import json
import pathlib
import re

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES_ROOT = REPO_ROOT / "sentinel" / "analytics-rules"
WORKBOOK_JSON = REPO_ROOT / "sentinel" / "workbooks" / "PowerPlatformSecurityPosture.json"
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


def build_all_in_one_template(all_rules: list[dict]) -> dict:
    resources = [rule_to_arm_resource(rule) for rule in all_rules]
    parameters: dict = {
        "workspaceName": {
            "type": "string",
            "metadata": {
                "description": "Name of the Microsoft Sentinel Log Analytics workspace."
            },
        },
        "deployWorkbook": {
            "type": "bool",
            "defaultValue": True,
            "metadata": {
                "description": "Deploy the Power Platform Security Posture workbook alongside all analytics rules."
            },
        },
        "workbookDisplayName": {
            "type": "string",
            "defaultValue": "Power Platform Security Posture",
            "metadata": {
                "description": "Display name of the Microsoft Sentinel workbook."
            },
        },
    }

    if WORKBOOK_JSON.is_file():
        wb_data = json.loads(WORKBOOK_JSON.read_text(encoding="utf-8"))
        resources.append(
            {
                "condition": "[parameters('deployWorkbook')]",
                "type": "Microsoft.Insights/workbooks",
                "apiVersion": "2022-04-01",
                "name": "[guid(resourceId('Microsoft.OperationalInsights/workspaces', parameters('workspaceName')), parameters('workbookDisplayName'))]",
                "location": "[resourceGroup().location]",
                "kind": "shared",
                "properties": {
                    "displayName": "[parameters('workbookDisplayName')]",
                    "serializedData": json.dumps(wb_data),
                    "version": "1.0",
                    "sourceId": "[resourceId('Microsoft.OperationalInsights/workspaces', parameters('workspaceName'))]",
                    "category": "sentinel",
                },
            }
        )

    return {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "description": "One-step Microsoft Sentinel deployment package containing all custom Power Platform, Power Automate, Dataverse and Copilot Studio scheduled analytics rules plus the Power Platform Security Posture workbook.",
            "author": "power-platform-security-baseline",
        },
        "parameters": parameters,
        "resources": resources,
    }


def main() -> int:
    ARM_ROOT.mkdir(parents=True, exist_ok=True)
    all_rules: list[dict] = []
    for subdir in sorted(p for p in RULES_ROOT.iterdir() if p.is_dir()):
        rules = [
            yaml.safe_load(f.read_text(encoding="utf-8"))
            for f in sorted(subdir.glob("*.yaml"))
        ]
        if not rules:
            continue
        all_rules.extend(rules)
        template = build_template(
            rules,
            description=f"Microsoft Sentinel scheduled analytics rules for {subdir.name}.",
        )
        out_path = ARM_ROOT / f"{subdir.name}-rules.json"
        out_path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
        print(f"Generated {out_path.relative_to(REPO_ROOT)} ({len(rules)} rules)")

    all_in_one = build_all_in_one_template(all_rules)
    all_in_one_path = ARM_ROOT / "all-in-one-sentinel-deployment.json"
    all_in_one_path.write_text(json.dumps(all_in_one, indent=2) + "\n", encoding="utf-8")
    print(
        f"Generated {all_in_one_path.relative_to(REPO_ROOT)} "
        f"({len(all_rules)} rules + workbook)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
