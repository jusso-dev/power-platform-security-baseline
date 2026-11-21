---
id: PP-ENV-008
title: Enforce explicit user session and inactivity timeouts
scope: environment
workload: dataverse
severity: medium
recommended_value: Session timeout enabled (maximum 480 minutes / 8 hours) and inactivity timeout enabled (maximum 60 minutes)
rationale: Long-lived idle sessions increase the exposure window on shared or unattended endpoints and delay revocation after access changes.
ism_controls:
  - ISM-0428
  - ISM-1585
essential_eight:
  - Multi-factor authentication
configure_summary: Power Platform admin centre > Environments > Select environment > Settings > Product > Privacy + Security > Enable Session expiration and Inactivity timeout.
verify_summary: Read Dataverse organization entity sessiontimeoutenabled, sessiontimeoutinmins, inactivitytimeoutenabled and inactivitytimeoutinmins via Web API.
assessor_check_id: pp_env_session_timeout_configured
automated: true
sentinel_rules: []
references:
  - title: Manage user session timeout and inactivity timeout - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/user-session-management
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-008: Enforce explicit user session and inactivity timeouts

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Enable **Session expiration** (`sessiontimeoutenabled: true`) with maximum session length of **480 minutes (8 hours)** or less, and enable **Inactivity timeout** (`inactivitytimeoutenabled: true`) with maximum idle duration of **60 minutes** or less (15 to 30 minutes for sensitive environments). Complement this with Microsoft Entra Conditional Access sign-in frequency for canvas apps, which are not governed by Dataverse session timeout alone.
- **Assessor check ID**: `pp_env_session_timeout_configured` (automated)

## Rationale

Without explicit timeouts, model-driven app and Dataverse sessions persist across extended periods. Enforcing bounded session lifetime and inactivity logout reduces exposure from unattended workstations and ensures Conditional Access and role updates take effect promptly.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0428` (locking or terminating idle user sessions) and `ISM-1585` (enforcing cloud session hygiene). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Reinforces [Multi-factor authentication](https://www.cyber.gov.au/essential-eight) by ensuring periodic re-authentication.

## How to configure

1. In the Power Platform admin centre, select the environment > **Settings** > **Product** > **Privacy + Security**.
2. Under **Session expiration**, enable custom session length and set **Maximum session length** to `480` minutes or fewer.
3. Under **Inactivity timeout**, enable inactivity timeout and set **Maximum duration of inactivity** to `60` minutes or fewer with an appropriate warning interval.
4. Select **Save**.

## How to verify

- **Automated**: Query Dataverse Web API `organizations` entity and assert `sessiontimeoutenabled == true`, `sessiontimeoutinmins <= 480`, `inactivitytimeoutenabled == true`, and `inactivitytimeoutinmins <= 60`.
- **Manual**: Review **Settings** > **Product** > **Privacy + Security** for each production environment.

## References

- [Manage user session timeout and inactivity timeout - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/user-session-management)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
