---
id: PP-ENV-006
title: Enable Dataverse IP firewall on sensitive Managed Environments
scope: environment
workload: dataverse
severity: high
recommended_value: IP firewall enabled in Enforce mode with approved corporate egress CIDR ranges on sensitive production Managed Environments
rationale: IP firewall blocks Dataverse API and web requests originating outside trusted corporate or VPN IP ranges, mitigating stolen token replay from unmanaged networks.
ism_controls:
  - ISM-1585
  - ISM-1405
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Environments > Select Managed Environment > Settings > Product > Privacy + Security > Enable IP address based firewall rule.
verify_summary: Read Dataverse organization entity IP firewall properties via Web API and verify enableipbasedfirewallrule is true, ipbasedfirewallrulemode is Enforce and allowediprangeforfirewall is non-empty.
assessor_check_id: pp_env_ip_firewall_enabled
automated: true
sentinel_rules:
  - Dataverse - Login from IP not in the allow list
  - Dataverse - Login from IP in the block list
references:
  - title: IP firewall in Power Platform environments - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/ip-firewall
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-006: Enable Dataverse IP firewall on sensitive Managed Environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Enable the **IP address based firewall rule** on sensitive Managed Environments in **Enforce** mode (after initial **Audit only** validation), restricted to approved corporate egress and VPN CIDR ranges. Avoid `0.0.0.0/0`.
- **Assessor check ID**: `pp_env_ip_firewall_enabled` (automated)

## Rationale

Unlike Conditional Access (which evaluates at token issuance), Dataverse IP firewall evaluates the source IP address on every live Dataverse request in real time. Even if an attacker steals an active bearer token or session cookie, requests from outside approved IP ranges are rejected.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-1585` (network access restrictions for cloud services) and `ISM-1405` (restricting access from untrusted networks). Verify against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Confirm the environment is a Managed Environment and inventory all legitimate egress CIDR ranges (corporate proxies, VPNs, approved Azure NAT gateways).
2. In the Power Platform admin centre, go to **Environments** > select environment > **Settings** > **Product** > **Privacy + Security**.
3. Turn **Enable IP address based firewall rule** to **On**, enter approved CIDR ranges, test in **Audit only** mode, then switch to **Enforce** mode.

## How to verify

- **Automated**: Read Dataverse organization settings via the read-only Web API and assert `enableipbasedfirewallrule` is `true`, `ipbasedfirewallrulemode` is `"Enforce"` (not `"AuditOnly"`), and `allowediprangeforfirewall` is non-empty and excludes `0.0.0.0/0`.
- **Manual**: Review **Settings** > **Product** > **Privacy + Security** > **IP firewall** in the Power Platform admin centre.

## References

- [IP firewall in Power Platform environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/ip-firewall)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
