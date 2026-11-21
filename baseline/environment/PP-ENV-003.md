---
id: PP-ENV-003
title: Enable Dataverse read auditing on sensitive production environments
scope: environment
workload: dataverse
severity: medium
recommended_value: isreadauditenabled set to true on environments designated as sensitive or holding regulated data
rationale: Read auditing captures Retrieve and RetrieveMultiple operations required by Microsoft Sentinel rules that detect bulk record exfiltration, suspicious Web API scraping and TDS endpoint queries.
ism_controls:
  - ISM-0580
  - ISM-0585
essential_eight: []
configure_summary: Power Platform admin centre > Environments > Select sensitive environment > Settings > Audit and logs > Audit settings > Enable Read logs.
verify_summary: Read Dataverse organization entity via Web API GET /api/data/v9.2/organizations and verify isreadauditenabled is true on environments tagged or designated as sensitive.
assessor_check_id: pp_env_dataverse_read_auditing
automated: true
sentinel_rules:
  - Dataverse - User bulk retrieval outside normal activity
  - Dataverse - Suspicious use of TDS endpoint
  - Dataverse - Suspicious use of Web API
  - C8 - Dataverse export or bulk read by a guest
references:
  - title: Manage Dataverse auditing - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing
  - title: Security content reference for Power Platform and Dynamics 365 CE | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/sentinel/business-applications/power-platform-solution-security-content
  - title: DataverseActivity table reference | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dataverseactivity
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-003: Enable Dataverse read auditing on sensitive production environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Enable **Read logs** (`isreadauditenabled: true`) on production environments storing sensitive or regulated records. Because read logging generates high volume and consumes Dataverse Log capacity and Sentinel ingestion, apply it selectively to sensitive environments and consider a Data Collection Rule (DCR) transformation to filter noisy service accounts where appropriate.
- **Assessor check ID**: `pp_env_dataverse_read_auditing` (automated)

## Rationale

Write-only auditing detects deletions and updates but cannot detect silent data theft via the Dataverse Web API, Tabular Data Stream (TDS) SQL endpoint or repeated `RetrieveMultiple` queries. Microsoft Sentinel rules for bulk retrieval, suspicious Web API use and TDS abuse depend on read logs flowing into `DataverseActivity` (see [docs/research/verification.md](../../docs/research/verification.md)).

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0580` (logging access to sensitive data) and `ISM-0585` (detecting unauthorised data retrieval via centralised SIEM analysis). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. Confirm sufficient Dataverse Log capacity and Sentinel ingestion budget.
2. In the Power Platform admin centre, open the sensitive production environment > **Settings** > **Audit and logs** > **Audit settings**.
3. Enable **Read logs** (`isreadauditenabled`) and select **Save**.
4. Ensure sensitive tables have **Single record auditing** and **Multiple record auditing** enabled and published.

## How to verify

- **Automated**: Query the read-only Dataverse Web API (`GET <instanceUrl>/api/data/v9.2/organizations?$select=isreadauditenabled`) for environments marked sensitive and assert `isreadauditenabled` is `true`.
- **Manual**: Verify **Read logs** is checked in **Audit settings** and confirm `RetrieveMultiple` events appear in Microsoft Sentinel `DataverseActivity`.

## References

- [Manage Dataverse auditing - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing)
- [Security content reference for Power Platform and Dynamics 365 CE | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/power-platform-solution-security-content)
- [DataverseActivity table reference | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dataverseactivity)
- [Research verification record](../../docs/research/verification.md)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
