---
id: PP-ENV-010
title: Enforce Solution Checker in Block mode on production Managed Environments
scope: environment
workload: power-platform
severity: medium
recommended_value: Solution Checker enforcement set to Block on production Managed Environments (Warn minimum on sandbox)
rationale: Blocking solution imports that fail critical static security and reliability checks prevents insecure plug-ins, cross-site scripting risks and unvalidated web resources from reaching production.
ism_controls:
  - ISM-0400
  - ISM-1405
essential_eight:
  - Application control
configure_summary: Power Platform admin centre > Environments > Select Managed Environment > Edit Managed Environments > Solution checker > Block.
verify_summary: Read Managed Environment governanceConfiguration.settings.extendedSettings.solutionCheckerMode via BAP API and assert it equals Block on production environments.
assessor_check_id: pp_env_solution_checker_block
automated: true
sentinel_rules: []
references:
  - title: Solution checker enforcement in Managed Environments - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-solution-checker
  - title: Power Platform checker API overview | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/alm/checker-api/overview
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-010: Enforce Solution Checker in Block mode on production Managed Environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Power Platform
- **Recommended value**: Set **Solution checker** enforcement to **Block** (`solutionCheckerMode: "Block"`) on all production Managed Environments, and at least **Warn** (`"Warn"`) on sandbox and test environments, with email notifications enabled for security and platform administrators.
- **Assessor check ID**: `pp_env_solution_checker_block` (automated)

## Rationale

Low-code solutions can bundle custom JavaScript web resources, .NET plug-ins and flows that introduce injection, unsafe API usage or security misconfigurations. Enforcing Solution Checker in **Block** mode provides an automated static analysis gate prior to production deployment.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0400` (secure software development and pre-deployment security testing) and `ISM-1405` (preventing insecure code execution). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Aligns with [Application control](https://www.cyber.gov.au/essential-eight) by blocking unvalidated solution packages from deploying into production.

## How to configure

1. In the Power Platform admin centre, select the production Managed Environment (or its environment group).
2. Open **Edit Managed Environments** > **Solution checker**.
3. Set validation level to **Block** and enable **Send emails only when a solution is blocked**.
4. Save changes.

## How to verify

- **Automated**: Read `properties.governanceConfiguration.settings.extendedSettings.solutionCheckerMode` from the read-only BAP environments API and assert `"Block"` for production environments (`"Warn"` or `"Block"` for non-production).
- **Manual**: Review **Solution checker** settings under **Edit Managed Environments** or **Environment groups** > **Rules**.

## References

- [Solution checker enforcement in Managed Environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-solution-checker)
- [Power Platform checker API overview | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/alm/checker-api/overview)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
