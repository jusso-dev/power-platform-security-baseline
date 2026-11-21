---
id: PP-ENV-009
title: Enforce canvas app and solution flow sharing limits in Managed Environments
scope: environment
workload: power-apps
severity: high
recommended_value: Managed Environment sharing limits exclude sharing with security groups (or cap total recipients to 20 or fewer) in default and personal developer environments
rationale: Unrestricted app sharing lets a single maker broadcast a phishing, data-harvesting or misconfigured canvas app to the entire tenant.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Environments > Select Managed Environment > Edit Managed Environments > Limit sharing.
verify_summary: Read Managed Environment governanceConfiguration.settings.extendedSettings via BAP API and assert excludeSharingWithSecurityGroups is true or maxLimitUserSharing is set to 20 or fewer.
assessor_check_id: pp_env_sharing_limits_configured
automated: true
sentinel_rules:
  - Power Apps - Bulk sharing of Power Apps to newly created guest users
  - C6 - App shared with Everyone or 20+ principals in an hour
references:
  - title: Limit sharing in Managed Environments - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-sharing-limits
  - title: Managed environments overview - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-009: Enforce canvas app and solution flow sharing limits in Managed Environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Power Apps
- **Recommended value**: On Managed Environments (especially default, developer and citizen-maker environments), configure **Limit sharing** to **Exclude sharing with security groups** (`excludeSharingWithSecurityGroups: true`) and cap **Limit total individuals who can be shared to** at **20** or fewer (or `1` in personal developer environments). Production application environments that legitimately distribute apps via curated security groups must still restrict editor sharing and govern distribution through ALM.
- **Assessor check ID**: `pp_env_sharing_limits_configured` (automated)

## Rationale

Without sharing limits, makers can share canvas apps or solution flows with "Everyone" or large dynamic security groups. If a maker account is compromised or embeds unsafe connectors, tenant-wide sharing amplifies impact immediately.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (enforcing need-to-know access) and `ISM-1585` (preventing uncontrolled cloud resource sharing). Confirm against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. In the Power Platform admin centre, open **Manage** > **Environments** (or **Environment groups** > **Rules**).
2. Select the Managed Environment and choose **Edit Managed Environments**.
3. Under **Limit sharing**, enable **Exclude sharing with security groups** and set **Limit total individuals who can be shared to** to `20` (or stricter for personal developer environments).
4. Save changes.

## How to verify

- **Automated**: Read `properties.governanceConfiguration.settings.extendedSettings` via the BAP environments API and verify `excludeSharingWithSecurityGroups` is `"true"` (or `true`) and `maxLimitUserSharing` is an integer between `1` and `20` (unless the environment is explicitly tagged for governed group distribution).
- **Manual**: Review **Limit sharing** under **Edit Managed Environments** or the assigned environment group rule.

## References

- [Limit sharing in Managed Environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-sharing-limits)
- [Managed environments overview - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
