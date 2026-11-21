"""Tests for JSON, CSV and Markdown report formatters."""

from __future__ import annotations

import csv
import io
import json
import pathlib

from pp_assessor.formatters import format_csv, format_json, format_markdown, write_report
from pp_assessor.models import AssessmentReport, CheckResult, CheckStatus


def _sample_report() -> AssessmentReport:
    return AssessmentReport(
        tenant_id="00000000-0000-0000-0000-000000000001",
        mode="fixture",
        generated_at="2026-11-21T00:00:00Z",
        findings=[
            CheckResult(
                baseline_id="PP-TEN-004",
                check_id="pp_ten_tenant_isolation_enabled",
                title="Enable tenant isolation",
                scope="tenant",
                workload="power-platform",
                severity="critical",
                status=CheckStatus.FAIL,
                target_id="00000000-0000-0000-0000-000000000001",
                target_name="Tenant",
                details="Tenant isolation is disabled.",
                recommended_value="Tenant isolation enabled",
                remediation="Enable tenant isolation in Power Platform admin centre.",
                ism_controls=["ISM-0263", "ISM-1585"],
                essential_eight=["User application hardening"],
            ),
            CheckResult(
                baseline_id="PP-TEN-001",
                check_id="pp_ten_restrict_prod_env_creation",
                title="Restrict production environment creation",
                scope="tenant",
                workload="power-platform",
                severity="high",
                status=CheckStatus.PASS,
                target_id="00000000-0000-0000-0000-000000000001",
                target_name="Tenant",
                details="Non-admin production environment creation is disabled.",
                recommended_value="disableEnvironmentCreationByNonAdminUsers set to true",
                remediation="Restrict environment creation to admins.",
                ism_controls=["ISM-0407"],
                essential_eight=["Restrict administrative privileges"],
            ),
            CheckResult(
                baseline_id="PP-TEN-014",
                check_id="pp_ten_purview_audit_enabled",
                title="Enable Microsoft Purview auditing",
                scope="tenant",
                workload="power-platform",
                severity="critical",
                status=CheckStatus.MANUAL,
                target_id="00000000-0000-0000-0000-000000000001",
                target_name="Tenant",
                details="Verify Purview Audit is enabled.",
                recommended_value="Purview Audit active",
                remediation="Activate Audit in Purview portal.",
                ism_controls=["ISM-0580"],
                essential_eight=[],
            ),
        ],
    )


def test_format_json_structure() -> None:
    report = _sample_report()
    parsed = json.loads(format_json(report))
    assert parsed["tenant_id"] == "00000000-0000-0000-0000-000000000001"
    assert parsed["summary"] == {
        "pass": 1,
        "fail": 1,
        "manual": 1,
        "error": 0,
        "not_applicable": 0,
        "total": 3,
    }
    assert len(parsed["findings"]) == 3


def test_format_csv_rows() -> None:
    report = _sample_report()
    rows = list(csv.DictReader(io.StringIO(format_csv(report))))
    assert len(rows) == 3
    assert rows[0]["baseline_id"] == "PP-TEN-004"
    assert rows[0]["status"] == "fail"
    assert rows[0]["ism_controls"] == "ISM-0263; ISM-1585"


def test_format_markdown_style_and_ordering() -> None:
    report = _sample_report()
    md = format_markdown(report)
    assert "\u2014" not in md  # No em dashes
    assert "| Fail | 1 |" in md
    assert "## Recommended remediation actions" in md
    assert md.index("PP-TEN-004") < md.index("PP-TEN-001")


def test_write_report_all_formats(tmp_path: pathlib.Path) -> None:
    report = _sample_report()
    out_dir = tmp_path / "reports"
    write_report(report, fmt="all", output_path=out_dir)
    assert (out_dir / "report.json").is_file()
    assert (out_dir / "report.csv").is_file()
    assert (out_dir / "report.md").is_file()
