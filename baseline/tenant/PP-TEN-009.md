---
id: PP-TEN-009
title: Restrict guest user access and external sharing in Power Platform
scope: tenant
workload: power-platform
severity: high
recommended_value: Guest makers disabled in Power Platform tenant settings and Microsoft Entra external collaboration restricted to approved domains
rationale: Unrestricted guest access lets external accounts discover, run or co-author internal apps and export Dataverse records outside organisational control.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - Multi-factor authentication
  - Restrict administrative privileges
configure_summary: Disable guest makers in Power Platform tenant settings and restrict guest invitations and object visibility in Microsoft Entra External Collaboration settings.
verify_summary: Read Power Platform tenant settings (walkMeOptIn/guest maker flags) and Microsoft Graph authorizationPolicy to confirm guest restrictions.
assessor_check_id: pp_ten_guest_access_restricted
automated: true
sentinel_rules:
  - Power Apps - Bulk sharing of Power Apps to newly created guest users
  - C5 - Flow shared with a guest or external account
  - C8 - Dataverse export or bulk read by a guest
references:
  - title: Tenant settings - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings
  - title: Configure external collaboration settings - Microsoft Entra | Microsoft Learn
    url: https://learn.microsoft.com/en-us/entra/external-id/external-collaboration-settings-configure
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-009: Restrict guest user access and external sharing in Power Platform

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Disable guest maker capabilities in Power Platform tenant settings (`powerPlatform.powerApps.disableShareWithEveryone` enabled where applicable and guest makers blocked) and configure Microsoft Entra External Collaboration settings so only administrators or the Guest Inviter role can invite guests (`allowInvitesFrom: adminsAndGuestInviters` or `none`) with restricted guest directory visibility.
- **Assessor check ID**: `pp_ten_guest_access_restricted` (automated)

## Rationale

Guest accounts can be invited by regular users under default Microsoft Entra settings and then granted access to Power Apps, flows or Dataverse tables. Combined with overly broad permissions, guest access is a common path for unauthorised external data access and exfiltration.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (enforcing least privilege for external accounts) and `ISM-1585` (controlling external access to cloud data). Always check the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Multi-factor authentication](https://www.cyber.gov.au/essential-eight) (when paired with Conditional Access MFA for guests) and [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight).

## How to configure

1. In the Power Platform admin centre, go to **Manage** > **Tenant settings** and restrict guest maker permissions and tenant-wide sharing where available.
2. In the Microsoft Entra admin centre, go to **External Identities** > **External collaboration settings**.
3. Set **Guest user access** to the most restrictive option appropriate for your organisation and set **Guest invite settings** to **Only users assigned to specific admin roles can invite guest users** (or **No one**).
4. Restrict collaboration domains to an explicit allow-list where external collaboration is required.

## How to verify

- **Automated**: Read Power Platform tenant settings and Microsoft Graph `GET https://graph.microsoft.com/v1.0/policies/authorizationPolicy` to verify `allowInvitesFrom` is `adminsAndGuestInviters` or `none` and guest access is restricted.
- **Manual**: Review Power Platform tenant settings and Microsoft Entra External collaboration settings.

## References

- [Tenant settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings)
- [Configure external collaboration settings - Microsoft Entra | Microsoft Learn](https://learn.microsoft.com/en-us/entra/external-id/external-collaboration-settings-configure)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
