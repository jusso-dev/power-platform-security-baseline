"""Core read-only assessment engine, data providers and check registry."""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from pp_assessor.auth import (
    BAP_DEFAULT_SCOPE,
    DELEGATED_GRAPH_READ_SCOPES,
    GRAPH_DEFAULT_SCOPE,
    TokenProvider,
    dataverse_scope_for_instance,
)
from pp_assessor.baseline_loader import load_baseline_items
from pp_assessor.http_client import HttpRequestError, ReadOnlyHttpClient
from pp_assessor.models import AssessmentReport, BaselineItem, CheckResult, CheckStatus

BAP_BASE_URL = "https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform"
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
POWER_PLATFORM_ADMIN_ROLE_TEMPLATE_ID = "11648597-926c-4cf3-9c36-bcebb0ba8dcc"
DYNAMICS_365_ADMIN_ROLE_TEMPLATE_ID = "44367163-eba1-44c3-98af-f5787879f96a"


class ReadOnlyDataProvider(Protocol):
    """Read-only abstraction supplying tenant and environment configuration snapshots."""

    tenant_id: str
    mode: str

    def get_tenant_settings(self) -> dict[str, Any]: ...
    def get_tenant_isolation(self) -> dict[str, Any]: ...
    def get_dlp_policies(self) -> list[dict[str, Any]]: ...
    def get_environments(self) -> list[dict[str, Any]]: ...
    def get_environment_groups(self) -> list[dict[str, Any]]: ...
    def get_enterprise_policies(self) -> list[dict[str, Any]]: ...
    def get_graph_authorization_policy(self) -> dict[str, Any]: ...
    def get_privileged_role_assignments(self) -> list[dict[str, Any]]: ...
    def get_self_service_purchase_policies(self) -> list[dict[str, Any]]: ...
    def get_dataverse_org_settings(self, environment_id: str, instance_url: str) -> dict[str, Any]: ...
    def get_copilot_studio_bots(self, environment_id: str, instance_url: str) -> list[dict[str, Any]]: ...


@dataclass
class FixtureDataProvider:
    """Offline fixture data provider for deterministic unit tests and air-gapped demos."""

    payload: dict[str, Any]
    mode: str = "fixture"

    @classmethod
    def from_file(cls, path: pathlib.Path) -> FixtureDataProvider:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Fixture file must contain a JSON object: {path}")
        return cls(payload=data)

    @property
    def tenant_id(self) -> str:
        return str(self.payload.get("tenant_id", "00000000-0000-0000-0000-000000000000"))

    def get_tenant_settings(self) -> dict[str, Any]:
        return dict(self.payload.get("tenant_settings", {}))

    def get_tenant_isolation(self) -> dict[str, Any]:
        return dict(self.payload.get("tenant_isolation", {}))

    def get_dlp_policies(self) -> list[dict[str, Any]]:
        return list(self.payload.get("dlp_policies", []))

    def get_environments(self) -> list[dict[str, Any]]:
        return list(self.payload.get("environments", []))

    def get_environment_groups(self) -> list[dict[str, Any]]:
        return list(self.payload.get("environment_groups", []))

    def get_enterprise_policies(self) -> list[dict[str, Any]]:
        return list(self.payload.get("enterprise_policies", []))

    def get_graph_authorization_policy(self) -> dict[str, Any]:
        return dict(self.payload.get("graph_authorization_policy", {}))

    def get_privileged_role_assignments(self) -> list[dict[str, Any]]:
        return list(self.payload.get("privileged_role_assignments", []))

    def get_self_service_purchase_policies(self) -> list[dict[str, Any]]:
        return list(self.payload.get("self_service_purchase_policies", []))

    def get_dataverse_org_settings(self, environment_id: str, instance_url: str) -> dict[str, Any]:
        by_env = self.payload.get("dataverse_org_settings", {})
        if isinstance(by_env, dict):
            return dict(by_env.get(environment_id, {}))
        return {}

    def get_copilot_studio_bots(self, environment_id: str, instance_url: str) -> list[dict[str, Any]]:
        by_env = self.payload.get("copilot_studio_bots", {})
        if isinstance(by_env, dict):
            return list(by_env.get(environment_id, []))
        return []


class LiveApiDataProvider:
    """Live read-only API provider calling supported Power Platform, Graph and Dataverse GET endpoints."""

    def __init__(
        self,
        tenant_id: str,
        token_provider: TokenProvider,
        http_client: ReadOnlyHttpClient | None = None,
        delegated: bool = False,
    ) -> None:
        self.tenant_id = tenant_id
        self.mode = "delegated" if delegated else "app-only"
        self._tokens = token_provider
        self._http = http_client or ReadOnlyHttpClient()
        self._delegated = delegated

    def _bap_token(self) -> str:
        return self._tokens.get_token([BAP_DEFAULT_SCOPE])

    def _graph_token(self) -> str:
        scopes = list(DELEGATED_GRAPH_READ_SCOPES) if self._delegated else [GRAPH_DEFAULT_SCOPE]
        return self._tokens.get_token(scopes)

    def get_tenant_settings(self) -> dict[str, Any]:
        url = f"{BAP_BASE_URL}/tenantSettings?api-version=2023-06-01"
        return self._http.get_json(url, access_token=self._bap_token())

    def get_tenant_isolation(self) -> dict[str, Any]:
        url = (
            f"{BAP_BASE_URL}/scopes/admin/tenantIsolationPolicy"
            f"?api-version=2020-10-01&tenantId={self.tenant_id}"
        )
        return self._http.get_json(url, access_token=self._bap_token())

    def get_dlp_policies(self) -> list[dict[str, Any]]:
        url = f"{BAP_BASE_URL}/scopes/admin/apiPolicies?api-version=2021-04-01"
        return self._http.get_paginated(url, access_token=self._bap_token())

    def get_environments(self) -> list[dict[str, Any]]:
        url = f"{BAP_BASE_URL}/scopes/admin/environments?api-version=2023-06-01"
        return self._http.get_paginated(url, access_token=self._bap_token())

    def get_environment_groups(self) -> list[dict[str, Any]]:
        url = f"{BAP_BASE_URL}/scopes/admin/environmentGroups?api-version=2023-06-01"
        return self._http.get_paginated(url, access_token=self._bap_token())

    def get_enterprise_policies(self) -> list[dict[str, Any]]:
        url = f"{BAP_BASE_URL}/enterprisePolicies?api-version=2022-03-01-preview"
        return self._http.get_paginated(url, access_token=self._bap_token())

    def get_graph_authorization_policy(self) -> dict[str, Any]:
        url = f"{GRAPH_BASE_URL}/policies/authorizationPolicy"
        return self._http.get_json(url, access_token=self._graph_token())

    def get_privileged_role_assignments(self) -> list[dict[str, Any]]:
        url = (
            f"{GRAPH_BASE_URL}/roleManagement/directory/roleAssignments"
            f"?$filter=roleDefinitionId eq '{POWER_PLATFORM_ADMIN_ROLE_TEMPLATE_ID}' "
            f"or roleDefinitionId eq '{DYNAMICS_365_ADMIN_ROLE_TEMPLATE_ID}'"
        )
        return self._http.get_paginated(url, access_token=self._graph_token())

    def get_self_service_purchase_policies(self) -> list[dict[str, Any]]:
        return []

    def get_dataverse_org_settings(self, environment_id: str, instance_url: str) -> dict[str, Any]:
        if not instance_url:
            return {}
        token = self._tokens.get_token([dataverse_scope_for_instance(instance_url)])
        base = instance_url.rstrip("/")
        select = (
            "isauditenabled,isuseraccessauditenabled,isreadauditenabled,"
            "auditretentionperiodv2,enableipbasedfirewallrule,ipbasedfirewallrulemode,"
            "allowediprangeforfirewall,enableipbasedcookiebinding,sessiontimeoutenabled,"
            "sessiontimeoutinmins,inactivitytimeoutenabled,inactivitytimeoutinmins,"
            "blockedattachments,isenablesaslogginginpurview"
        )
        url = f"{base}/api/data/v9.2/organizations?$select={select}"
        payload = self._http.get_json(url, access_token=token)
        items = payload.get("value", [])
        return dict(items[0]) if isinstance(items, list) and items else {}

    def get_copilot_studio_bots(self, environment_id: str, instance_url: str) -> list[dict[str, Any]]:
        if not instance_url:
            return []
        token = self._tokens.get_token([dataverse_scope_for_instance(instance_url)])
        base = instance_url.rstrip("/")
        url = (
            f"{base}/api/data/v9.2/bots"
            "?$select=botid,name,authenticationmode,authenticationtrigger,configuration,statecode"
        )
        try:
            return self._http.get_paginated(url, access_token=token)
        except HttpRequestError as exc:
            if exc.status_code == 404:
                return []
            raise


CheckFunc = Callable[[BaselineItem, ReadOnlyDataProvider], list[CheckResult]]


@dataclass
class CheckRegistry:
    """Registry mapping assessor_check_id values to read-only evaluator callables."""

    _checks: dict[str, CheckFunc] = field(default_factory=dict)

    def register(self, check_id: str) -> Callable[[CheckFunc], CheckFunc]:
        def decorator(func: CheckFunc) -> CheckFunc:
            self._checks[check_id] = func
            return func

        return decorator

    def get(self, check_id: str) -> CheckFunc | None:
        return self._checks.get(check_id)

    def registered_ids(self) -> set[str]:
        return set(self._checks.keys())


def build_manual_result(
    item: BaselineItem,
    target_id: str,
    target_name: str,
    reason: str | None = None,
) -> CheckResult:
    """Create a standardised manual verification finding for non-automated items."""
    return CheckResult(
        baseline_id=item.id,
        check_id=item.assessor_check_id or "manual",
        title=item.title,
        scope=item.scope,
        workload=item.workload,
        severity=item.severity,
        status=CheckStatus.MANUAL,
        target_id=target_id,
        target_name=target_name,
        details=reason or f"Manual verification required: {item.verify_summary}",
        recommended_value=item.recommended_value,
        remediation=item.configure_summary,
        ism_controls=list(item.ism_controls),
        essential_eight=list(item.essential_eight),
    )


class CachingDataProvider:
    """Per-run read-only cache avoiding duplicate API calls across multiple checks."""

    def __init__(self, inner: ReadOnlyDataProvider) -> None:
        self._inner = inner
        self.tenant_id = inner.tenant_id
        self.mode = inner.mode
        self._cache: dict[str, Any] = {}

    def _cached(self, key: str, loader: Callable[[], Any]) -> Any:
        if key not in self._cache:
            self._cache[key] = loader()
        return self._cache[key]

    def get_tenant_settings(self) -> dict[str, Any]:
        return self._cached("tenant_settings", self._inner.get_tenant_settings)

    def get_tenant_isolation(self) -> dict[str, Any]:
        return self._cached("tenant_isolation", self._inner.get_tenant_isolation)

    def get_dlp_policies(self) -> list[dict[str, Any]]:
        return self._cached("dlp_policies", self._inner.get_dlp_policies)

    def get_environments(self) -> list[dict[str, Any]]:
        return self._cached("environments", self._inner.get_environments)

    def get_environment_groups(self) -> list[dict[str, Any]]:
        return self._cached("environment_groups", self._inner.get_environment_groups)

    def get_enterprise_policies(self) -> list[dict[str, Any]]:
        return self._cached("enterprise_policies", self._inner.get_enterprise_policies)

    def get_graph_authorization_policy(self) -> dict[str, Any]:
        return self._cached("graph_authz", self._inner.get_graph_authorization_policy)

    def get_privileged_role_assignments(self) -> list[dict[str, Any]]:
        return self._cached("priv_roles", self._inner.get_privileged_role_assignments)

    def get_self_service_purchase_policies(self) -> list[dict[str, Any]]:
        return self._cached("self_service", self._inner.get_self_service_purchase_policies)

    def get_dataverse_org_settings(self, environment_id: str, instance_url: str) -> dict[str, Any]:
        return self._cached(
            f"dv_org:{environment_id}",
            lambda: self._inner.get_dataverse_org_settings(environment_id, instance_url),
        )

    def get_copilot_studio_bots(self, environment_id: str, instance_url: str) -> list[dict[str, Any]]:
        return self._cached(
            f"cs_bots:{environment_id}",
            lambda: self._inner.get_copilot_studio_bots(environment_id, instance_url),
        )


def run_assessment(
    provider: ReadOnlyDataProvider,
    registry: CheckRegistry | None = None,
    baseline_dir: pathlib.Path | None = None,
    scopes: set[str] | None = None,
) -> AssessmentReport:
    """Execute registered checks across loaded baseline items and build a report."""
    active_registry = registry or CheckRegistry()
    cached_provider = CachingDataProvider(provider)
    items = load_baseline_items(baseline_dir)
    if scopes:
        items = [item for item in items if item.scope in scopes]

    report = AssessmentReport(tenant_id=cached_provider.tenant_id, mode=cached_provider.mode)

    for item in items:
        if not item.automated or not item.assessor_check_id:
            report.findings.append(
                build_manual_result(item, target_id=cached_provider.tenant_id, target_name="Tenant")
            )
            continue

        check_fn = active_registry.get(item.assessor_check_id)
        if check_fn is None:
            report.findings.append(
                build_manual_result(
                    item,
                    target_id=cached_provider.tenant_id,
                    target_name="Tenant",
                    reason=(
                        f"Automated check '{item.assessor_check_id}' is not registered yet; "
                        f"verify manually: {item.verify_summary}"
                    ),
                )
            )
            continue

        try:
            results = check_fn(item, cached_provider)
            report.findings.extend(results)
        except Exception as exc:
            report.findings.append(
                CheckResult(
                    baseline_id=item.id,
                    check_id=item.assessor_check_id,
                    title=item.title,
                    scope=item.scope,
                    workload=item.workload,
                    severity=item.severity,
                    status=CheckStatus.ERROR,
                    target_id=cached_provider.tenant_id,
                    target_name="Tenant",
                    details=f"Check raised an error: {exc}",
                    recommended_value=item.recommended_value,
                    remediation=item.configure_summary,
                    ism_controls=list(item.ism_controls),
                    essential_eight=list(item.essential_eight),
                )
            )

    return report
