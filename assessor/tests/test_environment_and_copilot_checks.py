"""Unit and scale tests for environment, Dataverse and Copilot Studio checks."""

from __future__ import annotations

import pathlib
import time

from pp_assessor.baseline_loader import load_baseline_items
from pp_assessor.cli import default_registry
from pp_assessor.engine import FixtureDataProvider, run_assessment
from pp_assessor.models import CheckStatus

FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"
ENV_FIXTURE = FIXTURES_DIR / "environments_full.json"


def test_every_automated_baseline_item_in_repo_has_a_registered_check() -> None:
    registry = default_registry()
    automated_items = [i for i in load_baseline_items() if i.automated]
    assert len(automated_items) >= 34
    missing = [
        item.id
        for item in automated_items
        if not item.assessor_check_id or registry.get(item.assessor_check_id) is None
    ]
    assert missing == [], f"Unregistered automated baseline items: {missing}"


def test_environment_and_copilot_checks_distinguish_compliant_and_noncompliant() -> None:
    provider = FixtureDataProvider.from_file(ENV_FIXTURE)
    report = run_assessment(provider=provider, registry=default_registry(), scopes={"environment"})

    by_key = {(f.baseline_id, f.target_name): f for f in report.findings}

    # All 13 automated PP-ENV checks and 4 environment-scoped PP-CS checks pass on Prod Compliant
    env_ids = [f"PP-ENV-{n:03d}" for n in range(1, 14)] + [
        "PP-CS-001",
        "PP-CS-004",
        "PP-CS-007",
        "PP-CS-009",
    ]
    for bid in env_ids:
        assert by_key[(bid, "Prod Compliant")].status == CheckStatus.PASS, (
            f"{bid} failed on Prod Compliant: {by_key[(bid, 'Prod Compliant')].details}"
        )
        assert by_key[(bid, "Prod NonCompliant")].status == CheckStatus.FAIL, (
            f"{bid} did not fail on Prod NonCompliant: {by_key[(bid, 'Prod NonCompliant')].status}"
        )

    # Manual environment items reported as manual
    manual_ids = {f.baseline_id for f in report.findings if f.status == CheckStatus.MANUAL}
    assert "PP-ENV-014" in manual_ids
    assert "PP-CS-008" in manual_ids
    assert report.summary["error"] == 0


def test_50_environment_fixture_runs_fast_well_under_5_minutes() -> None:
    """Acceptance test: 50 environments must complete well under 5 minutes."""
    envs = []
    dv_orgs = {}
    bots = {}
    for idx in range(50):
        env_id = f"00000000-0000-0000-0000-00000000{idx + 1000:04d}"
        envs.append(
            {
                "name": env_id,
                "properties": {
                    "displayName": f"Production Env {idx + 1:02d}",
                    "isDefault": idx == 0,
                    "environmentSku": "Default" if idx == 0 else "Production",
                    "isSensitive": True,
                    "backupRetentionPeriodInDays": 28,
                    "isLockboxEnabled": True,
                    "linkedEnvironmentMetadata": {
                        "securityGroupId": f"00000000-0000-0000-0000-00000001{idx + 1000:04d}",
                        "instanceUrl": f"https://org{idx + 1000:04d}.crm6.dynamics.com",
                    },
                    "governanceConfiguration": {
                        "protectionLevel": "Standard",
                        "settings": {
                            "extendedSettings": {
                                "excludeSharingWithSecurityGroups": "true",
                                "maxLimitUserSharing": "10",
                                "solutionCheckerMode": "Block",
                            }
                        },
                    },
                },
            }
        )
        dv_orgs[env_id] = {
            "isauditenabled": True,
            "isuseraccessauditenabled": True,
            "isreadauditenabled": True,
            "isenablesaslogginginpurview": True,
            "isbotauditenabled": True,
            "auditretentionperiodv2": 90,
            "enableipbasedfirewallrule": True,
            "ipbasedfirewallrulemode": "Enforce",
            "allowediprangeforfirewall": "203.0.113.0/24",
            "enableipbasedcookiebinding": True,
            "sessiontimeoutenabled": True,
            "sessiontimeoutinmins": 480,
            "inactivitytimeoutenabled": True,
            "inactivitytimeoutinmins": 30,
            "blockedattachments": "exe;dll;msi;ps1;bat;cmd;vbs;js;hta;scr;lnk",
        }
        bots[env_id] = [
            {
                "botid": f"00000000-0000-0000-0000-00000002{idx + 1000:04d}",
                "name": f"Agent {idx + 1:02d}",
                "authenticationmode": 2,
                "statecode": 0,
                "configuration": "{\"channels\":[\"teams\"]}",
            }
        ]

    payload = {
        "tenant_id": "00000000-0000-0000-0000-000000000050",
        "tenant_settings": {
            "disableEnvironmentCreationByNonAdminUsers": True,
            "disableTrialEnvironmentCreationByNonAdminUsers": True,
            "powerPlatform": {
                "governance": {"enableDefaultEnvironmentRouting": True},
                "analytics": {"enableTenantLevelAnalytics": True},
                "security": {"enableCustomerLockbox": True},
                "powerApps": {"disableShareWithEveryone": True},
            },
        },
        "tenant_isolation": {"properties": {"isDisabled": False, "allowedTenants": []}},
        "self_service_purchase_policies": [],
        "dlp_policies": [],
        "environments": envs,
        "environment_groups": [],
        "enterprise_policies": [],
        "graph_authorization_policy": {"allowInvitesFrom": "adminsAndGuestInviters"},
        "privileged_role_assignments": [],
        "dataverse_org_settings": dv_orgs,
        "copilot_studio_bots": bots,
    }

    provider = FixtureDataProvider(payload=payload)
    start = time.monotonic()
    report = run_assessment(provider=provider, registry=default_registry())
    elapsed = time.monotonic() - start

    # 17 automated env checks x 50 environments = 850 env findings + tenant & manual items
    assert report.summary["total"] >= 850
    assert report.summary["error"] == 0
    assert elapsed < 5.0, f"50-environment assessment took {elapsed:.2f}s (expected < 5s / well under 5 min)"
