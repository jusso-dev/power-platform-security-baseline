---
id: PP-TEN-007
title: Enable default environment routing for new makers
scope: tenant
workload: power-platform
severity: medium
recommended_value: Default environment routing enabled so makers are routed to personal developer environments
rationale: Routing new makers into isolated personal developer environments reduces sprawl and blast radius inside the shared default environment.
ism_controls:
  - ISM-1585
  - ISM-0407
essential_eight: []
configure_summary: Power Platform admin centre > Settings > Tenant settings > Default environment routing > Enable.
verify_summary: Read tenant settings via the BAP API and check whether default environment routing is enabled.
assessor_check_id: pp_ten_default_env_routing
automated: true
sentinel_rules: []
references:
  - title: Enable default environment routing - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/default-environment-routing
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-007: Enable default environment routing for new makers

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Enable **Default environment routing** so makers are automatically directed to individual, governed developer environments placed in an environment group with strict DLP and sharing rules, rather than building in the shared default environment.
- **Assessor check ID**: `pp_ten_default_env_routing` (automated)

## Rationale

The shared default environment accumulates unmanaged personal productivity apps and flows visible across broad user populations. Default environment routing isolates individual maker experimentation into personal developer environments that can be governed by environment group rules and cleaned up automatically when users leave.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-1585` (segregating development and production cloud workloads) and `ISM-0407` (limiting user privileges in shared environments). Check the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Go to **Manage** > **Tenant settings** > **Default environment routing**.
3. Turn **Create personal developer environments for makers** to **On**.
4. Select the target environment group for newly routed developer environments and save.

## How to verify

- **Automated**: Read tenant settings via the read-only BAP API and confirm `powerPlatform.governance.enableDefaultEnvironmentRouting` (or equivalent environment routing flag) is `true`.
- **Manual**: Open **Manage** > **Tenant settings** > **Default environment routing** in the Power Platform admin centre and confirm routing is enabled.

## References

- [Enable default environment routing - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/default-environment-routing)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
