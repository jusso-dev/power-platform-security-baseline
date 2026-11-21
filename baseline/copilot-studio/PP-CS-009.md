---
id: PP-CS-009
title: Enable Dataverse bot table auditing and CopilotActivity ingestion (mitigating the Copilot Studio logging gap)
scope: environment
workload: copilot-studio
severity: critical
recommended_value: Dataverse auditing enabled on bot and botcomponent tables in agent environments, plus Microsoft Copilot Sentinel solution connected for CopilotActivity
rationale: Microsoft does not document a Sentinel table that receives Purview Copilot Studio admin/maker audit events (BotCreate, BotUpdateOperation-*); auditing the Dataverse bot table is the reliable Sentinel path to detect agent auth and configuration tampering.
ism_controls:
  - ISM-0580
  - ISM-0585
  - ISM-1228
essential_eight: []
configure_summary: Enable Dataverse auditing on environments hosting Copilot Studio agents (including bot and botcomponent tables) and connect the Microsoft Copilot Sentinel solution (CopilotActivity).
verify_summary: Verify Dataverse auditing is active on every environment containing Copilot Studio bots via the Dataverse Web API, and manually confirm CopilotActivity ingestion in Sentinel.
assessor_check_id: pp_cs_audit_and_sentinel_coverage
automated: true
sentinel_rules:
  - C9 - Copilot Studio agent configured with No authentication
  - Copilot - Jailbreak Attempt Detected
  - Copilot - Plugin Created by Non-Admin User
  - Copilot - Plugin tampering
references:
  - title: Audit logs for Copilot and AI applications | Microsoft Learn
    url: https://learn.microsoft.com/en-us/purview/audit-copilot
  - title: CopilotActivity table reference | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/copilotactivity
  - title: Manage Dataverse auditing - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing
  - title: Guidelines for secure AI system development | cyber.gov.au
    url: https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-009: Enable Dataverse bot table auditing and CopilotActivity ingestion (mitigating the Copilot Studio logging gap)

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Copilot Studio
- **Recommended value**:
  1. Enable Dataverse global auditing (`isauditenabled: true`) and table-level auditing on the `bot` and `botcomponent` tables in every environment hosting Copilot Studio agents so configuration changes land in Microsoft Sentinel's `DataverseActivity` table.
  2. Install the **Microsoft Copilot** Sentinel solution (version 3.0.2 or later; table `CopilotActivity`, which replaced `LLMActivity` on 12 December 2025) to capture `CopilotInteraction` and plugin/settings telemetry.
- **Assessor check ID**: `pp_cs_audit_and_sentinel_coverage` (automated for Dataverse auditing on agent environments; verify `CopilotActivity` ingestion in Sentinel)

## Rationale

**Documented logging gap**: Microsoft Purview documents Copilot interaction events ([Audit logs for Copilot and AI applications](https://learn.microsoft.com/en-us/purview/audit-copilot)) and records Copilot Studio maker/admin events (`BotCreate`, `BotDelete`, `BotUpdateOperation-BotAuthUpdate`, `BotUpdateOperation-BotPublish`, `BotUpdateOperation-BotShare`), but **Microsoft does not document any Microsoft Sentinel table guaranteed to receive Copilot Studio maker and admin audit events**. Furthermore, Copilot Studio interaction events in Purview are only recorded for users holding an assigned Microsoft 365 licence. See [docs/research/verification.md](../../docs/research/verification.md).

Enabling Dataverse auditing on the `bot` and `botcomponent` tables provides a dependable Sentinel detection trail in `DataverseActivity` when an agent is created or switched to **No authentication**, complementing `CopilotActivity` for runtime interactions and jailbreak detections.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0580` (security event logging), `ISM-0585` (centralised SIEM log analysis) and `ISM-1228` (detecting configuration tampering). Aligns with ASD's [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development) (logging and monitoring AI systems in operation). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. In every environment hosting Copilot Studio agents, enable **Start auditing** and **Log access** (`PP-ENV-002`).
2. In Power Apps maker portal (**Tables** > **All**), open the `bot` and `botcomponent` tables, enable **Audit changes to its data** under **Properties** > **Advanced options**, and publish customisations.
3. In the Microsoft Defender portal (Microsoft Sentinel), install the **Microsoft Copilot** solution from Content Hub and connect the Microsoft Copilot data connector (`CopilotActivity`).
4. Enable the out-of-the-box `Copilot - Jailbreak Attempt Detected`, `Copilot - Plugin Created by Non-Admin User` and `Copilot - Plugin tampering` rules alongside the custom Dataverse `bot` table rule.

## How to verify

- **Automated**: For every environment containing one or more Copilot Studio bots, verify `isauditenabled` is `true` in Dataverse organization settings (and `bot` table auditing metadata where returned).
- **Manual**: Confirm `CopilotActivity` and `DataverseActivity` (where `EntityName == "bot"`) receive rows in Microsoft Sentinel.

## References

- [Audit logs for Copilot and AI applications | Microsoft Learn](https://learn.microsoft.com/en-us/purview/audit-copilot)
- [CopilotActivity table reference | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/copilotactivity)
- [Manage Dataverse auditing - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing)
- [Research verification record](../../docs/research/verification.md)
- [Guidelines for secure AI system development | cyber.gov.au](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
