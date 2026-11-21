---
id: PP-CS-007
title: Restrict Copilot Studio agent sharing limits in Managed Environments
scope: environment
workload: copilot-studio
severity: high
recommended_value: Managed Environment agent sharing limits restrict viewer and editor sharing and prohibit sharing agents with Everyone or unrestricted security groups
rationale: Unrestricted agent sharing allows untested or malicious agents to reach the entire organisation, amplifying prompt-injection, misinformation and data leakage risks.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Environments (or Environment groups) > Managed Environment settings > Limit sharing for Copilot Studio agents.
verify_summary: Read Managed Environment governanceConfiguration.settings.extendedSettings via BAP API and confirm agent sharing limits are enforced.
assessor_check_id: pp_cs_agent_sharing_limits
automated: true
sentinel_rules: []
references:
  - title: Share an agent with other users - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-share-bots
  - title: Limit sharing in Managed Environments - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-sharing-limits
  - title: Engaging with artificial intelligence | cyber.gov.au
    url: https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-007: Restrict Copilot Studio agent sharing limits in Managed Environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Copilot Studio
- **Recommended value**: In Managed Environments (and environment group rules), enable **Sharing limits** for Copilot Studio agents to prohibit sharing with security groups (in default/developer environments), restrict editor sharing, and cap individual viewer sharing (maximum 20 viewers unless promoted through formal production ALM review).
- **Assessor check ID**: `pp_cs_agent_sharing_limits` (automated)

## Rationale

An unreviewed citizen-built agent shared tenant-wide can mislead staff, leak grounded data via misconfigured connections or provide an attacker-controlled interaction channel if a maker account is compromised. Managed Environment sharing limits enforce a hard cap on distribution outside formal release governance.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (need-to-know access) and `ISM-1585` (governing cloud AI distribution). Aligns with ASD's [Engaging with artificial intelligence](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Open the Power Platform admin centre > **Manage** > **Environments** (or **Environment groups** > **Rules**).
2. Select **Edit Managed Environments** > **Limit sharing**.
3. Configure **Copilot Studio agents** sharing limits to disallow editor sharing where unnecessary, exclude security group sharing in non-production/default environments, and set a viewer cap.
4. Save and publish rules.

## How to verify

- **Automated**: Read `properties.governanceConfiguration.settings.extendedSettings` via the BAP environments API and confirm agent sharing restrictions (or environment sharing limits `excludeSharingWithSecurityGroups` / `maxLimitUserSharing` / `disableAgentSharingWithEditors`) are active on Managed Environments.
- **Manual**: Review **Limit sharing** in **Edit Managed Environments** and inspect shared users on published agents in Copilot Studio.

## References

- [Share an agent with other users - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-share-bots)
- [Limit sharing in Managed Environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-sharing-limits)
- [Engaging with artificial intelligence | cyber.gov.au](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
