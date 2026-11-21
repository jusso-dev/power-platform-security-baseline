"""Unit tests for all tenant-level baseline checks using mocked fixtures and HTTP responses."""

from __future__ import annotations

import json
import pathlib

from pp_assessor.auth import StaticTokenProvider
from pp_assessor.baseline_loader import load_baseline_items
from pp_assessor.cli import default_registry
from pp_assessor.engine import FixtureDataProvider, LiveApiDataProvider, run_assessment
from pp_assessor.http_client import ReadOnlyHttpClient
from pp_assessor.models import CheckStatus

FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"
COMPLIANT_FIXTURE = FIXTURES_DIR / "tenant_compliant.json"
NONCOMPLIANT_FIXTURE = FIXTURES_DIR / "tenant_noncompliant.json"


def test_every_automated_tenant_baseline_item_has_a_registered_check() -> None:
    registry = default_registry()
    tenant_items = [i for i in load_baseline_items() if i.scope == "tenant" and i.automated]
    assert len(tenant_items) >= 17
    missing = [
        item.id
        for item in tenant_items
        if not item.assessor_check_id or registry.get(item.assessor_check_id) is None
    ]
    assert missing == [], f"Unregistered automated tenant checks: {missing}"


def test_compliant_tenant_passes_all_automated_checks_and_flags_manual() -> None:
    provider = FixtureDataProvider.from_file(COMPLIANT_FIXTURE)
    report = run_assessment(provider=provider, registry=default_registry(), scopes={"tenant"})
    by_id = {f.baseline_id: f for f in report.findings}

    # All 13 automated PP-TEN checks pass
    for num in range(1, 14):
        bid = f"PP-TEN-{num:03d}"
        assert by_id[bid].status == CheckStatus.PASS, f"{bid} failed: {by_id[bid].details}"

    # Tenant-scoped Copilot Studio DLP checks pass
    for bid in ("PP-CS-002", "PP-CS-003", "PP-CS-005", "PP-CS-006"):
        assert by_id[bid].status == CheckStatus.PASS, f"{bid} failed: {by_id[bid].details}"

    # Manual items reported explicitly as manual
    assert by_id["PP-TEN-014"].status == CheckStatus.MANUAL
    assert by_id["PP-CS-010"].status == CheckStatus.MANUAL
    assert report.summary["fail"] == 0
    assert report.summary["error"] == 0


def test_noncompliant_tenant_fails_all_automated_checks() -> None:
    provider = FixtureDataProvider.from_file(NONCOMPLIANT_FIXTURE)
    report = run_assessment(provider=provider, registry=default_registry(), scopes={"tenant"})
    by_id = {f.baseline_id: f for f in report.findings}

    for num in range(1, 14):
        bid = f"PP-TEN-{num:03d}"
        assert by_id[bid].status == CheckStatus.FAIL, f"{bid} unexpectedly {by_id[bid].status}"

    for bid in ("PP-CS-002", "PP-CS-003", "PP-CS-005", "PP-CS-006"):
        assert by_id[bid].status == CheckStatus.FAIL, f"{bid} unexpectedly {by_id[bid].status}"

    assert by_id["PP-TEN-014"].status == CheckStatus.MANUAL
    assert by_id["PP-CS-010"].status == CheckStatus.MANUAL


def test_tenant_isolation_wildcard_fails() -> None:
    payload = json.loads(COMPLIANT_FIXTURE.read_text(encoding="utf-8"))
    payload["tenant_isolation"]["properties"]["allowedTenants"] = [
        {"tenantId": "*", "direction": "InboundAndOutbound"}
    ]
    provider = FixtureDataProvider(payload=payload)
    report = run_assessment(provider=provider, registry=default_registry(), scopes={"tenant"})
    by_id = {f.baseline_id: f for f in report.findings}
    assert by_id["PP-TEN-004"].status == CheckStatus.FAIL
    assert "wildcard" in by_id["PP-TEN-004"].details.lower()


def test_live_api_provider_executes_only_get_requests_against_mocked_transport() -> None:
    sample = json.loads(COMPLIANT_FIXTURE.read_text(encoding="utf-8"))
    seen_methods: list[str] = []

    class FakeResp:
        def __init__(self, body: dict) -> None:
            self._body = json.dumps(body).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self) -> bytes:
            return self._body

    def fake_opener(req, timeout):
        seen_methods.append(req.get_method())
        url = req.full_url
        if "tenantSettings" in url:
            return FakeResp(sample["tenant_settings"])
        if "tenantIsolationPolicy" in url:
            return FakeResp(sample["tenant_isolation"])
        if "apiPolicies" in url:
            return FakeResp({"value": sample["dlp_policies"]})
        if "environmentGroups" in url:
            return FakeResp({"value": sample["environment_groups"]})
        if "enterprisePolicies" in url:
            return FakeResp({"value": sample["enterprise_policies"]})
        if "/environments" in url:
            return FakeResp({"value": sample["environments"]})
        if "authorizationPolicy" in url:
            return FakeResp(sample["graph_authorization_policy"])
        if "roleAssignments" in url:
            return FakeResp({"value": sample["privileged_role_assignments"]})
        return FakeResp({})

    http_client = ReadOnlyHttpClient(opener=fake_opener)
    provider = LiveApiDataProvider(
        tenant_id=sample["tenant_id"],
        token_provider=StaticTokenProvider(),
        http_client=http_client,
    )
    report = run_assessment(provider=provider, registry=default_registry(), scopes={"tenant"})
    assert seen_methods and all(m == "GET" for m in seen_methods)
    assert report.summary["error"] == 0
    assert report.summary["pass"] >= 16
