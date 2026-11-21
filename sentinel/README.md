# Microsoft Sentinel content

Analytics rules, hunting queries, workbook and Logic Apps playbooks for Microsoft Power Platform, Power Automate, Dataverse and Copilot Studio.

> **Portal note**: Microsoft Sentinel will no longer be supported in the Azure portal after **31 March 2027** and will be available only in the [Microsoft Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal). Deploy and test these detections in the Microsoft Defender portal.

## Prerequisites

1. Enable **Microsoft Purview Audit** ([Power Platform activity logging overview](https://learn.microsoft.com/en-us/power-platform/admin/activity-logging-auditing/activity-logs-overview)).
2. Install the **Microsoft Business Applications** solution version **3.2.5 or later** from Content Hub and connect:
   - Microsoft Power Platform Admin Activity (`PowerPlatformAdminActivity`)
   - Microsoft Power Automate (`PowerAutomateActivity`)
   - Microsoft Dataverse (`DataverseActivity`)
3. Install the **Microsoft Copilot** solution (version **3.0.2 or later**) for `CopilotActivity` if monitoring Copilot and agent interactions.
4. Connect **Microsoft Entra ID** (`SigninLogs`, `AuditLogs`) for identity and risk correlation.
5. Do **not** deploy legacy connectors feeding retired tables (`PowerAppsActivity`, `PowerPlatformConnectorActivity`, `PowerPlatformDlpActivity`, `Dynamics365Activity`, `LLMActivity`, `AIAgentsInfo`). See [docs/research/verification.md](../docs/research/verification.md).

## Out-of-the-box versus custom rules

Enable Microsoft's out-of-the-box rules in the [Microsoft Business Applications solution](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/power-platform-solution-security-content) first. The custom rules in this directory only close gaps that out-of-the-box content misses:

| Custom rule | What the out-of-the-box solution misses | Table(s) | ATT&CK | ISM |
| --- | --- | --- | --- | --- |
| [pp-admin-dlp-policy-unauthorised-change.yaml](analytics-rules/power-platform-admin/pp-admin-dlp-policy-unauthorised-change.yaml) | OOB DLP rule ignores `CreateDlpPolicy`, ignores edits within 10 minutes of creation, and has no approved-admin allow-list | `PowerPlatformAdminActivity` | T1562.001 | ISM-0263, ISM-0580, ISM-1585 |
| [pp-admin-tenant-isolation-or-secgroup-changed.yaml](analytics-rules/power-platform-admin/pp-admin-tenant-isolation-or-secgroup-changed.yaml) | OOB guest exfiltration rule fires only after exfiltration alerts follow; does not alert on defence impairment alone | `PowerPlatformAdminActivity` | T1562.001 | ISM-0263, ISM-0407, ISM-1585 |
| [pp-admin-environment-unapproved-region.yaml](analytics-rules/power-platform-admin/pp-admin-environment-unapproved-region.yaml) | No OOB rule alerts when environments are provisioned outside approved data residency regions or copied/moved | `PowerPlatformAdminActivity` | T1578.002, T1537 | ISM-1585, ISM-0407 |
| [pp-admin-role-self-elevation-or-change.yaml](analytics-rules/power-platform-admin/pp-admin-role-self-elevation-or-change.yaml) | OOB Entra role rule misses tenant admins self-elevating via `ApplyAdminRole` and Dataverse `System Administrator` grants | `PowerPlatformAdminActivity`, `DataverseActivity` | T1098, T1078 | ISM-0445, ISM-1175, ISM-1228 |
| [pp-admin-sensitive-env-high-risk-connector.yaml](analytics-rules/power-platform-admin/pp-admin-sensitive-env-high-risk-connector.yaml) | OOB connector rule is Low severity and treats all connectors equally; this highlights high-risk HTTP, file-transfer and consumer connectors | `PowerPlatformAdminActivity` | T1059, T1567 | ISM-0263, ISM-1585 |
| [dv-guest-export-or-bulk-read.yaml](analytics-rules/power-automate-dataverse/dv-guest-export-or-bulk-read.yaml) | OOB export baseline rule can miss brand-new guest accounts with no 14-day history | `DataverseActivity` | T1567, T1213 | ISM-0263, ISM-0585 |
| [dv-bulk-record-deletion-or-purge.yaml](analytics-rules/power-automate-dataverse/dv-bulk-record-deletion-or-purge.yaml) | Adds maintenance-account allow-list over BulkDelete, DeleteAuditData and high-volume Delete activity | `DataverseActivity` | T1485, T1070 | ISM-0585, ISM-1511 |
| [dv-audit-settings-disabled-or-weakened.yaml](analytics-rules/power-automate-dataverse/dv-audit-settings-disabled-or-weakened.yaml) | Explicitly detects disabling of read auditing, user access logging and SAS Purview logging in addition to global auditing | `DataverseActivity` | T1562.001, T1562.008 | ISM-0580, ISM-1228 |
| [dv-copilot-agent-no-authentication.yaml](analytics-rules/power-automate-dataverse/dv-copilot-agent-no-authentication.yaml) | Mitigates Microsoft's Copilot Studio admin Sentinel logging gap by watching Dataverse `bot` table `authenticationmode` | `DataverseActivity` | T1190, T1562.001 | ISM-0407, ISM-1585 |
| [pa-flow-personal-or-http-connectors.yaml](analytics-rules/power-automate-dataverse/pa-flow-personal-or-http-connectors.yaml) | OOB Power Automate rules do not flag flows built with personal email, file-storage or raw HTTP connectors | `PowerAutomateActivity` | T1567, T1048 | ISM-0263, ISM-1585 |
| [pa-flow-created-after-risky-signin.yaml](analytics-rules/power-automate-dataverse/pa-flow-created-after-risky-signin.yaml) | Correlates Entra ID Protection risky sign-ins with immediate flow creation or edits | `PowerAutomateActivity`, `SigninLogs` | T1078, T1567 | ISM-0585, ISM-1228 |
| [pa-flow-shared-with-guest-or-external.yaml](analytics-rules/power-automate-dataverse/pa-flow-shared-with-guest-or-external.yaml) | Flags flows shared with guests or external domains, distinguishing Owner versus Run-only grants | `PowerAutomateActivity` | T1098 | ISM-0407, ISM-1585 |

## Hunting queries and tuning

- Six proactive hunting queries for Dataverse exports, TDS/Web API bulk reads, application user spikes, unapproved flow connectors, rare maker IPs and broad canvas app sharing live in [sentinel/hunting-queries/power-automate-dataverse/](hunting-queries/power-automate-dataverse/).
- Noise tuning guidance lives in [sentinel/analytics-rules/power-automate-dataverse/TUNING.md](analytics-rules/power-automate-dataverse/TUNING.md).

## Workbook

- The Power Platform Security Posture workbook (JSON, deployable ARM template, Deploy to Azure button and synthetic preview screenshot) lives in [sentinel/workbooks/](workbooks/README.md).

## Validation and tests

- Run `python3 scripts/validate_sentinel.py` to validate YAML rules against Microsoft Sentinel content schemas, check ARM JSON templates, block retired table names and verify every rule has a KQL datatable test.
- KQL datatable tests live under `sentinel/tests/` and can be pasted directly into Log Analytics or Microsoft Defender Advanced Hunting.
- ARM templates for one-step deployment live under `sentinel/arm/`.
