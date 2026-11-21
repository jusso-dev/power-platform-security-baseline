"""Tests for baseline loading, engine execution and CLI offline mode."""

from __future__ import annotations

import json
import pathlib

from pp_assessor.baseline_loader import load_baseline_items
from pp_assessor.cli import main
from pp_assessor.engine import CheckRegistry, FixtureDataProvider, run_assessment
from pp_assessor.models import CheckResult, CheckStatus

FIXTURE_PATH = pathlib.Path(__file__).resolve().parent / "fixtures" / "minimal_tenant.json"


def test_loads_repo_baseline_items() -> None:
    items = load_baseline_items()
    ids = {item.id for item in items}
    assert "PP-TEN-001" in ids
    assert "PP-ENV-001" in ids


def test_engine_executes_registered_check_and_marks_manual() -> None:
    registry = CheckRegistry()

    @registry.register("pp_ten_restrict_prod_env_creation")
    def check_prod_creation(item, provider):
        val = bool(provider.get_tenant_settings().get("disableEnvironmentCreationByNonAdminUsers"))
        return [
            CheckResult(
                baseline_id=item.id,
                check_id=item.assessor_check_id or "",
                title=item.title,
                scope=item.scope,
                workload=item.workload,
                severity=item.severity,
                status=CheckStatus.PASS if val else CheckStatus.FAIL,
                target_id=provider.tenant_id,
                target_name="Tenant",
                details=f"disableEnvironmentCreationByNonAdminUsers={val}",
                recommended_value=item.recommended_value,
                remediation=item.configure_summary,
                ism_controls=list(item.ism_controls),
                essential_eight=list(item.essential_eight),
            )
        ]

    provider = FixtureDataProvider.from_file(FIXTURE_PATH)
    report = run_assessment(provider=provider, registry=registry, scopes={"tenant"})

    by_id = {f.baseline_id: f for f in report.findings}
    assert by_id["PP-TEN-001"].status == CheckStatus.PASS
    assert by_id["PP-TEN-014"].status == CheckStatus.MANUAL


def test_cli_outputs_all_formats_offline(tmp_path: pathlib.Path) -> None:
    out_dir = tmp_path / "cli-out"
    rc = main(
        [
            "assess",
            "--fixture",
            str(FIXTURE_PATH),
            "--scope",
            "tenant",
            "--format",
            "all",
            "--output",
            str(out_dir),
        ]
    )
    assert rc == 0
    payload = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert payload["mode"] == "fixture"
    assert payload["summary"]["total"] >= 14
    assert (out_dir / "report.csv").is_file()
    assert (out_dir / "report.md").is_file()
