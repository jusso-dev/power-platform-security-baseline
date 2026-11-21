"""Read-only tenant-level baseline checks (PP-TEN-* and tenant-scoped PP-CS-*)."""

from __future__ import annotations

from typing import Any

from pp_assessor.engine import CheckRegistry, ReadOnlyDataProvider
from pp_assessor.models import BaselineItem, CheckResult, CheckStatus

HIGH_RISK_CONNECTORS = (
    "shared_http",
    "shared_ftp",
    "shared_sftpwithssh",
    "shared_gmail",
    "shared_outlook",
    "shared_dropbox",
    "shared_googledrive",
)

COPILOT_NO_AUTH_CONNECTORS = (
    "shared_pva-no-auth",
    "chat without microsoft entra id authentication",
)

COPILOT_BLOCKED_CHANNELS = (
    "shared_pva-directline",
    "shared_pva-facebook",
)

COPILOT_BLOCKED_KNOWLEDGE = (
    "shared_pva-knowledge-bing",
)

COPILOT_BLOCKED_SKILLS_AND_HTTP = (
    "shared_pva-skills",
    "shared_http",
)


def _tenant_result(
    item: BaselineItem,
    provider: ReadOnlyDataProvider,
    status: CheckStatus,
    details: str,
    evidence: dict[str, Any] | None = None,
) -> list[CheckResult]:
    return [
        CheckResult(
            baseline_id=item.id,
            check_id=item.assessor_check_id or "manual",
            title=item.title,
            scope=item.scope,
            workload=item.workload,
            severity=item.severity,
            status=status,
            target_id=provider.tenant_id,
            target_name="Tenant",
            details=details,
            recommended_value=item.recommended_value,
            remediation=item.configure_summary,
            ism_controls=list(item.ism_controls),
            essential_eight=list(item.essential_eight),
            evidence=evidence or {},
        )
    ]


def _policy_blocked_connectors(policy: dict[str, Any]) -> set[str]:
    """Extract lower-cased connector IDs and names in the Blocked group of a DLP policy."""
    blocked: set[str] = set()
    groups = policy.get("connectorGroups") or policy.get("properties", {}).get("connectorGroups", [])
    for group in groups:
        if not isinstance(group, dict):
            continue
        classification = str(group.get("classification", "")).strip().lower()
        if classification != "blocked":
            continue
        for conn in group.get("connectors", []):
            if not isinstance(conn, dict):
                continue
            for key in ("id", "name", "displayName"):
                val = conn.get(key)
                if isinstance(val, str) and val.strip():
                    lowered = val.strip().lower()
                    blocked.add(lowered)
                    if "/" in lowered:
                        blocked.add(lowered.rsplit("/", 1)[-1])
    return blocked


def _policy_default_classification(policy: dict[str, Any]) -> str:
    default_cls = policy.get("defaultConnectorsClassification") or policy.get(
        "properties", {}
    ).get("defaultConnectorsClassification", "")
    return str(default_cls).strip().lower()


def _policy_applies_to_env(policy: dict[str, Any], env_id: str) -> bool:
    env_type = str(
        policy.get("environmentType")
        or policy.get("properties", {}).get("environmentType", "")
    ).strip()
    env_list = policy.get("environments") or policy.get("properties", {}).get("environments", [])
    env_ids = {
        str(e.get("name") or e.get("id", "")).strip().lower()
        for e in env_list
        if isinstance(e, dict)
    }
    target = env_id.strip().lower()
    if env_type == "AllEnvironments":
        return True
    if env_type == "OnlyEnvironments":
        return target in env_ids
    if env_type == "ExceptEnvironments":
        return target not in env_ids
    return False


def _policy_is_tenant_wide(policy: dict[str, Any]) -> bool:
    env_type = str(
        policy.get("environmentType")
        or policy.get("properties", {}).get("environmentType", "")
    ).strip()
    return env_type in ("AllEnvironments", "ExceptEnvironments")


def _all_tenant_wide_blocked_connectors(policies: list[dict[str, Any]]) -> set[str]:
    blocked: set[str] = set()
    for policy in policies:
        if _policy_is_tenant_wide(policy):
            blocked.update(_policy_blocked_connectors(policy))
    return blocked


def register_tenant_checks(registry: CheckRegistry) -> None:
    """Register all automatable tenant-level Power Platform and Copilot Studio checks."""

    @registry.register("pp_ten_restrict_prod_env_creation")
    def check_restrict_prod_env_creation(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        settings = provider.get_tenant_settings()
        disabled = bool(settings.get("disableEnvironmentCreationByNonAdminUsers", False))
        status = CheckStatus.PASS if disabled else CheckStatus.FAIL
        details = (
            "Production and sandbox environment creation is restricted to admins."
            if disabled
            else "Non-admin users are permitted to create production and sandbox environments."
        )
        return _tenant_result(
            item,
            provider,
            status,
            details,
            {"disableEnvironmentCreationByNonAdminUsers": disabled},
        )

    @registry.register("pp_ten_restrict_trial_env_creation")
    def check_restrict_trial_env_creation(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        settings = provider.get_tenant_settings()
        disabled = bool(settings.get("disableTrialEnvironmentCreationByNonAdminUsers", False))
        status = CheckStatus.PASS if disabled else CheckStatus.FAIL
        details = (
            "Trial environment creation is restricted to admins."
            if disabled
            else "Non-admin users are permitted to create trial environments."
        )
        return _tenant_result(
            item,
            provider,
            status,
            details,
            {"disableTrialEnvironmentCreationByNonAdminUsers": disabled},
        )

    @registry.register("pp_ten_disable_self_service_purchases")
    def check_disable_self_service_purchases(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        settings = provider.get_tenant_settings()
        trial_disabled = bool(settings.get("disableTrialEnvironmentCreationByNonAdminUsers", False))
        policies = provider.get_self_service_purchase_policies()
        if not policies:
            return _tenant_result(
                item,
                provider,
                CheckStatus.MANUAL,
                "Microsoft 365 self-service purchase policies were not supplied by the API; verify manually in the M365 admin centre.",
                {"disableTrialEnvironmentCreationByNonAdminUsers": trial_disabled},
            )
        enabled_products = [
            str(p.get("productName") or p.get("productId"))
            for p in policies
            if bool(p.get("allowSelfServicePurchase", True))
        ]
        if trial_disabled and not enabled_products:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                "Self-service purchases and non-admin trials are disabled for Power Platform products.",
                {"enabled_products": []},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Self-service purchase or trials remain enabled (products: {', '.join(enabled_products) or 'none'}; trial_disabled={trial_disabled}).",
            {"enabled_products": enabled_products, "trial_disabled": trial_disabled},
        )

    @registry.register("pp_ten_tenant_isolation_enabled")
    def check_tenant_isolation_enabled(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        iso = provider.get_tenant_isolation()
        props = iso.get("properties", iso)
        is_disabled = props.get("isDisabled", True)
        allowed = props.get("allowedTenants", []) or []
        has_wildcard = any(
            isinstance(rule, dict) and str(rule.get("tenantId", "")).strip() == "*"
            for rule in allowed
        )
        if is_disabled is False and not has_wildcard:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"Tenant isolation is enabled with {len(allowed)} explicit allow-list rule(s) and no wildcard.",
                {"isDisabled": False, "allowedTenantsCount": len(allowed)},
            )
        reason = (
            "Tenant isolation contains a wildcard '*' allow-list rule."
            if has_wildcard
            else "Tenant isolation is disabled (cross-tenant connections are unrestricted)."
        )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            reason,
            {"isDisabled": is_disabled, "hasWildcard": has_wildcard},
        )

    @registry.register("pp_ten_default_env_dlp_policy")
    def check_default_env_dlp_policy(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        default_envs = [
            e
            for e in envs
            if bool(e.get("properties", {}).get("isDefault", False))
            or str(e.get("properties", {}).get("environmentSku", "")).lower() == "default"
        ]
        if not default_envs:
            return _tenant_result(
                item,
                provider,
                CheckStatus.FAIL,
                "Could not locate the default environment in tenant environment inventory.",
            )
        default_env_id = str(default_envs[0].get("name") or default_envs[0].get("id", ""))
        policies = provider.get_dlp_policies()
        covering = [p for p in policies if _policy_applies_to_env(p, default_env_id)]
        strict = [
            p
            for p in covering
            if _policy_default_classification(p) == "blocked"
            and len(_policy_blocked_connectors(p)) > 0
        ]
        if strict:
            names = [str(p.get("displayName") or p.get("name", "unnamed")) for p in strict]
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"Default environment ({default_env_id}) is covered by restrictive DLP policy: {', '.join(names)}.",
                {"defaultEnvironmentId": default_env_id, "strictPolicies": names},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Default environment ({default_env_id}) lacks a DLP policy setting new connectors to Blocked with blocked connectors defined (covering policies: {len(covering)}).",
            {"defaultEnvironmentId": default_env_id, "coveringPolicies": len(covering)},
        )

    @registry.register("pp_ten_dlp_blocks_high_risk_connectors")
    def check_dlp_blocks_high_risk_connectors(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        blocked = _all_tenant_wide_blocked_connectors(provider.get_dlp_policies())
        missing = [c for c in HIGH_RISK_CONNECTORS if c not in blocked]
        if not missing:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                "All baseline high-risk HTTP, file transfer and consumer connectors are blocked in tenant-wide DLP.",
                {"checkedConnectors": list(HIGH_RISK_CONNECTORS)},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"High-risk connectors not blocked in tenant-wide DLP: {', '.join(missing)}.",
            {"missingBlockedConnectors": missing},
        )

    @registry.register("pp_ten_default_env_routing")
    def check_default_env_routing(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        settings = provider.get_tenant_settings()
        gov = settings.get("powerPlatform", {}).get("governance", {})
        enabled = bool(
            gov.get("enableDefaultEnvironmentRouting", False)
            or settings.get("enableDefaultEnvironmentRouting", False)
        )
        status = CheckStatus.PASS if enabled else CheckStatus.FAIL
        details = (
            "Default environment routing is enabled for new makers."
            if enabled
            else "Default environment routing is disabled; new makers land in the shared default environment."
        )
        return _tenant_result(item, provider, status, details, {"enableDefaultEnvironmentRouting": enabled})

    @registry.register("pp_ten_managed_environments_enabled")
    def check_managed_environments_enabled(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        target_envs = [
            e
            for e in envs
            if bool(e.get("properties", {}).get("isDefault", False))
            or str(e.get("properties", {}).get("environmentSku", "")).lower() in ("production", "default")
        ]
        if not target_envs:
            return _tenant_result(
                item,
                provider,
                CheckStatus.NOT_APPLICABLE,
                "No production or default environments found in tenant inventory.",
            )
        unmanaged = []
        for env in target_envs:
            props = env.get("properties", {})
            level = str(props.get("governanceConfiguration", {}).get("protectionLevel", "Basic"))
            if level.lower() != "standard":
                unmanaged.append(str(props.get("displayName") or env.get("name")))
        if not unmanaged:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"All {len(target_envs)} production and default environments have Managed Environments enabled.",
                {"checkedCount": len(target_envs)},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Managed Environments is not enabled on: {', '.join(unmanaged)}.",
            {"unmanagedEnvironments": unmanaged},
        )

    @registry.register("pp_ten_guest_access_restricted")
    def check_guest_access_restricted(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        authz = provider.get_graph_authorization_policy()
        allow_invites = str(authz.get("allowInvitesFrom", "everyone")).strip()
        settings = provider.get_tenant_settings()
        guest_makers_blocked = bool(
            settings.get("powerPlatform", {})
            .get("powerApps", {})
            .get("disableShareWithEveryone", True)
        )
        invites_restricted = allow_invites in ("adminsAndGuestInviters", "adminsGuestInvitersAndAllMembers", "none")
        strict_invites = allow_invites in ("adminsAndGuestInviters", "none")
        if strict_invites and guest_makers_blocked:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"External guest invitations are restricted ({allow_invites}) and tenant-wide sharing is restricted.",
                {"allowInvitesFrom": allow_invites, "disableShareWithEveryone": guest_makers_blocked},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Guest access is overly permissive (allowInvitesFrom={allow_invites}, disableShareWithEveryone={guest_makers_blocked}).",
            {
                "allowInvitesFrom": allow_invites,
                "invitesRestricted": invites_restricted,
                "disableShareWithEveryone": guest_makers_blocked,
            },
        )

    @registry.register("pp_ten_admin_role_least_privilege")
    def check_admin_role_least_privilege(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        assignments = provider.get_privileged_role_assignments()
        active_count = len(assignments)
        max_standing = 2
        if active_count <= max_standing:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"Standing Power Platform / Dynamics 365 Administrator assignments ({active_count}) are within threshold (<= {max_standing}).",
                {"activeStandingAssignments": active_count, "threshold": max_standing},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Found {active_count} standing Power Platform / Dynamics 365 Administrator assignments (threshold <= {max_standing}); convert to PIM eligible.",
            {"activeStandingAssignments": active_count, "threshold": max_standing},
        )

    @registry.register("pp_ten_cmk_configured")
    def check_cmk_configured(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        policies = provider.get_enterprise_policies()
        encryption_policies = [
            p
            for p in policies
            if str(p.get("kind", "")).lower() == "encryption"
            or str(p.get("properties", {}).get("kind", "")).lower() == "encryption"
        ]
        if encryption_policies:
            names = [str(p.get("name", "unnamed")) for p in encryption_policies]
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"Customer-Managed Key encryption enterprise policy configured ({', '.join(names)}).",
                {"encryptionPolicies": names},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            "No Power Platform Encryption (Customer-Managed Key) enterprise policy found.",
            {"encryptionPolicies": []},
        )

    @registry.register("pp_ten_tenant_level_analytics")
    def check_tenant_level_analytics(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        settings = provider.get_tenant_settings()
        analytics = settings.get("powerPlatform", {}).get("analytics", {})
        enabled = bool(analytics.get("enableTenantLevelAnalytics", False))
        if "disableTenantLevelAnalytics" in settings:
            enabled = enabled or (settings.get("disableTenantLevelAnalytics") is False)
        status = CheckStatus.PASS if enabled else CheckStatus.FAIL
        details = (
            "Tenant-level analytics is enabled."
            if enabled
            else "Tenant-level analytics is disabled."
        )
        return _tenant_result(item, provider, status, details, {"enableTenantLevelAnalytics": enabled})

    @registry.register("pp_ten_environment_groups_configured")
    def check_environment_groups_configured(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        groups = provider.get_environment_groups()
        published = [
            g
            for g in groups
            if bool(g.get("properties", {}).get("rulesPublished", False))
            or len(g.get("properties", {}).get("rules", [])) > 0
        ]
        if published:
            names = [str(g.get("properties", {}).get("displayName") or g.get("name")) for g in published]
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                f"Configured {len(published)} environment group(s) with rules: {', '.join(names)}.",
                {"publishedGroups": names},
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"No environment groups with published governance rules found (total groups: {len(groups)}).",
            {"totalGroups": len(groups)},
        )

    @registry.register("pp_cs_dlp_block_no_auth_chat")
    def check_cs_dlp_block_no_auth_chat(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        blocked = _all_tenant_wide_blocked_connectors(provider.get_dlp_policies())
        if any(token in blocked for token in COPILOT_NO_AUTH_CONNECTORS):
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                "Copilot Studio unauthenticated chat connector is blocked in tenant-wide DLP.",
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            "Copilot Studio 'Chat without Microsoft Entra ID authentication' connector is not blocked in tenant-wide DLP.",
        )

    @registry.register("pp_cs_dlp_restrict_channels")
    def check_cs_dlp_restrict_channels(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        blocked = _all_tenant_wide_blocked_connectors(provider.get_dlp_policies())
        missing = [c for c in COPILOT_BLOCKED_CHANNELS if c not in blocked]
        if not missing:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                "External Copilot Studio publishing channels (Direct Line, Facebook) are blocked in tenant-wide DLP.",
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"External Copilot Studio channel connectors not blocked in tenant-wide DLP: {', '.join(missing)}.",
            {"missingBlockedChannels": missing},
        )

    @registry.register("pp_cs_dlp_restrict_knowledge_sources")
    def check_cs_dlp_restrict_knowledge_sources(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        blocked = _all_tenant_wide_blocked_connectors(provider.get_dlp_policies())
        missing = [c for c in COPILOT_BLOCKED_KNOWLEDGE if c not in blocked]
        if not missing:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                "Public web search knowledge grounding connector for Copilot Studio is blocked in tenant-wide DLP.",
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Copilot Studio public web knowledge connectors not blocked in tenant-wide DLP: {', '.join(missing)}.",
            {"missingBlockedKnowledge": missing},
        )

    @registry.register("pp_cs_dlp_block_skills_and_http")
    def check_cs_dlp_block_skills_and_http(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        blocked = _all_tenant_wide_blocked_connectors(provider.get_dlp_policies())
        missing = [c for c in COPILOT_BLOCKED_SKILLS_AND_HTTP if c not in blocked]
        if not missing:
            return _tenant_result(
                item,
                provider,
                CheckStatus.PASS,
                "Copilot Studio Skills and HTTP connectors are blocked in tenant-wide DLP.",
            )
        return _tenant_result(
            item,
            provider,
            CheckStatus.FAIL,
            f"Copilot Studio skills or HTTP connectors not blocked in tenant-wide DLP: {', '.join(missing)}.",
            {"missingBlockedConnectors": missing},
        )
