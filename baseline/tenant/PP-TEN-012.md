---
id: PP-TEN-012
title: Enable tenant-level analytics and capacity monitoring
scope: tenant
workload: power-platform
severity: low
recommended_value: Tenant-level analytics enabled in Power Platform tenant settings
rationale: Tenant-level analytics provides visibility across all environments into app, flow and connector usage as well as audit log storage capacity before log truncation occurs.
ism_controls:
  - ISM-0580
  - ISM-1405
essential_eight: []
configure_summary: Power Platform admin centre > Manage > Tenant settings > Tenant-level analytics > Enable.
verify_summary: Read tenant settings via the BAP API and verify tenant-level analytics is enabled.
assessor_check_id: pp_ten_tenant_level_analytics
automated: true
sentinel_rules: []
references:
  - title: Tenant-level analytics - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/tenant-level-analytics
  - title: Power Platform inventory - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/power-platform-inventory
  - title: Dataverse storage capacity - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-012: Enable tenant-level analytics and capacity monitoring

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Enable **Tenant-level analytics** in the Power Platform admin centre (`disableTenantLevelAnalytics: false` / `enableTenantLevelAnalytics: true`) and monitor Dataverse Log capacity alongside Power Platform inventory.
- **Assessor check ID**: `pp_ten_tenant_level_analytics` (automated)

## Rationale

Administrators cannot secure environments, connectors or makers they cannot see. Enabling tenant-level analytics and monitoring Dataverse log capacity ensures security teams have cross-environment visibility and can detect storage pressure before Dataverse auditing is impacted.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0580` (monitoring event logs and capacity for security operations) and `ISM-1405` (maintaining asset visibility across cloud services). Verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Go to **Manage** > **Tenant settings** > **Tenant-level analytics**.
3. Turn **Enable tenant-level analytics** to **On** and select **Save**.
4. Configure capacity alerts under **Licensing** > **Capacity** to warn before Dataverse log storage is exhausted.

## How to verify

- **Automated**: Read tenant settings via the read-only BAP API and confirm tenant-level analytics is enabled (`powerPlatform.analytics.enableTenantLevelAnalytics == true` or `disableTenantLevelAnalytics == false`).
- **Manual**: Confirm **Tenant-level analytics** is **On** under **Manage** > **Tenant settings** and verify reports populate in the **Monitor** section.

## References

- [Tenant-level analytics - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/tenant-level-analytics)
- [Power Platform inventory - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/power-platform-inventory)
- [Dataverse storage capacity - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
