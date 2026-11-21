---
id: PP-TEN-008
title: Activate Managed Environments on production and default environments
scope: tenant
workload: power-platform
severity: high
recommended_value: Managed Environments protectionLevel set to Standard on all production and default environments
rationale: Key governance capabilities such as sharing limits, solution checker enforcement, IP firewall, Customer Lockbox and Customer-Managed Keys require Managed Environments.
ism_controls:
  - ISM-1585
  - ISM-1405
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Manage > Environments > Select environment > Enable Managed Environments.
verify_summary: List environments via the BAP API and verify governanceConfiguration.protectionLevel is Standard for all production and default environments.
assessor_check_id: pp_ten_managed_environments_enabled
automated: true
sentinel_rules: []
references:
  - title: Managed environments overview - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-008: Activate Managed Environments on production and default environments

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Enable **Managed Environments** (`governanceConfiguration.protectionLevel == "Standard"`) on the default environment and every production environment across the tenant. Note that Managed Environments require standalone Power Platform or Dynamics 365 licences for users accessing those environments.
- **Assessor check ID**: `pp_ten_managed_environments_enabled` (automated)

## Rationale

Unmanaged environments cannot enforce canvas app and agent sharing limits, automated Solution Checker blocking on import, Dataverse IP firewall, Customer Lockbox or Customer-Managed Keys. Activating Managed Environments establishes the governance baseline required for enterprise security controls.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-1585` (enforcing cloud security governance controls) and `ISM-1405` (restricting unauthorised cloud application behaviour). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight) by unlocking sharing limits and runtime protections.

## How to configure

1. Confirm licensing eligibility for users of target environments.
2. In the Power Platform admin centre, go to **Manage** > **Environments**.
3. Select each production environment and the default environment, then select **Enable Managed Environments**.
4. Configure sharing limits, solution checker enforcement and weekly usage insights, then select **Enable**.

## How to verify

- **Automated**: Call the read-only BAP environments list API and verify that every environment where `environmentSku` is `Production` or `isDefault` is `true` has `properties.governanceConfiguration.protectionLevel == "Standard"`.
- **Manual**: Review the **Type** and **Managed** columns under **Manage** > **Environments** in the Power Platform admin centre.

## References

- [Managed environments overview - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
