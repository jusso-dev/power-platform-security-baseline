---
id: PP-TEN-010
title: Restrict Power Platform and Dynamics 365 Administrator roles with PIM
scope: tenant
workload: power-platform
severity: critical
recommended_value: Fewer than 5 permanent Power Platform or Dynamics 365 Administrators; assignments governed via Microsoft Entra PIM just-in-time activation with MFA
rationale: Standing tenant-wide Power Platform Administrator privileges allow silent self-elevation to System Administrator in any Dataverse environment and modification of DLP and tenant isolation policies.
ism_controls:
  - ISM-0445
  - ISM-1175
  - ISM-1507
essential_eight:
  - Restrict administrative privileges
  - Multi-factor authentication
configure_summary: Microsoft Entra admin centre > Identity Governance > Privileged Identity Management > Convert standing Power Platform and Dynamics 365 Administrator assignments to eligible with MFA and approval.
verify_summary: Query Microsoft Graph directory role assignments for Power Platform Administrator and Dynamics 365 Administrator and confirm minimal permanent assignments.
assessor_check_id: pp_ten_admin_role_least_privilege
automated: true
sentinel_rules:
  - Power Platform - Account added to privileged Microsoft Entra roles
  - C7 - Admin self-elevation or System Administrator granted
references:
  - title: Use service admin roles to manage your tenant - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/use-service-admin-role-manage-tenant
  - title: Configure Microsoft Entra role settings in PIM | Microsoft Learn
    url: https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-010: Restrict Power Platform and Dynamics 365 Administrator roles with PIM

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Maintain zero standing (or strictly minimised, fewer than 5 total including break-glass exceptions) active assignments to the **Power Platform Administrator** and **Dynamics 365 Administrator** Microsoft Entra roles. Require just-in-time activation via Microsoft Entra Privileged Identity Management (PIM) with phishing-resistant MFA, justification and ticket tracking.
- **Assessor check ID**: `pp_ten_admin_role_least_privilege` (automated)

## Rationale

Power Platform Administrators can disable tenant isolation, weaken DLP policies, and elevate themselves to System Administrator in any environment (`ApplyAdminRole`). Compromising a standing administrator account grants full control over every Dataverse database and connector in the tenant.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0445` (restricting privileged access to authorised administrators), `ISM-1175` (minimising standing privileges) and `ISM-1507` (enforcing multi-factor authentication for privileged operations). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Directly supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight) and [Multi-factor authentication](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Sign in to the Microsoft Entra admin centre as a Privileged Role Administrator.
2. Open **Identity Governance** > **Privileged Identity Management** > **Microsoft Entra roles**.
3. Locate **Power Platform Administrator** and **Dynamics 365 Administrator**.
4. Convert active user assignments to **Eligible**, require MFA and justification on activation, limit maximum activation duration (for example 4 hours), and remove unnecessary members.

## How to verify

- **Automated**: Call Microsoft Graph read-only role assignment endpoints (`GET https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments`) filtered to Power Platform Administrator (`11648597-926c-4cf3-9c36-bcebb0ba8dcc`) and Dynamics 365 Administrator (`44367163-eba1-44c3-98af-f5787879f96a`), verifying active permanent counts remain within the configured threshold (default maximum 2 active assignments).
- **Manual**: Review active and eligible role assignments in Microsoft Entra PIM.

## References

- [Use service admin roles to manage your tenant - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/use-service-admin-role-manage-tenant)
- [Configure Microsoft Entra role settings in PIM | Microsoft Learn](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
