"""Output formatters for JSON, CSV and Markdown assessment reports."""

from __future__ import annotations

import csv
import io
import json
import pathlib

from pp_assessor.models import AssessmentReport, CheckStatus

CSV_COLUMNS = [
    "baseline_id",
    "check_id",
    "scope",
    "workload",
    "target_id",
    "target_name",
    "title",
    "severity",
    "status",
    "ism_controls",
    "essential_eight",
    "recommended_value",
    "details",
    "remediation",
]


def format_json(report: AssessmentReport) -> str:
    """Serialise an assessment report as indented JSON."""
    return json.dumps(report.to_dict(), indent=2, sort_keys=False) + "\n"


def format_csv(report: AssessmentReport) -> str:
    """Serialise an assessment report as RFC 4180 CSV."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for finding in report.findings:
        writer.writerow(
            {
                "baseline_id": finding.baseline_id,
                "check_id": finding.check_id,
                "scope": finding.scope,
                "workload": finding.workload,
                "target_id": finding.target_id,
                "target_name": finding.target_name,
                "title": finding.title,
                "severity": finding.severity,
                "status": finding.status.value,
                "ism_controls": "; ".join(finding.ism_controls),
                "essential_eight": "; ".join(finding.essential_eight),
                "recommended_value": finding.recommended_value,
                "details": finding.details,
                "remediation": finding.remediation,
            }
        )
    return buffer.getvalue()


def _escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def format_markdown(report: AssessmentReport) -> str:
    """Render an assessment report as ASD Blueprint-style Markdown."""
    summary = report.summary
    lines: list[str] = [
        "# Power Platform Security Baseline Assessment Report",
        "",
        "## Overview",
        "",
        f"- **Tenant ID**: `{report.tenant_id}`",
        f"- **Assessment mode**: `{report.mode}`",
        f"- **Generated (UTC)**: `{report.generated_at}`",
        f"- **Schema version**: `{report.schema_version}`",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "| --- | --- |",
        f"| Pass | {summary['pass']} |",
        f"| Fail | {summary['fail']} |",
        f"| Manual | {summary['manual']} |",
        f"| Error | {summary['error']} |",
        f"| Not applicable | {summary['not_applicable']} |",
        f"| **Total** | **{summary['total']}** |",
        "",
        "## Findings",
        "",
    ]

    if not report.findings:
        lines.append("No findings recorded.")
        lines.append("")
        return "\n".join(lines)

    status_order = [
        CheckStatus.FAIL,
        CheckStatus.ERROR,
        CheckStatus.MANUAL,
        CheckStatus.PASS,
        CheckStatus.NOT_APPLICABLE,
    ]
    ordered = sorted(
        report.findings,
        key=lambda f: (status_order.index(f.status), f.baseline_id, f.target_name),
    )

    lines.extend(
        [
            "| Baseline ID | Scope | Target | Severity | Status | Title | ISM controls | Details |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for finding in ordered:
        ism = ", ".join(finding.ism_controls) if finding.ism_controls else "None"
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape_md(finding.baseline_id),
                    _escape_md(finding.scope),
                    _escape_md(finding.target_name),
                    _escape_md(finding.severity),
                    _escape_md(finding.status.value.upper()),
                    _escape_md(finding.title),
                    _escape_md(ism),
                    _escape_md(finding.details),
                ]
            )
            + " |"
        )
    lines.append("")

    failed = [f for f in ordered if f.status == CheckStatus.FAIL]
    if failed:
        lines.append("## Recommended remediation actions")
        lines.append("")
        for finding in failed:
            lines.append(
                f"- **{finding.baseline_id} ({_escape_md(finding.target_name)})**: "
                f"{_escape_md(finding.remediation)}"
            )
        lines.append("")

    return "\n".join(lines)


def write_report(
    report: AssessmentReport,
    fmt: str,
    output_path: pathlib.Path | None,
) -> dict[str, str]:
    """Render report in one or all formats and optionally write to disk."""
    normalised = fmt.lower()
    outputs: dict[str, str] = {}

    if normalised in ("json", "all"):
        outputs["json"] = format_json(report)
    if normalised in ("csv", "all"):
        outputs["csv"] = format_csv(report)
    if normalised in ("markdown", "md", "all"):
        outputs["markdown"] = format_markdown(report)

    if not outputs:
        raise ValueError(f"Unsupported output format: {fmt}")

    if output_path is not None:
        if normalised == "all":
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "report.json").write_text(outputs["json"], encoding="utf-8")
            (output_path / "report.csv").write_text(outputs["csv"], encoding="utf-8")
            (output_path / "report.md").write_text(outputs["markdown"], encoding="utf-8")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            content = next(iter(outputs.values()))
            output_path.write_text(content, encoding="utf-8")

    return outputs
