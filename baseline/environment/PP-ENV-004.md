---
id: PP-ENV-004
title: Enable Dataverse SAS logging to Microsoft Purview
scope: environment
workload: dataverse
severity: medium
recommended_value: Enable SAS Logging in Purview turned on in Privacy + Security settings for production environments
rationale: Shared Access Signature (SAS) logging records access to Dataverse blob and file attachments in Purview so file-based exfiltration and suspicious attachment access appear in Sentinel DataverseActivity.
ism_controls:
  - ISM-0580
  - ISM-0585
essential_eight: []
configure_summary: Power Platform admin centre > Environments > Select environment > Settings > Product > Privacy + Security > Enable SAS Logging in Purview.
verify_summary: Read environment privacy and security settings via Dataverse Web API or BAP API and confirm SAS logging in Purview is enabled.
assessor_check_id: pp_env_sas_logging_purview
automated: true
sentinel_rules:
  - Dataverse - Mass export of records to Excel
references:
  - title: Privacy + Security settings - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/settings-privacy-security
  - title: Connect Power Platform and Dynamics 365 CE to Microsoft Sentinel | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-004: Enable Dataverse SAS logging to Microsoft Purview

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Turn **Enable SAS Logging in Purview** to **On** in every production Dataverse environment, after verifying network allow-lists permit `https://*.api.powerplatformusercontent.com`.
- **Assessor check ID**: `pp_env_sas_logging_purview` (automated)

## Rationale

Dataverse file columns and attachments are served via short-lived Shared Access Signature (SAS) URLs. Enabling SAS logging in Microsoft Purview closes a blind spot in file access monitoring and is part of Microsoft's deployment guidance for the [Microsoft Sentinel Business Applications solution](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution) (documented in [docs/research/verification.md](../../docs/research/verification.md)).

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0580` (comprehensive event logging) and `ISM-0585` (forwarding cloud access events for SIEM analysis). Confirm against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. Confirm egress proxies and firewalls allow `https://*.api.powerplatformusercontent.com`.
2. In the Power Platform admin centre, open the environment > **Settings** > **Product** > **Privacy + Security**.
3. Turn **Enable SAS Logging in Purview** to **On** and select **Save**.

## How to verify

- **Automated**: Read the Dataverse organization configuration via the read-only Web API and assert that Purview SAS logging is enabled (`isenablesaslogginginpurview` / environment privacy setting flag `true`).
- **Manual**: Inspect **Settings** > **Product** > **Privacy + Security** for each production environment in the Power Platform admin centre.

## References

- [Privacy + Security settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/settings-privacy-security)
- [Connect Power Platform and Dynamics 365 CE to Microsoft Sentinel | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/deploy-power-platform-solution)
- [Research verification record](../../docs/research/verification.md)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
