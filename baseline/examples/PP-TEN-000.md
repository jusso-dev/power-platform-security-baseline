---
id: PP-TEN-000
title: Example baseline item (restrict tenant isolation)
scope: tenant
workload: power-platform
severity: high
recommended_value: Tenant isolation enabled with explicit allow-list rules only where justified
rationale: Leaving cross-tenant connector connections unrestricted allows makers to move data from corporate connectors to external Microsoft Entra tenants.
ism_controls:
  - ISM-0263
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Tenant isolation > Enable tenant isolation and maintain an explicit allow-list.
verify_summary: Read tenant isolation policy via the Power Platform Business Application Platform API and verify isolation is enabled.
assessor_check_id: pp_ten_example_isolation
automated: true
sentinel_rules:
  - C1 - Tenant isolation disabled or environment security group changed
references:
  - title: Restrict cross-tenant inbound and outbound access - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/cross-tenant-restrictions
  - title: Information Security Manual | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-000: Example baseline item (restrict tenant isolation)

> Note: This is a schema validation example item. Production baseline items live under `baseline/tenant/`, `baseline/environment/` and `baseline/copilot-studio/`.

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Enable tenant isolation so inbound and outbound Microsoft Entra ID connector connections to external tenants are blocked by default, with documented allow-list exceptions only where business-justified.
- **Assessor check ID**: `pp_ten_example_isolation` (automated)

## Rationale

Without tenant isolation, users can create connections using external Microsoft Entra credentials and move corporate data across tenant boundaries using standard connectors. Enabling tenant isolation enforces a default-deny boundary for Microsoft Entra-based connectors across all environments.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (controlling data transfers across security domains) and `ISM-1585` (restricting unauthorised cloud data flows). Always confirm control wording against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight) by restricting unnecessary external SaaS connectivity.

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Go to **Manage** > **Tenant settings** or **Policies** > **Tenant isolation**.
3. Turn **Restrict cross-tenant connections** on.
4. Add explicit inbound or outbound tenant allow-list rules only for approved partner tenants.

## How to verify

- **Automated**: Query the read-only tenant isolation policy endpoint and confirm `isDisabled` is `false` (isolation enabled) and that any allow-listed tenant IDs match the approved register.
- **Manual**: Review **Policies** > **Tenant isolation** in the Power Platform admin centre and confirm the toggle is enabled and no wildcard `*` rule is present.

## References

- [Restrict cross-tenant inbound and outbound access - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/cross-tenant-restrictions)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
- [Essential Eight | cyber.gov.au](https://www.cyber.gov.au/essential-eight)
