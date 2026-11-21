# Noise tuning notes for Power Automate and Dataverse detections

Before enabling these detections in production, run each query interactively over the past 14 to 30 days in Microsoft Sentinel (Microsoft Defender portal) and adjust the allow-lists and thresholds below.

## General tuning guidance

- **Use watchlists for dynamic lists**: Replace inline `dynamic([...])` placeholders (`approved_admins`, `sensitive_environments`, `internal_domains`, `maintenance_accounts`, `approved_integration_envs`) with Sentinel watchlists so updates do not require editing rule queries.
- **Avoid duplicating Defender XDR custom detections**: Starting with Microsoft Business Applications 3.2.4, Microsoft ships equivalent detections in both Sentinel Scheduled Analytics and Defender XDR Custom Detection formats. Enable one format per rule.
- **Manage `DataverseActivity` Read log volume**: Read logs (`isreadauditenabled`) generate high ingestion volume. Only enable Read logs on sensitive production environments (`PP-ENV-003`) and consider a Data Collection Rule (DCR) transformation to filter high-volume benign service accounts (`SYSTEM`, scheduled sync application users) if ingestion cost rises.

## Rule-specific tuning

| Rule | Common benign noise sources | Recommended tuning |
| --- | --- | --- |
| `dv-guest-export-or-bulk-read.yaml` | External contractors legitimately running reporting views in a partner portal | Raise `retrieve_threshold` (default `500`) per environment or exclude specific partner guest UPNs bound to an approved security group. If guest UPNs do not contain `#EXT#`, join against `IdentityInfo` where `UserType == "Guest"`. |
| `dv-bulk-record-deletion-or-purge.yaml` | Scheduled Dataverse retention jobs (for example `conversationtranscript` or old `asyncoperation` cleanup) | Add dedicated archival service principals to `maintenance_accounts` and exclude `EntityName in ("asyncoperation", "conversationtranscript")` only if governed by approved retention jobs. |
| `dv-audit-settings-disabled-or-weakened.yaml` | Planned sandbox refreshes or temporary migration maintenance windows | Keep enabled with zero exclusions in production; scope out non-production `InstanceUrl` values if sandbox admins toggle auditing during testing. |
| `dv-copilot-agent-no-authentication.yaml` | Approved public website customer-service agents hosted in a dedicated public environment | Exclude the dedicated public-website `InstanceUrl` once `PP-CS-002` DLP blocking is active on all internal environments. Confirm the integer value of `authenticationmode` in your `bot` table schema first. |
| `pa-flow-personal-or-http-connectors.yaml` | Approved enterprise integration flows calling internal REST APIs via HTTP in a dedicated integration environment | Add the integration environment GUID to `approved_integration_envs` and confirm exact `FlowConnectorNames` strings in your tenant (`PowerAutomateActivity \| distinct FlowConnectorNames`). |
| `pa-flow-created-after-risky-signin.yaml` | False-positive VPN or travel sign-in risk events | Require `RiskLevelDuringSignIn == "high"` for lower alert volume, or keep `medium` and `high` with an incident verification playbook (`MSBizApps-Incident-From-Alert-Teams`). |
| `pa-flow-shared-with-guest-or-external.yaml` | Multi-domain organisations with subsidiaries or sister agencies | Populate `internal_domains` with all verified Entra domains belonging to the organisation; prioritise `Permission == "Owner"` alerts as High severity. |
