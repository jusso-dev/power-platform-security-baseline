# Microsoft Sentinel Logic Apps Playbooks

Automated response playbooks for high-severity Power Platform, Power Automate and Dataverse incidents in Microsoft Sentinel. Every playbook uses a **System-Assigned Managed Identity** and least-privilege permissions (no stored user passwords or long-lived client secrets).

> **Operational safety**: Start containment playbooks (`PP-Disable-Risky-Flow`, `PP-Quarantine-Power-App`, `PP-Remove-User-Env-SecurityGroup`) on manual analyst trigger or behind a Teams approval workflow until analytics rule false-positive rates are proven low.

## Playbook catalogue

| Playbook | Action | Triggering rules | Deploy |
| --- | --- | --- | --- |
| [PP-Notify-Admin-Team](PP-Notify-Admin-Team/azuredeploy.json) | Posts high-severity incident details to the Power Platform admin team channel and comments on the incident | All high-severity Power Platform rules | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fpower-platform-security-baseline%2Fmain%2Fsentinel%2Fplaybooks%2FPP-Notify-Admin-Team%2Fazuredeploy.json) |
| [PP-Disable-Risky-Flow](PP-Disable-Risky-Flow/azuredeploy.json) | Stops a risky Power Automate flow via the Power Automate Management API and logs the action on the incident | `pa-flow-personal-or-http-connectors`, `pa-flow-created-after-risky-signin` | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fpower-platform-security-baseline%2Fmain%2Fsentinel%2Fplaybooks%2FPP-Disable-Risky-Flow%2Fazuredeploy.json) |
| [PP-Quarantine-Power-App](PP-Quarantine-Power-App/azuredeploy.json) | Sets a canvas Power App's quarantine state to `Quarantined` via the Power Apps Admin API and comments on the incident | `hunt-pa-canvas-app-broad-sharing`, OOB malicious link / unauthorised geo rules | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fpower-platform-security-baseline%2Fmain%2Fsentinel%2Fplaybooks%2FPP-Quarantine-Power-App%2Fazuredeploy.json) |
| [PP-Remove-User-Env-SecurityGroup](PP-Remove-User-Env-SecurityGroup/azuredeploy.json) | Removes an affected user from a protected environment's Entra security group and revokes active sign-in sessions via Microsoft Graph | `dv-guest-export-or-bulk-read`, `dv-bulk-record-deletion-or-purge`, `pa-flow-created-after-risky-signin` | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fpower-platform-security-baseline%2Fmain%2Fsentinel%2Fplaybooks%2FPP-Remove-User-Env-SecurityGroup%2Fazuredeploy.json) |

## Least-privilege managed identity permissions

After deploying each ARM template, note the `playbookPrincipalId` output and grant **only** the permissions required by that playbook:

| Playbook | Azure RBAC (Sentinel workspace RG) | Power Platform / Microsoft Graph API permissions |
| --- | --- | --- |
| `PP-Notify-Admin-Team` | `Microsoft Sentinel Responder` | None (uses secured Teams/SOC webhook URL) |
| `PP-Disable-Risky-Flow` | `Microsoft Sentinel Responder` | Register Managed Identity as a Power Platform management app (`New-PowerAppManagementApp`) with flow stop rights |
| `PP-Quarantine-Power-App` | `Microsoft Sentinel Responder` | Register Managed Identity as a Power Platform management app with Power Apps quarantine rights |
| `PP-Remove-User-Env-SecurityGroup` | `Microsoft Sentinel Responder` | Microsoft Graph application permissions: `User.Read.All`, `User.RevokeSessions.All`, `GroupMember.ReadWrite.All` (prefer scoping group management via Administrative Units or dedicated non-privileged groups) |

To allow Microsoft Sentinel automation rules to trigger a playbook, grant the **Microsoft Sentinel Automation Contributor** role to the `Azure Security Insights` service principal on the resource group hosting the playbooks ([Automate threat response with playbooks in Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks)).

## References

- [Automate threat response with playbooks in Microsoft Sentinel | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks)
- [Power Automate Management connector | Microsoft Learn](https://learn.microsoft.com/en-us/connectors/flowmanagement/)
- [Power Apps for Admins connector | Microsoft Learn](https://learn.microsoft.com/en-us/connectors/powerappsforadmins/)
- [Power Platform for Admins V2 connector | Microsoft Learn](https://learn.microsoft.com/en-us/connectors/powerplatformadminv2/)
- [Microsoft Graph permissions reference | Microsoft Learn](https://learn.microsoft.com/en-us/graph/permissions-reference)
