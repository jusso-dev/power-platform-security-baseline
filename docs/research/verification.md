# Research verification record

This document records the verification of claims, table names, solution versions, connectors and retirement dates from [pp-sentinel-research.tsx](pp-sentinel-research.tsx) against current official Microsoft Learn documentation and the [Azure/Azure-Sentinel](https://github.com/Azure/Azure-Sentinel) repository.

Verification date: 21 November 2026.

## Summary of outcomes

- **Microsoft Business Applications solution**: confirmed at version **3.2.5** (26 October 2026), which restored the Power Automate, Dataverse and Power Platform Admin Codeless Connector Framework (CCF) data connectors after the 3.2.4 migration to Defender XDR custom detections.
- **Microsoft Copilot solution**: confirmed GA on 2 April 2026 (3.0.2), with an additional update **3.2.2** on 11 April 2026 adding four Defender XDR custom detections and an XDR workbook. The table rename from `LLMActivity` to `CopilotActivity` occurred on 12 December 2025 (3.0.1).
- **Retired and legacy tables**: `PowerAppsActivity`, `PowerPlatformConnectorActivity` and `PowerPlatformDlpActivity` connectors were removed on **12 July 2024** (solution 3.1.3), with events consolidated into `PowerPlatformAdminActivity`. `Dynamics365Activity` is superseded by `DataverseActivity`. `AIAgentsInfo` was deprecated on **1 July 2026** in favour of `AgentsInfo`.
- **Copilot Studio admin logging gap**: no Microsoft-documented Sentinel table receives Copilot Studio maker and admin audit events (`BotCreate`, `BotDelete`, `BotUpdateOperation-*`). `CopilotActivity` covers interactions, plugins and Copilot settings; monitoring Dataverse `bot` table auditing and enforcing Copilot Studio data policies remain necessary.
- **Sentinel portal transition**: confirmed that Microsoft Sentinel will no longer be supported in the Azure portal after **31 March 2027** and will be available only in the Microsoft Defender portal.

## Solution versions and milestone dates

| Claim | Date in source | Status | Verified details and official source |
| --- | --- | --- | --- |
| Power Apps, Connectors and DLP connectors removed (solution 3.1.3) | 12 July 2024 | Verified | Confirmed in [Microsoft Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md). Events moved to `PowerPlatformAdminActivity`. |
| Solution renamed to Microsoft Business Applications (3.2.0); PPInventory retired | 15 November 2024 | Verified | Confirmed in [Microsoft Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md). Merged Dynamics 365 CE and F&O and retired the PPInventory function app. |
| Business Applications solution moved to GA (3.2.1) | 11 April 2025 | Verified | Confirmed in [Microsoft Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md). |
| Microsoft Copilot table renamed from `LLMActivity` to `CopilotActivity` (3.0.1) | 12 December 2025 | Verified | Confirmed in [Microsoft Copilot ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Copilot/ReleaseNotes.md). |
| Microsoft Copilot solution GA (3.0.2) and XDR update (3.2.2) | 2 April 2026 | Verified and updated | Confirmed 3.0.2 GA on 2 April 2026; updated with 3.2.2 on 11 April 2026 adding Defender XDR custom detections and XDR workbook in [Microsoft Copilot ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Copilot/ReleaseNotes.md). |
| Defender AI agent security requires Microsoft Agent 365 licence; `AIAgentsInfo` replaced by `AgentsInfo` | 1 July 2026 | Verified | Confirmed in [Transition Microsoft Copilot Studio and Microsoft Foundry agent security capabilities to Microsoft Agent 365](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/transition-agent-security-to-agent-365) and [AI agent inventory](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-inventory). |
| Business Applications XDR migration (3.2.4) and CCF connector restoration (3.2.5) | 25 to 26 October 2026 | Verified | Confirmed in [Microsoft Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md). Deploy version 3.2.5 or later. |
| Microsoft Sentinel retires in the Azure portal (Defender portal only) | 31 March 2027 | Verified | Confirmed verbatim ("After March 31, 2027, Microsoft Sentinel will no longer be supported in the Azure portal") in [Microsoft Sentinel in the Microsoft Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal) and [Microsoft Sentinel Tech Community timeline update](https://techcommunity.microsoft.com/blog/microsoftsentinelblog/update-new-timeline-for-transitioning-sentinel-experience-to-defender-portal/4490464). |

## Active tables and connectors

| Table | Connector / solution | Status | Official reference |
| --- | --- | --- | --- |
| `PowerPlatformAdminActivity` | Microsoft Power Platform Admin Activity (Microsoft Business Applications 3.2.5+, CCF via Purview Audit) | Verified active | [PowerPlatformAdminActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/powerplatformadminactivity) and [Deploy Power Platform solution](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution) |
| `PowerAutomateActivity` | Microsoft Power Automate (Microsoft Business Applications 3.2.5+, CCF via Purview Audit) | Verified active | [PowerAutomateActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/powerautomateactivity) |
| `DataverseActivity` | Microsoft Dataverse (Microsoft Business Applications 3.2.5+, CCF via Purview Audit) | Verified active | [DataverseActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dataverseactivity) and [Manage Dataverse auditing](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing) |
| `CopilotActivity` | Microsoft Copilot (Microsoft Copilot solution 3.0.1+ / 3.2.2+) | Verified active | [CopilotActivity table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/copilotactivity) and [Audit logs for Copilot and AI applications](https://learn.microsoft.com/en-us/purview/audit-copilot) |
| `AgentsInfo` | Microsoft Defender XDR / Microsoft Agent 365 (Advanced Hunting) | Verified active | [AI agent inventory](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-inventory) |
| `SigninLogs`, `AuditLogs` | Microsoft Entra ID connector | Verified active | Required for correlation by multiple Business Applications analytic rules; documented in [Security content reference](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/power-platform-solution-security-content) |
| `OfficeActivity` | Microsoft 365 connector | Verified active (optional) | Used by Dataverse SharePoint document management rules in [Microsoft Business Applications solution](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/Microsoft%20Business%20Applications/Analytic%20Rules) |

## Retired and legacy tables

| Legacy table or component | Retirement / removal date | Replacement | Official reference |
| --- | --- | --- | --- |
| `PowerAppsActivity` | 12 July 2024 (solution 3.1.3 connector removal) | `PowerPlatformAdminActivity` | [PowerAppsActivity reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/powerappsactivity) and [Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md) |
| `PowerPlatformConnectorActivity` | 12 July 2024 (solution 3.1.3 connector removal) | `PowerPlatformAdminActivity` | [PowerPlatformConnectorActivity reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/powerplatformconnectoractivity) and [Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md) |
| `PowerPlatformDlpActivity` | 12 July 2024 (solution 3.1.3 connector removal) | `PowerPlatformAdminActivity` | [PowerPlatformDlpActivity reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/powerplatformdlpactivity) and [Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md) |
| `Dynamics365Activity` | Legacy connector replaced by Microsoft Dataverse connector (date varies by tenant migration; deprecated in favour of Dataverse CCF) | `DataverseActivity` | [Dynamics365Activity reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/dynamics365activity) and [Solution overview](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/solution-overview) |
| `PPInventory` function app | 15 November 2024 (solution 3.2.0) | [Power Platform inventory](https://learn.microsoft.com/en-us/power-platform/admin/power-platform-inventory) | [Business Applications ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Business%20Applications/ReleaseNotes.md) |
| `LLMActivity` | 12 December 2025 (Microsoft Copilot 3.0.1) | `CopilotActivity` | [Microsoft Copilot ReleaseNotes.md](https://github.com/Azure/Azure-Sentinel/blob/master/Solutions/Microsoft%20Copilot/ReleaseNotes.md) |
| `AIAgentsInfo` | 1 July 2026 | `AgentsInfo` | [Transition agent security to Microsoft Agent 365](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/transition-agent-security-to-agent-365) |

Note: Schema reference pages for `PowerAppsActivity`, `PowerPlatformConnectorActivity`, `PowerPlatformDlpActivity` and `Dynamics365Activity` still exist on Microsoft Learn for historical workspaces, but new detections must not target them.

## Out-of-the-box Sentinel content verification

Direct inspection of `Azure/Azure-Sentinel` confirmed the following content counts:

- **Microsoft Business Applications** ([repository folder](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/Microsoft%20Business%20Applications)):
  - 49 analytic rules total: 44 across Power Platform, Power Apps, Power Automate and Dataverse (matching the 44 listed in `pp-sentinel-research.tsx`), plus 5 Dynamics 365 Finance and Operations (F&O) rules excluded from Power Platform scope.
  - 8 hunting queries (`Dataverse` and `Power Apps`).
  - 8 playbooks (`MSBizApps-Incident-From-Alert-Teams`, `Dataverse-Send-Manager-Notification`, five blocklist playbooks, and `Dataverse-Add-SharePoint-Site`).
  - 1 workbook (`Dynamics365Activity.json`), plus Defender XDR detections and workbooks added in 3.2.4.
- **Microsoft Copilot** ([repository folder](https://github.com/Azure/Azure-Sentinel/tree/master/Solutions/Microsoft%20Copilot)):
  - 4 analytic rules (`CopilotJailbreakAttempt`, `CopilotPluginCreatedByNonAdmin`, `CopilotPluginTampering`, `CopilotFileUploadsDisabled`).
  - 2 hunting queries (`CopilotExternalIPAccess`, `CopilotPluginReEnabled`).
  - 1 workbook (`MicrosoftCopilotActivityMonitoring.json`), plus Defender XDR custom detections and workbook added in 3.2.2.

## Playbook and governance connectors verified

- **Power Platform for Admins V2** ([connector reference](https://learn.microsoft.com/en-us/connectors/powerplatformadminv2/)): verified. Supports Logic Apps managed identity connections and Service Principal connections.
- **Power Platform for Admins** ([connector reference](https://learn.microsoft.com/en-us/connectors/powerplatformforadmins/)): verified.
- **Power Automate Management** ([connector reference](https://learn.microsoft.com/en-us/connectors/flowmanagement/)): verified.
- **Power Apps for Admins** ([connector reference](https://learn.microsoft.com/en-us/connectors/powerappsforadmins/)): verified.
- **Copilot Studio data policies** ([Configure data policies for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)): verified that organisations can restrict channels and block unauthenticated chat in Copilot Studio via Power Platform data policies.

## Copilot Studio logging gap

- **Status**: Verified gap.
- **Findings**: Microsoft Purview captures Copilot interaction audit events ([Audit logs for Copilot and AI applications](https://learn.microsoft.com/en-us/purview/audit-copilot)) which flow into Sentinel's `CopilotActivity` table via the Microsoft Copilot solution. While Copilot Studio maker and admin operations (`BotCreate`, `BotDelete`, `BotUpdateOperation-*`) appear in Purview Audit, Microsoft does not document a dedicated Sentinel table or Business Applications connector stream guaranteed to ingest those Copilot Studio admin operations.
- **Mitigation**:
  1. Enable Dataverse auditing on the `bot` and `botcomponent` tables in environments hosting agents so changes are captured in `DataverseActivity` ([Manage Dataverse auditing](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing)).
  2. Enforce preventive controls via Power Platform data policies ([Configure data policies for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)).
  3. Where licensed for Microsoft Agent 365, use `AgentsInfo` in Microsoft Defender XDR Advanced Hunting ([AI agent inventory](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-inventory)).

## Unverified and tenant-dependent claims

The following items from `pp-sentinel-research.tsx` could not be independently confirmed from static Microsoft Learn pages alone and must be validated against live tenant telemetry before relying on them in production detections:

| Item | Status | Notes |
| --- | --- | --- |
| Exact raw `EventOriginalType` names for environment lifecycle events (custom rule C3) | Unverified (tenant-dependent) | [Power Platform activity logging overview](https://learn.microsoft.com/en-us/power-platform/admin/activity-logging-auditing/activity-logs-overview) documents friendly names; run a 30-day `summarize by EventOriginalType` query on `PowerPlatformAdminActivity` in the target tenant to pin exact strings. |
| `FlowConnectorNames` string formatting in `PowerAutomateActivity` (custom rule C4) | Unverified (tenant-dependent) | Display names versus connector IDs vary across connector types; confirm distinct values in `PowerAutomateActivity` before finalising allow/block lists. |
| `targetuser.id` equals the tenant GUID when a canvas app is shared with Everyone (custom rule C6) | Unverified (tenant-dependent) | Test sharing a sandbox canvas app with Everyone and inspect `PropertyCollection` in `PowerPlatformAdminActivity`. |
| Per-environment `System Administrator` role GUIDs in `DataverseActivity` (custom rule C7) | Tenant-specific by design | Each Dataverse environment generates unique `roleid` values; maintain an environment-to-roleid watchlist. |
| Guest user `#EXT#` pattern in `DataverseActivity.UserId` (custom rule C8) | Unverified (tenant-dependent) | Verify whether guest `UserId` values contain `#EXT#` in your tenant or join against `IdentityInfo` where `UserType == "Guest"`. |
| Dataverse `bot` table `authenticationmode == "1"` equals "No authentication" (custom rule C9) | Unverified (tenant-dependent) | Confirm the `authenticationmode` picklist integer values in the Dataverse `bot` table metadata in a target environment before enabling the rule. |
| Purview preview label on Power Platform admin activity logs | Unverified (subject to change) | Microsoft updates preview/GA status periodically on [Power Platform activity logging overview](https://learn.microsoft.com/en-us/power-platform/admin/activity-logging-auditing/activity-logs-overview); check the banner when deploying. |
