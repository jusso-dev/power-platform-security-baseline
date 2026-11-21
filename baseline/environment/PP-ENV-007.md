---
id: PP-ENV-007
title: Enable IP address-based cookie binding in Dataverse
scope: environment
workload: dataverse
severity: high
recommended_value: enableipbasedcookiebinding set to true on all Dataverse environments
rationale: Cookie binding ties Dataverse session cookies to the client IP address that established the session, blocking cookie replay attacks from attacker infrastructure.
ism_controls:
  - ISM-1585
  - ISM-1175
essential_eight:
  - Multi-factor authentication
configure_summary: Power Platform admin centre > Environments > Select environment > Settings > Product > Privacy + Security > Enable IP address based cookie binding.
verify_summary: Read Dataverse organization entity via Web API and verify enableipbasedcookiebinding is true.
assessor_check_id: pp_env_cookie_binding_enabled
automated: true
sentinel_rules:
  - Dataverse - Unusual sign-in following disabled IP address-based cookie binding protection
references:
  - title: Enable IP address-based cookie binding - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/block-cookie-replay-attack
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-007: Enable IP address-based cookie binding in Dataverse

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Enable **IP address-based cookie binding** (`enableipbasedcookiebinding: true`) on all production Dataverse environments.
- **Assessor check ID**: `pp_env_cookie_binding_enabled` (automated)

## Rationale

Adversary-in-the-middle phishing and infostealer malware frequently target session cookies to bypass MFA. IP address-based cookie binding embeds the client IP address into Dataverse session cookies (`CrmOwinAuth`) and rejects requests if the cookie is replayed from a different IP address, forcing re-authentication.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-1585` (protecting cloud application sessions) and `ISM-1175` (defending authenticated sessions against hijack). Check the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Reinforces [Multi-factor authentication](https://www.cyber.gov.au/essential-eight) by reducing session cookie replay risk after MFA succeeds.

## How to configure

1. In the Power Platform admin centre, select the environment > **Settings** > **Product** > **Privacy + Security**.
2. Turn **Enable IP address based cookie binding** to **On**.
3. Select **Save**.

## How to verify

- **Automated**: Query the read-only Dataverse Web API `organizations` entity and assert `enableipbasedcookiebinding` is `true`.
- **Manual**: Confirm **Enable IP address based cookie binding** is **On** under **Settings** > **Product** > **Privacy + Security**.

## References

- [Enable IP address-based cookie binding - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/block-cookie-replay-attack)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
