---
id: PP-TEN-014
title: Enable Microsoft Purview auditing and Sentinel Business Applications ingestion
scope: tenant
workload: power-platform
severity: critical
recommended_value: Microsoft Purview unified audit logging enabled and Microsoft Business Applications Sentinel solution (3.2.5+) connected for PowerPlatformAdminActivity, PowerAutomateActivity and DataverseActivity
rationale: All current Microsoft Sentinel Power Platform CCF connectors poll the Office 365 Management API through Microsoft Purview Audit; without Purview auditing enabled, zero Power Platform admin, flow or Dataverse security telemetry reaches the SOC.
ism_controls:
  - ISM-0580
  - ISM-0585
  - ISM-1228
essential_eight: []
configure_summary: Activate Audit in the Microsoft Purview portal and deploy the Microsoft Business Applications solution (3.2.5+) in Microsoft Sentinel.
verify_summary: Manual verification in Microsoft Purview Audit and Microsoft Sentinel (Defender portal) confirming active log ingestion across PowerPlatformAdminActivity, PowerAutomateActivity and DataverseActivity.
assessor_check_id: pp_ten_purview_audit_enabled
automated: false
sentinel_rules:
  - Power Platform - DLP policy updated or removed
  - Power Platform - Connector added to a sensitive environment
  - C1 - Tenant isolation disabled or environment security group changed
references:
  - title: Power Platform activity logging in Microsoft Purview | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/activity-logging-auditing/activity-logs-overview
  - title: Connect Power Platform and Dynamics 365 CE to Microsoft Sentinel | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution
  - title: Learn about auditing solutions in Microsoft Purview | Microsoft Learn
    url: https://learn.microsoft.com/en-us/purview/audit-solutions-overview
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-014: Enable Microsoft Purview auditing and Sentinel Business Applications ingestion

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Enable **Microsoft Purview Audit** (Standard or Premium) at the tenant level, install the **Microsoft Business Applications** Sentinel solution (version 3.2.5 or later) in the Microsoft Defender portal, and connect **Power Platform Admin Activity**, **Power Automate** and **Dataverse** data connectors. Do not deploy legacy connectors feeding `PowerAppsActivity`, `PowerPlatformConnectorActivity`, `PowerPlatformDlpActivity` or `Dynamics365Activity`.
- **Assessor check ID**: `pp_ten_purview_audit_enabled` (manual)

## Rationale

Microsoft Sentinel's Codeless Connector Framework (CCF) connectors for Power Platform rely on Microsoft Purview Audit as their upstream source. Without Purview auditing active and connected to Sentinel, critical events such as DLP weakening, tenant isolation changes, mass app deletions and Dataverse exports go undetected.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0580` (centralised event logging), `ISM-0585` (retaining and analysing security event logs) and `ISM-1228` (detecting unauthorised administrative activity). Confirm against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly, though logging underpins monitoring across all strategies.

## How to configure

1. Open the Microsoft Purview portal with the **Audit Logs** or **Compliance Administrator** role, go to **Audit**, and confirm audit recording is active (select **Start recording user and admin activity** if not already enabled).
2. In the Microsoft Defender portal (Microsoft Sentinel), open **Content hub** and install **Microsoft Business Applications** version 3.2.5 or later.
3. Connect **Microsoft Power Platform Admin Activity**, **Microsoft Power Automate** and **Microsoft Dataverse** data connectors.
4. See [docs/research/verification.md](../../docs/research/verification.md) for verified table names and retirement dates.

## How to verify

- **Automated**: Manual check only (`manual`). The Power Platform BAP API does not expose Microsoft Purview Audit activation status or Sentinel workspace ingestion health.
- **Manual**: Confirm Purview Audit is active and run the following KQL validation query in Microsoft Sentinel:

```kusto
union withsource=Table isfuzzy=true PowerPlatformAdminActivity, PowerAutomateActivity, DataverseActivity
| where TimeGenerated > ago(1d)
| summarize Rows = count(), Latest = max(TimeGenerated) by Table
```

## References

- [Power Platform activity logging in Microsoft Purview | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/activity-logging-auditing/activity-logs-overview)
- [Connect Power Platform and Dynamics 365 CE to Microsoft Sentinel | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution)
- [Learn about auditing solutions in Microsoft Purview | Microsoft Learn](https://learn.microsoft.com/en-us/purview/audit-solutions-overview)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
