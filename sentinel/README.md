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

## Validation and tests

- Run `python3 scripts/validate_sentinel.py` to validate YAML rules against Microsoft Sentinel content schemas, check ARM JSON templates, block retired table names and verify every rule has a KQL datatable test.
- KQL datatable tests live under `sentinel/tests/` and can be pasted directly into Log Analytics or Microsoft Defender Advanced Hunting.
- ARM templates for one-step deployment live under `sentinel/arm/`.
