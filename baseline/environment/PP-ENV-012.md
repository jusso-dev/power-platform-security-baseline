---
id: PP-ENV-012
title: Enable Microsoft Customer Lockbox for Managed Environments
scope: environment
workload: dataverse
severity: medium
recommended_value: Customer Lockbox enabled at tenant level and active across Managed Environments holding sensitive data
rationale: Customer Lockbox ensures Microsoft support engineers cannot access customer Dataverse data during troubleshooting without explicit, time-limited approval from an organisational administrator.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - Restrict administrative privileges
configure_summary: Power Platform admin centre > Manage > Tenant settings > Customer Lockbox > Enable for Managed Environments.
verify_summary: Read tenant/environment lockbox configuration via BAP API and assert isLockboxEnabled is true for Managed Environments.
assessor_check_id: pp_env_customer_lockbox_enabled
automated: true
sentinel_rules: []
references:
  - title: Securely access customer data using Customer Lockbox in Power Platform and Dynamics 365 | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/about-lockbox
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-012: Enable Microsoft Customer Lockbox for Managed Environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Enable **Customer Lockbox** (`enableCustomerLockbox: true`) across all production Managed Environments so any Microsoft support request requiring customer data access triggers an auditable approval workflow reviewed by a Power Platform Administrator or Global Administrator.
- **Assessor check ID**: `pp_env_customer_lockbox_enabled` (automated)

## Rationale

In rare support escalations, Microsoft engineers may request temporary access to customer Dataverse databases. Enabling Customer Lockbox puts the organisation in the approval path and records every approval, rejection and access window in `PowerPlatformAdminActivity`.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (explicit authorisation of third-party privileged access) and `ISM-1585` (governing cloud provider support access). Confirm against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Ensure target production environments are enabled as Managed Environments.
2. Open the Power Platform admin centre > **Manage** > **Tenant settings** > **Customer Lockbox**.
3. Turn **Enable** to **On** and select **Save**.
4. Document the internal approval procedure and SLA for lockbox requests.

## How to verify

- **Automated**: Read tenant lockbox settings and Managed Environment status via the read-only BAP API and verify Customer Lockbox is enabled and enforced on production Managed Environments.
- **Manual**: Confirm **Customer Lockbox** is **On** in **Manage** > **Tenant settings** and review **Lockbox requests** history.

## References

- [Securely access customer data using Customer Lockbox in Power Platform and Dynamics 365 | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/about-lockbox)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
