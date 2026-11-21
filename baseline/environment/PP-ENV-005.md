---
id: PP-ENV-005
title: Configure explicit Dataverse audit log retention period
scope: environment
workload: dataverse
severity: medium
recommended_value: Dataverse audit retention set to at least 90 days (or aligned with organisational retention policy and Sentinel archival)
rationale: Setting an explicit audit retention period ensures local forensic evidence remains available during investigations while preventing unbounded log capacity exhaustion.
ism_controls:
  - ISM-0585
  - ISM-0859
essential_eight: []
configure_summary: Power Platform admin centre > Environments > Select environment > Settings > Audit and logs > Audit settings > Set Retain these logs for.
verify_summary: Read Dataverse organization entity auditretentionperiodv2 via Web API and verify retention is configured to at least 90 days.
assessor_check_id: pp_env_audit_retention_configured
automated: true
sentinel_rules:
  - Dataverse - Audit log data deletion
  - Dataverse - Audit logging disabled
references:
  - title: Manage Dataverse auditing - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing
  - title: Dataverse storage capacity - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-005: Configure explicit Dataverse audit log retention period

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Configure an explicit Dataverse audit retention period (`auditretentionperiodv2`) of at least **90 days** (or longer where required by agency records policy, complemented by long-term retention in Microsoft Sentinel analytics/data lake tiers).
- **Assessor check ID**: `pp_env_audit_retention_configured` (automated)

## Rationale

Short retention windows can purge forensic records before an incident is detected and investigated, while unmonitored "Forever" retention can exhaust Dataverse Log capacity. Coordinating Dataverse retention with Microsoft Sentinel workspace retention ensures investigators have complete telemetry without operational surprises.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0585` (retaining event logs for security investigations) and `ISM-0859` (preserving audit trails according to retention requirements). Verify against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. In the Power Platform admin centre, open the production environment > **Settings** > **Audit and logs** > **Audit settings**.
2. Set **Retain these logs for** to **90 days** or greater (for example **1 year** or custom period matching agency policy).
3. Verify Microsoft Sentinel retention on the `DataverseActivity` table matches long-term archival requirements.

## How to verify

- **Automated**: Read `auditretentionperiodv2` from the Dataverse Web API `organizations` entity and verify it is configured to at least 90 days (or `-1` where "Forever" is explicitly approved alongside capacity monitoring).
- **Manual**: Inspect **Audit settings** in the Power Platform admin centre and cross-check `DataverseActivity` table retention in Microsoft Sentinel.

## References

- [Manage Dataverse auditing - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing)
- [Dataverse storage capacity - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage)
- [Research verification record](../../docs/research/verification.md)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
