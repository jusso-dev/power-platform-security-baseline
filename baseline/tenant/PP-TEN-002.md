---
id: PP-TEN-002
title: Restrict trial environment creation to administrators
scope: tenant
workload: power-platform
severity: medium
recommended_value: disableTrialEnvironmentCreationByNonAdminUsers set to true
rationale: Unrestricted trial environments create shadow IT workspaces where users connect corporate data sources without environment security groups, auditing or change control.
ism_controls:
  - ISM-0407
  - ISM-1405
essential_eight:
  - Restrict administrative privileges
configure_summary: Power Platform admin centre > Settings > Tenant settings > Environment creation > Restrict trial environment creation to administrators.
verify_summary: Read tenant settings via the Power Platform BAP API and confirm disableTrialEnvironmentCreationByNonAdminUsers is true.
assessor_check_id: pp_ten_restrict_trial_env_creation
automated: true
sentinel_rules:
  - C3 - Environment lifecycle operation outside approved regions or controls
references:
  - title: Control who can create and manage environments - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/control-environment-creation
  - title: Tenant settings - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-002: Restrict trial environment creation to administrators

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Set **Who can create trial environments** to **Only specific admins** (`disableTrialEnvironmentCreationByNonAdminUsers: true`).
- **Assessor check ID**: `pp_ten_restrict_trial_env_creation` (automated)

## Rationale

Trial environments are short-lived and often excluded from targeted production DLP policies and Dataverse audit onboarding. Restricting trial environment creation prevents users from bypassing production guardrails to prototype flows or apps against sensitive corporate systems.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (restricting configuration changes to privileged accounts) and `ISM-1405` (preventing unauthorised software or cloud service provisioning). Check the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Select **Manage** > **Tenant settings** > **Environment creation**.
3. Under **Trial environments**, select **Only specific admins**.
4. Select **Save**.

## How to verify

- **Automated**: Query the read-only tenant settings API and verify `disableTrialEnvironmentCreationByNonAdminUsers` is `true`.
- **Manual**: Inspect **Manage** > **Tenant settings** > **Environment creation** in the Power Platform admin centre and confirm trial environment creation is limited to specific admins.

## References

- [Control who can create and manage environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/control-environment-creation)
- [Tenant settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
