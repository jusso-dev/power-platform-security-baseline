"""Read-only environment, Dataverse and Copilot Studio baseline checks."""

from __future__ import annotations

import json
from typing import Any

from pp_assessor.engine import CheckRegistry, ReadOnlyDataProvider
from pp_assessor.models import BaselineItem, CheckResult, CheckStatus

ZERO_GUID = "00000000-0000-0000-0000-000000000000"

MANDATORY_BLOCKED_EXTENSIONS = (
    "exe",
    "dll",
    "msi",
    "ps1",
    "bat",
    "cmd",
    "vbs",
    "js",
    "hta",
    "scr",
    "lnk",
)


def _env_meta(env: dict[str, Any]) -> tuple[str, str, dict[str, Any], str, bool, str]:
    props = env.get("properties", {}) if isinstance(env.get("properties"), dict) else {}
    env_id = str(env.get("name") or env.get("id") or "unknown-env")
    display_name = str(props.get("displayName") or env_id)
    sku = str(props.get("environmentSku") or "Unknown")
    is_default = bool(props.get("isDefault", False)) or sku.lower() == "default"
    linked = props.get("linkedEnvironmentMetadata") or {}
    instance_url = str(linked.get("instanceUrl") or "") if isinstance(linked, dict) else ""
    return env_id, display_name, props, sku, is_default, instance_url


def _extended_settings(props: dict[str, Any]) -> dict[str, Any]:
    gov = props.get("governanceConfiguration") or {}
    if not isinstance(gov, dict):
        return {}
    settings = gov.get("settings") or {}
    if not isinstance(settings, dict):
        return {}
    ext = settings.get("extendedSettings") or {}
    return ext if isinstance(ext, dict) else {}


def _is_managed(props: dict[str, Any]) -> bool:
    gov = props.get("governanceConfiguration") or {}
    if not isinstance(gov, dict):
        return False
    return str(gov.get("protectionLevel", "Basic")).strip().lower() == "standard"


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def _env_result(
    item: BaselineItem,
    env_id: str,
    env_name: str,
    status: CheckStatus,
    details: str,
    evidence: dict[str, Any] | None = None,
) -> CheckResult:
    return CheckResult(
        baseline_id=item.id,
        check_id=item.assessor_check_id or "manual",
        title=item.title,
        scope=item.scope,
        workload=item.workload,
        severity=item.severity,
        status=status,
        target_id=env_id,
        target_name=env_name,
        details=details,
        recommended_value=item.recommended_value,
        remediation=item.configure_summary,
        ism_controls=list(item.ism_controls),
        essential_eight=list(item.essential_eight),
        evidence=evidence or {},
    )


def _no_envs_result(item: BaselineItem, provider: ReadOnlyDataProvider) -> list[CheckResult]:
    return [
        _env_result(
            item,
            env_id=provider.tenant_id,
            env_name="Tenant",
            status=CheckStatus.NOT_APPLICABLE,
            details="No environments returned in tenant inventory.",
        )
    ]


def _parse_bot_config(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except ValueError:
            return {}
    return {}


def register_environment_checks(registry: CheckRegistry) -> None:
    """Register all automatable environment, Dataverse and Copilot Studio checks."""

    @registry.register("pp_env_security_group_assigned")
    def check_security_group_assigned(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, _, is_default, _ = _env_meta(env)
            if is_default:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "Default environment does not support a Microsoft Entra security group binding.",
                    )
                )
                continue
            linked = props.get("linkedEnvironmentMetadata") or {}
            sec_group = str(linked.get("securityGroupId") or "").strip() if isinstance(linked, dict) else ""
            if sec_group and sec_group != ZERO_GUID:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"Environment is bound to Microsoft Entra security group {sec_group}.",
                        {"securityGroupId": sec_group},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        "Environment has no Microsoft Entra security group assigned.",
                        {"securityGroupId": sec_group or None},
                    )
                )
        return results

    @registry.register("pp_env_dataverse_auditing_enabled")
    def check_dataverse_auditing_enabled(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, sku, _, instance_url = _env_meta(env)
            if not instance_url:
                results.append(
                    _env_result(
                        item, env_id, name, CheckStatus.NOT_APPLICABLE, "Environment has no Dataverse database."
                    )
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            audit_on = bool(org.get("isauditenabled", False))
            access_on = bool(org.get("isuseraccessauditenabled", False))
            if audit_on and access_on:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        "Dataverse global auditing and user access logging are enabled.",
                        {"isauditenabled": audit_on, "isuseraccessauditenabled": access_on},
                    )
                )
            elif sku.lower() != "production":
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        f"Non-production environment ({sku}); Dataverse auditing is mandatory for production.",
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Dataverse auditing incomplete (isauditenabled={audit_on}, isuseraccessauditenabled={access_on}).",
                        {"isauditenabled": audit_on, "isuseraccessauditenabled": access_on},
                    )
                )
        return results

    @registry.register("pp_env_dataverse_read_auditing")
    def check_dataverse_read_auditing(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, sku, _, instance_url = _env_meta(env)
            if not instance_url:
                results.append(
                    _env_result(item, env_id, name, CheckStatus.NOT_APPLICABLE, "No Dataverse database.")
                )
                continue
            is_sensitive = bool(props.get("isSensitive", sku.lower() == "production"))
            if not is_sensitive:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "Environment is not designated as sensitive for Dataverse read logging.",
                    )
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            read_on = bool(org.get("isreadauditenabled", False))
            status = CheckStatus.PASS if read_on else CheckStatus.FAIL
            details = (
                "Dataverse read auditing (isreadauditenabled) is enabled."
                if read_on
                else "Dataverse read auditing (isreadauditenabled) is disabled on a sensitive production environment."
            )
            results.append(_env_result(item, env_id, name, status, details, {"isreadauditenabled": read_on}))
        return results

    @registry.register("pp_env_sas_logging_purview")
    def check_sas_logging_purview(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, sku, _, instance_url = _env_meta(env)
            if not instance_url or sku.lower() != "production":
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "Applies to production Dataverse environments.",
                    )
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            sas_on = bool(org.get("isenablesaslogginginpurview", False))
            status = CheckStatus.PASS if sas_on else CheckStatus.FAIL
            details = (
                "Dataverse SAS logging in Microsoft Purview is enabled."
                if sas_on
                else "Dataverse SAS logging in Microsoft Purview is disabled."
            )
            results.append(_env_result(item, env_id, name, status, details, {"isenablesaslogginginpurview": sas_on}))
        return results

    @registry.register("pp_env_audit_retention_configured")
    def check_audit_retention_configured(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, sku, _, instance_url = _env_meta(env)
            if not instance_url or sku.lower() != "production":
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "Applies to production Dataverse environments.",
                    )
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            days = org.get("auditretentionperiodv2")
            if isinstance(days, int) and (days >= 90 or days == -1):
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"Dataverse audit retention is configured ({days} days; -1 indicates Forever).",
                        {"auditretentionperiodv2": days},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Dataverse audit retention ({days}) is below the 90-day minimum.",
                        {"auditretentionperiodv2": days},
                    )
                )
        return results

    @registry.register("pp_env_ip_firewall_enabled")
    def check_ip_firewall_enabled(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, sku, _, instance_url = _env_meta(env)
            if not instance_url or sku.lower() != "production":
                results.append(
                    _env_result(item, env_id, name, CheckStatus.NOT_APPLICABLE, "Applies to production Dataverse environments.")
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            enabled = bool(org.get("enableipbasedfirewallrule", False))
            mode = str(org.get("ipbasedfirewallrulemode") or "")
            ranges = str(org.get("allowediprangeforfirewall") or "").strip()
            has_open_cidr = "0.0.0.0/0" in ranges
            if enabled and mode.lower() == "enforce" and ranges and not has_open_cidr:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        "Dataverse IP firewall is enabled in Enforce mode with restricted CIDR ranges.",
                        {"mode": mode, "allowedIpRanges": ranges},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Dataverse IP firewall not enforced cleanly (enabled={enabled}, mode={mode or 'unset'}, openCidr={has_open_cidr}).",
                        {"enabled": enabled, "mode": mode, "allowedIpRanges": ranges},
                    )
                )
        return results

    @registry.register("pp_env_cookie_binding_enabled")
    def check_cookie_binding_enabled(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, sku, _, instance_url = _env_meta(env)
            if not instance_url or sku.lower() != "production":
                results.append(
                    _env_result(item, env_id, name, CheckStatus.NOT_APPLICABLE, "Applies to production Dataverse environments.")
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            enabled = bool(org.get("enableipbasedcookiebinding", False))
            status = CheckStatus.PASS if enabled else CheckStatus.FAIL
            details = (
                "IP address-based cookie binding is enabled."
                if enabled
                else "IP address-based cookie binding is disabled."
            )
            results.append(_env_result(item, env_id, name, status, details, {"enableipbasedcookiebinding": enabled}))
        return results

    @registry.register("pp_env_session_timeout_configured")
    def check_session_timeout_configured(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, sku, _, instance_url = _env_meta(env)
            if not instance_url or sku.lower() != "production":
                results.append(
                    _env_result(item, env_id, name, CheckStatus.NOT_APPLICABLE, "Applies to production Dataverse environments.")
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            sess_on = bool(org.get("sessiontimeoutenabled", False))
            sess_mins = org.get("sessiontimeoutinmins")
            idle_on = bool(org.get("inactivitytimeoutenabled", False))
            idle_mins = org.get("inactivitytimeoutinmins")
            ok = (
                sess_on
                and isinstance(sess_mins, int)
                and 0 < sess_mins <= 480
                and idle_on
                and isinstance(idle_mins, int)
                and 0 < idle_mins <= 60
            )
            status = CheckStatus.PASS if ok else CheckStatus.FAIL
            details = (
                f"Session timeout ({sess_mins}m) and inactivity timeout ({idle_mins}m) meet baseline thresholds."
                if ok
                else f"Session/inactivity timeout non-compliant (session={sess_on}/{sess_mins}m, inactivity={idle_on}/{idle_mins}m)."
            )
            results.append(
                _env_result(
                    item,
                    env_id,
                    name,
                    status,
                    details,
                    {
                        "sessiontimeoutenabled": sess_on,
                        "sessiontimeoutinmins": sess_mins,
                        "inactivitytimeoutenabled": idle_on,
                        "inactivitytimeoutinmins": idle_mins,
                    },
                )
            )
        return results

    @registry.register("pp_env_sharing_limits_configured")
    def check_sharing_limits_configured(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, _, _, _ = _env_meta(env)
            if not _is_managed(props):
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        "Managed Environments is not enabled; sharing limits cannot be enforced.",
                    )
                )
                continue
            ext = _extended_settings(props)
            exclude_groups = _as_bool(ext.get("excludeSharingWithSecurityGroups", False))
            raw_limit = ext.get("maxLimitUserSharing")
            try:
                max_users = int(raw_limit) if raw_limit is not None else -1
            except (TypeError, ValueError):
                max_users = -1
            if exclude_groups and 1 <= max_users <= 20:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"Sharing limits enforced (excludeSecurityGroups=true, maxUsers={max_users}).",
                        {"excludeSharingWithSecurityGroups": True, "maxLimitUserSharing": max_users},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Sharing limits weak or unset (excludeSecurityGroups={exclude_groups}, maxUsers={max_users}).",
                        {"excludeSharingWithSecurityGroups": exclude_groups, "maxLimitUserSharing": max_users},
                    )
                )
        return results

    @registry.register("pp_env_solution_checker_block")
    def check_solution_checker_block(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, sku, _, _ = _env_meta(env)
            if not _is_managed(props):
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        "Managed Environments is not enabled; Solution Checker enforcement unavailable.",
                    )
                )
                continue
            ext = _extended_settings(props)
            mode = str(ext.get("solutionCheckerMode") or "None").strip()
            required = {"block"} if sku.lower() == "production" else {"block", "warn"}
            if mode.lower() in required:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"Solution Checker mode is '{mode}' for {sku} environment.",
                        {"solutionCheckerMode": mode},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Solution Checker mode is '{mode}' (expected Block for production, Warn or Block otherwise).",
                        {"solutionCheckerMode": mode},
                    )
                )
        return results

    @registry.register("pp_env_backup_retention_extended")
    def check_backup_retention_extended(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, sku, _, _ = _env_meta(env)
            if sku.lower() != "production":
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        f"Extended 28-day backup retention applies to production environments (sku={sku}).",
                    )
                )
                continue
            days = props.get("backupRetentionPeriodInDays")
            if isinstance(days, int) and days >= 28:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"Automated backup retention is {days} days (>= 28 days).",
                        {"backupRetentionPeriodInDays": days},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Automated backup retention is {days} days (expected >= 28 days).",
                        {"backupRetentionPeriodInDays": days},
                    )
                )
        return results

    @registry.register("pp_env_customer_lockbox_enabled")
    def check_customer_lockbox_enabled(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        settings = provider.get_tenant_settings()
        tenant_lockbox = bool(
            settings.get("powerPlatform", {})
            .get("security", {})
            .get("enableCustomerLockbox", False)
            or settings.get("enableCustomerLockbox", False)
        )
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, sku, _, _ = _env_meta(env)
            if sku.lower() != "production":
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "Customer Lockbox baseline applies to production Managed Environments.",
                    )
                )
                continue
            env_lockbox = bool(props.get("isLockboxEnabled", tenant_lockbox))
            if _is_managed(props) and env_lockbox:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        "Customer Lockbox is enabled on this Managed Environment.",
                        {"isManaged": True, "isLockboxEnabled": True},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Customer Lockbox inactive (isManaged={_is_managed(props)}, isLockboxEnabled={env_lockbox}).",
                        {"isManaged": _is_managed(props), "isLockboxEnabled": env_lockbox},
                    )
                )
        return results

    @registry.register("pp_env_blocked_file_extensions")
    def check_blocked_file_extensions(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, _, _, instance_url = _env_meta(env)
            if not instance_url:
                results.append(
                    _env_result(item, env_id, name, CheckStatus.NOT_APPLICABLE, "No Dataverse database.")
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            raw = str(org.get("blockedattachments") or "")
            present = {ext.strip().lstrip(".").lower() for ext in raw.split(";") if ext.strip()}
            missing = [ext for ext in MANDATORY_BLOCKED_EXTENSIONS if ext not in present]
            if not missing:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        "All mandatory dangerous file extensions are present in Dataverse blockedattachments.",
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Missing mandatory blocked file extensions: {', '.join(missing)}.",
                        {"missingExtensions": missing},
                    )
                )
        return results

    @registry.register("pp_cs_agent_auth_required")
    def check_cs_agent_auth_required(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, _, _, instance_url = _env_meta(env)
            if not instance_url:
                continue
            bots = provider.get_copilot_studio_bots(env_id, instance_url)
            active_bots = [b for b in bots if b.get("statecode", 0) == 0]
            if not active_bots:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "No active Copilot Studio agents found in this environment.",
                    )
                )
                continue
            unauth = [
                str(b.get("name") or b.get("botid"))
                for b in active_bots
                if str(b.get("authenticationmode")) in ("1", "None", "NoAuthentication")
            ]
            if not unauth:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"All {len(active_bots)} active Copilot Studio agent(s) require authentication.",
                        {"activeBots": len(active_bots)},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Copilot Studio agent(s) configured with No authentication: {', '.join(unauth)}.",
                        {"unauthenticatedBots": unauth},
                    )
                )
        return results or _no_envs_result(item, provider)

    @registry.register("pp_cs_web_channel_security")
    def check_cs_web_channel_security(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, _, _, instance_url = _env_meta(env)
            if not instance_url:
                continue
            bots = [b for b in provider.get_copilot_studio_bots(env_id, instance_url) if b.get("statecode", 0) == 0]
            web_bots = []
            insecure = []
            for bot in bots:
                cfg = _parse_bot_config(bot.get("configuration"))
                channels = cfg.get("channels") or []
                uses_web = bool(cfg.get("webChannelEnabled", False)) or any(
                    str(c).lower() in ("web", "directline", "customwebsite") for c in channels
                )
                if not uses_web:
                    continue
                web_bots.append(bot)
                if not _as_bool(cfg.get("webChannelSecurityEnabled", False)):
                    insecure.append(str(bot.get("name") or bot.get("botid")))
            if not web_bots:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "No active Copilot Studio agents expose web or Direct Line channels.",
                    )
                )
            elif not insecure:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"All {len(web_bots)} web-published agent(s) enforce Web channel security.",
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Web-published agent(s) missing Web channel security: {', '.join(insecure)}.",
                        {"insecureWebBots": insecure},
                    )
                )
        return results or _no_envs_result(item, provider)

    @registry.register("pp_cs_agent_sharing_limits")
    def check_cs_agent_sharing_limits(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, props, _, _, _ = _env_meta(env)
            if not _is_managed(props):
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        "Managed Environments is not enabled; Copilot Studio agent sharing limits cannot be enforced.",
                    )
                )
                continue
            ext = _extended_settings(props)
            agent_exclude = _as_bool(
                ext.get("excludeAgentSharingWithSecurityGroups", ext.get("excludeSharingWithSecurityGroups", False))
            )
            raw_cap = ext.get("maxLimitAgentUserSharing", ext.get("maxLimitUserSharing"))
            try:
                cap = int(raw_cap) if raw_cap is not None else -1
            except (TypeError, ValueError):
                cap = -1
            if agent_exclude and 1 <= cap <= 20:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        f"Copilot Studio agent sharing limits enforced (excludeSecurityGroups=true, cap={cap}).",
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Copilot Studio agent sharing limits weak or unset (excludeSecurityGroups={agent_exclude}, cap={cap}).",
                    )
                )
        return results

    @registry.register("pp_cs_audit_and_sentinel_coverage")
    def check_cs_audit_and_sentinel_coverage(
        item: BaselineItem, provider: ReadOnlyDataProvider
    ) -> list[CheckResult]:
        envs = provider.get_environments()
        if not envs:
            return _no_envs_result(item, provider)
        results: list[CheckResult] = []
        for env in envs:
            env_id, name, _, _, _, instance_url = _env_meta(env)
            if not instance_url:
                continue
            bots = provider.get_copilot_studio_bots(env_id, instance_url)
            if not bots:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.NOT_APPLICABLE,
                        "No Copilot Studio agents present in this environment.",
                    )
                )
                continue
            org = provider.get_dataverse_org_settings(env_id, instance_url)
            audit_on = bool(org.get("isauditenabled", False))
            bot_audit_on = bool(org.get("isbotauditenabled", audit_on))
            if audit_on and bot_audit_on:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.PASS,
                        "Dataverse auditing is enabled on this agent environment (verify CopilotActivity ingestion in Sentinel manually).",
                        {"isauditenabled": audit_on, "isbotauditenabled": bot_audit_on},
                    )
                )
            else:
                results.append(
                    _env_result(
                        item,
                        env_id,
                        name,
                        CheckStatus.FAIL,
                        f"Dataverse bot table auditing gap (isauditenabled={audit_on}, isbotauditenabled={bot_audit_on}).",
                        {"isauditenabled": audit_on, "isbotauditenabled": bot_audit_on},
                    )
                )
        return results or _no_envs_result(item, provider)
