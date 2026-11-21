---
id: PP-TEN-005
title: Apply a restrictive Data Loss Prevention policy to the default environment
scope: tenant
workload: power-platform
severity: critical
recommended_value: At least one active DLP policy covers the default environment with non-Microsoft and high-risk connectors blocked
rationale: Every licensed user has maker access in the default environment; without a restrictive DLP policy, any user can combine corporate Microsoft 365 connectors with external services.
ism_controls:
  - ISM-0263
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Data policies > Create a policy covering the default environment (or all environments) that restricts connectors to approved Microsoft 365 services.
verify_summary: List DLP policies via the Power Platform BAP API and verify at least one policy applies to the default environment with a non-empty Blocked connector group.
assessor_check_id: pp_ten_default_env_dlp_policy
automated: true
sentinel_rules:
  - Power Platform - DLP policy updated or removed
  - C2 - Data policy changed by a non-approved admin
references:
  - title: Data policies - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-005: Apply a restrictive Data Loss Prevention policy to the default environment

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Assign a dedicated restrictive Data Loss Prevention (DLP) policy to the default environment (or enforce an all-environments baseline policy) that permits only essential internal productivity connectors in the **Business** group, sets the default group for new connectors to **Blocked**, and places all third-party, consumer and unapproved connectors in **Blocked**.
- **Assessor check ID**: `pp_ten_default_env_dlp_policy` (automated)

## Rationale

The default environment cannot be deleted and grants maker permissions to every user in the tenant. Leaving the default environment without a restrictive DLP policy enables any employee or compromised account to create flows or apps that copy SharePoint, OneDrive or Exchange data to external storage or email services.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (preventing unauthorised data export) and `ISM-1585` (enforcing cloud data loss prevention controls). Confirm against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Go to **Policies** > **Data policies** > **New policy**.
3. Move approved internal connectors (such as SharePoint, Office 365 Users, Approvals) into **Business** and move all other blockable connectors into **Blocked**.
4. Set **Default group for new connectors** to **Blocked**.
5. Scope the policy to **Add multiple environments** (selecting the default environment) or **Add all environments**.

## How to verify

- **Automated**: Read environments and DLP policies via read-only BAP endpoints, identify the default environment (`isDefault: true`), and verify at least one DLP policy scopes it (either `AllEnvironments`, `OnlyEnvironments` including the default environment ID, or `ExceptEnvironments` not excluding it) with `defaultConnectorClassification == "Blocked"`.
- **Manual**: In **Policies** > **Data policies**, confirm a restrictive policy applies to the default environment and sets new connectors to **Blocked**.

## References

- [Data policies - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
