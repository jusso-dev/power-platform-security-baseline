---
id: PP-TEN-003
title: Disable self-service product trials and purchases for Power Platform
scope: tenant
workload: power-platform
severity: medium
recommended_value: Self-service purchases and trial sign-ups disabled for Power Apps, Power Automate, Power BI and Copilot Studio
rationale: Self-service licence acquisition lets end users bypass procurement, security review and licence governance, enabling premium connectors such as HTTP without administrator oversight.
ism_controls:
  - ISM-0380
  - ISM-1405
essential_eight:
  - Application control
configure_summary: Disable self-service trials in Power Platform tenant settings and disable self-service purchases in Microsoft 365 admin centre.
verify_summary: Check disableCapacityAllocationByEnvironmentAdmins and tenant trial settings via API and verify M365 self-service purchase policy.
assessor_check_id: pp_ten_disable_self_service_purchases
automated: true
sentinel_rules: []
references:
  - title: Manage self-service purchases and trials - Microsoft 365 | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-365/commerce/subscriptions/manage-self-service-purchases-admins
  - title: Tenant settings - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-003: Disable self-service product trials and purchases for Power Platform

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Disable self-service trials (`disableTrialEnvironmentCreationByNonAdminUsers` and tenant self-service trial controls) and block self-service purchases for Power Apps, Power Automate, Power BI and Copilot Studio in Microsoft 365 commerce settings.
- **Assessor check ID**: `pp_ten_disable_self_service_purchases` (automated)

## Rationale

Microsoft permits end users to activate free trials or purchase per-user Power Platform licences directly with a corporate email address unless administrators disable the capability. Unmanaged premium licences unlock custom connectors, HTTP actions and Dataverse access outside approved onboarding processes.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0380` (controlling software and cloud service usage) and `ISM-1405` (preventing unauthorised cloud service acquisition). Always verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Aligns with [Application control](https://www.cyber.gov.au/essential-eight) principles by preventing unapproved platform capabilities from being self-enabled.

## How to configure

1. Sign in to the Microsoft 365 admin centre as a Billing or Global Administrator.
2. Go to **Settings** > **Org settings** > **Services** > **Self-service trials and purchases**.
3. Set Power Apps, Power Automate, Power BI and Copilot Studio products to **Do not allow**.
4. In the Power Platform admin centre, confirm **Manage** > **Tenant settings** disables non-admin trial creation and capacity self-allocation where applicable.

## How to verify

- **Automated**: Read the Power Platform tenant settings and commerce self-service purchase configuration fixture or API response and assert that Power Platform self-service purchases and non-admin trials are disabled.
- **Manual**: Review **Settings** > **Org settings** > **Self-service trials and purchases** in the Microsoft 365 admin centre and verify all Power Platform and Copilot Studio products are blocked.

## References

- [Manage self-service purchases and trials - Microsoft 365 | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/commerce/subscriptions/manage-self-service-purchases-admins)
- [Tenant settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
