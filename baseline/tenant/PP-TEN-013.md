---
id: PP-TEN-013
title: Organise Managed Environments into environment groups with baseline rules
scope: tenant
workload: power-platform
severity: medium
recommended_value: At least one environment group configured with published sharing, solution checker and maker rules covering Managed Environments
rationale: Environment groups enforce consistent security rules across multiple environments at once, preventing configuration drift when new environments are provisioned.
ism_controls:
  - ISM-1585
  - ISM-0407
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Manage > Environment groups > Create groups (for example Production, Developer) and publish rules.
verify_summary: Read environment groups via the BAP API and verify at least one group exists with published governance rules.
assessor_check_id: pp_ten_environment_groups_configured
automated: true
sentinel_rules: []
references:
  - title: Environment groups - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/environment-groups
  - title: Managed environments overview - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-013: Organise Managed Environments into environment groups with baseline rules

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Group Managed Environments into structured **Environment groups** (such as Production, Non-Production and Personal Developer) and publish baseline rules for sharing controls, Solution Checker enforcement, usage insights and AI settings.
- **Assessor check ID**: `pp_ten_environment_groups_configured` (automated)

## Rationale

Configuring security controls individually on dozens of environments leads to drift and missed settings on newly created workspaces. Environment groups allow administrators to define a single security posture per tier and enforce it consistently across all member environments.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-1585` (enforcing consistent cloud baseline configurations) and `ISM-0407` (centralising security configuration governance). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Select **Manage** > **Environment groups** > **New group**.
3. Create tier groups (for example **Production**, **Sandbox**, **Personal Developer**).
4. Add Managed Environments to the appropriate group, configure **Rules** (sharing limits, Solution Checker enforcement, AI controls), and select **Publish rules**.

## How to verify

- **Automated**: Call the read-only BAP environment groups endpoint and verify at least one environment group exists with published rules.
- **Manual**: Review **Manage** > **Environment groups** in the Power Platform admin centre and confirm all Managed Environments belong to an appropriate group with published rules.

## References

- [Environment groups - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/environment-groups)
- [Managed environments overview - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
