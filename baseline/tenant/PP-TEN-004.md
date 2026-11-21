---
id: PP-TEN-004
title: Enable tenant isolation for cross-tenant connector connections
scope: tenant
workload: power-platform
severity: critical
recommended_value: Tenant isolation enabled (isDisabled false) with no wildcard allow-list rules
rationale: Without tenant isolation, makers can authenticate Microsoft Entra-based connectors against external tenants to exfiltrate organisational data or pull untrusted external data into corporate workflows.
ism_controls:
  - ISM-0263
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Tenant isolation > Enable Restrict cross-tenant connections.
verify_summary: Read tenant isolation policy via the BAP API and verify isDisabled is false and no wildcard '*' tenant rule exists.
assessor_check_id: pp_ten_tenant_isolation_enabled
automated: true
sentinel_rules:
  - C1 - Tenant isolation disabled or environment security group changed
  - Dataverse - Guest user exfiltration following Power Platform defense impairment
references:
  - title: Restrict cross-tenant inbound and outbound access - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/cross-tenant-restrictions
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-004: Enable tenant isolation for cross-tenant connector connections

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Enable **Tenant isolation** (`isDisabled: false`) with default-deny for both inbound and outbound cross-tenant connections. Permit specific external tenant IDs only through documented, time-bound exceptions and never use a wildcard (`*`) rule.
- **Assessor check ID**: `pp_ten_tenant_isolation_enabled` (automated)

## Rationale

Power Platform connectors that use Microsoft Entra ID authentication (such as SharePoint, Exchange Online, Dataverse and Azure Storage) allow users to sign in with accounts from another tenant unless tenant isolation is enabled. A compromised or insider account could build a flow that reads internal SharePoint documents and writes them to an attacker-controlled Microsoft 365 tenant.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (controlling data exports and imports across domains) and `ISM-1585` (enforcing cloud tenant boundaries). Always check the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight) by blocking unauthorised cross-tenant connector channels.

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Navigate to **Security** or **Policies** > **Tenant isolation**.
3. Turn **Tenant isolation** to **On**.
4. Add explicit inbound or outbound rules only for approved partner tenant GUIDs, avoiding any `*` wildcard entry.

## How to verify

- **Automated**: Call the read-only BAP tenant isolation policy endpoint and verify `properties.isDisabled` is `false` and no entry in `properties.allowedTenants` specifies `tenantId == "*"`.
- **Manual**: Open **Tenant isolation** in the Power Platform admin centre, confirm the toggle is **On** and audit the allowed tenants table against the approved register.

## References

- [Restrict cross-tenant inbound and outbound access - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/cross-tenant-restrictions)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
