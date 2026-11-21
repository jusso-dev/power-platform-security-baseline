---
id: PP-TEN-001
title: Restrict production and sandbox environment creation to administrators
scope: tenant
workload: power-platform
severity: high
recommended_value: disableEnvironmentCreationByNonAdminUsers set to true
rationale: Allowing any licensed user to create production or sandbox environments leads to ungoverned sprawl, inconsistent DLP coverage and unmonitored Dataverse databases.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - Restrict administrative privileges
configure_summary: Power Platform admin centre > Settings > Tenant settings > Environment creation > Restrict production and sandbox environment creation to administrators.
verify_summary: Read tenant settings via the Power Platform BAP API and confirm disableEnvironmentCreationByNonAdminUsers is true.
assessor_check_id: pp_ten_restrict_prod_env_creation
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

# PP-TEN-001: Restrict production and sandbox environment creation to administrators

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Set **Who can create production and sandbox environments** to **Only specific admins** (`disableEnvironmentCreationByNonAdminUsers: true`).
- **Assessor check ID**: `pp_ten_restrict_prod_env_creation` (automated)

## Rationale

By default, any user with an eligible licence can provision new production or sandbox environments. Uncontrolled environment creation fragments governance, can place Dataverse data in unapproved geographies and bypasses onboarding controls such as security groups, auditing and DLP assignment.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (preventing unprivileged users from modifying system configuration) and `ISM-1585` (maintaining governed cloud infrastructure boundaries). Always verify control identifiers against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight) by ensuring only authorised administrators can provision cloud environments.

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Select **Manage** > **Tenant settings**.
3. Open **Environment creation**.
4. Under **Production and sandbox environments**, select **Only specific admins**.
5. Select **Save**.

## How to verify

- **Automated**: Call the read-only Power Platform tenant settings API (`GET https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform/tenantSettings`) and confirm `disableEnvironmentCreationByNonAdminUsers` is `true`.
- **Manual**: In the Power Platform admin centre, navigate to **Manage** > **Tenant settings** > **Environment creation** and confirm production and sandbox creation is restricted to specific admins.

## References

- [Control who can create and manage environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/control-environment-creation)
- [Tenant settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
