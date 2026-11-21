---
id: PP-ENV-002
title: Enable Dataverse auditing and user access logging in production environments
scope: environment
workload: dataverse
severity: critical
recommended_value: isauditenabled and isuseraccessauditenabled both set to true on all production Dataverse environments
rationale: Without Dataverse auditing and user access logging enabled, record deletions, security role changes, organisation setting changes and sign-ins are never emitted to Purview or Microsoft Sentinel DataverseActivity.
ism_controls:
  - ISM-0580
  - ISM-0585
  - ISM-1228
essential_eight: []
configure_summary: Power Platform admin centre > Environments > Select environment > Settings > Audit and logs > Audit settings > Enable Start auditing and Log access.
verify_summary: Read Dataverse organization entity via Web API GET /api/data/v9.2/organizations and verify isauditenabled and isuseraccessauditenabled are true.
assessor_check_id: pp_env_dataverse_auditing_enabled
automated: true
sentinel_rules:
  - Dataverse - Audit logging disabled
  - Dataverse - Audit log data deletion
  - Dataverse - Mass export of records to Excel
  - Dataverse - Mass deletion of records
  - Dataverse - Suspicious security role modifications
references:
  - title: Manage Dataverse auditing - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing
  - title: Connect Power Platform and Dynamics 365 CE to Microsoft Sentinel | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution
  - title: DataverseActivity table reference | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dataverseactivity
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-002: Enable Dataverse auditing and user access logging in production environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Enable **Start auditing** (`isauditenabled: true`) and **Log access** (`isuseraccessauditenabled: true`) on every production environment with a Dataverse database, and import the Microsoft Sentinel Audit Settings managed solution so key security tables (and custom sensitive tables plus `bot`/`botcomponent` where Copilot Studio is used) emit events to `DataverseActivity`.
- **Assessor check ID**: `pp_env_dataverse_auditing_enabled` (automated)

## Rationale

Dataverse auditing is turned off by default on new environments. Without global auditing and access logging enabled, Microsoft Sentinel's Microsoft Dataverse connector (`DataverseActivity`) receives no sign-in, security role modification, export-to-Excel or record deletion telemetry, leaving high-impact insider and compromise scenarios invisible. See [docs/research/verification.md](../../docs/research/verification.md) for Sentinel connector details and why `DataverseActivity` replaces the legacy `Dynamics365Activity` table.

## ISM and Essential Eight mapping

- **ISM controls**: Directly supports `ISM-0580` (event logging policy), `ISM-0585` (centralised security log collection) and `ISM-1228` (logging administrative and user access events). Verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. Open the Power Platform admin centre > **Manage** > **Environments** > select the production environment.
2. Go to **Settings** > **Audit and logs** > **Audit settings**.
3. Turn on **Start auditing** and **Log access**, then select **Save**.
4. Import the **Audit Settings** solution from the [Microsoft Business Applications Sentinel solution](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution) and enable auditing on custom sensitive tables.

## How to verify

- **Automated**: Call the read-only Dataverse Web API (`GET <instanceUrl>/api/data/v9.2/organizations?$select=isauditenabled,isuseraccessauditenabled`) on each production environment and assert both `isauditenabled` and `isuseraccessauditenabled` are `true`.
- **Manual**: Review **Settings** > **Audit and logs** > **Audit settings** in the Power Platform admin centre and confirm rows are landing in Microsoft Sentinel `DataverseActivity`.

## References

- [Manage Dataverse auditing - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing)
- [Connect Power Platform and Dynamics 365 CE to Microsoft Sentinel | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution)
- [DataverseActivity table reference | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dataverseactivity)
- [Research verification record](../../docs/research/verification.md)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
