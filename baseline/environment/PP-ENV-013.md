---
id: PP-ENV-013
title: Maintain strict blocked file extensions in Dataverse attachment settings
scope: environment
workload: dataverse
severity: high
recommended_value: Dataverse blockedattachments list retains all default executable, script and macro-enabled extensions (including exe, ps1, bat, cmd, vbs, js, dll, msi, hta, scr, docm, xlsm)
rationale: Removing executable or script extensions from the Dataverse block list allows attackers or compromised users to host malware and phishing payloads inside Dataverse notes and file attachments.
ism_controls:
  - ISM-0263
  - ISM-1490
essential_eight:
  - Application control
  - User application hardening
configure_summary: Power Platform admin centre > Environments > Select environment > Settings > Product > Privacy + Security > Blocked attachments.
verify_summary: Read Dataverse organization entity blockedattachments via Web API and verify mandatory dangerous extensions remain present.
assessor_check_id: pp_env_blocked_file_extensions
automated: true
sentinel_rules:
  - Dataverse - Removal of blocked file extensions
  - Dataverse - Executable uploaded to SharePoint document management site
references:
  - title: Privacy + Security settings - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/settings-privacy-security
  - title: Security content reference for Power Platform and Dynamics 365 CE | Microsoft Learn
    url: https://learn.microsoft.com/en-us/azure/sentinel/business-applications/power-platform-solution-security-content
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-013: Maintain strict blocked file extensions in Dataverse attachment settings

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Keep Microsoft's full default list of blocked file extensions in Dataverse **Set blocked file extensions for attachments** (`blockedattachments`) and ensure critical high-risk extensions (`exe`, `dll`, `msi`, `ps1`, `bat`, `cmd`, `vbs`, `js`, `hta`, `scr`, `lnk`, `iso`, `img`, `cab`) are never removed. Add macro-enabled Office extensions (`docm`, `xlsm`, `pptm`) where macros are not required.
- **Assessor check ID**: `pp_env_blocked_file_extensions` (automated)

## Rationale

Adversaries abuse cloud business applications to stage malicious files internally where users trust links and downloads. Weakening the Dataverse attachment block list creates an internal malware hosting channel; Microsoft Sentinel specifically includes the out-of-the-box rule `Dataverse - Removal of blocked file extensions` to detect tampering.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (filtering executable and active content) and `ISM-1490` (blocking untrusted executable files). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Application control](https://www.cyber.gov.au/essential-eight) and [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. In the Power Platform admin centre, select the environment > **Settings** > **Product** > **Privacy + Security**.
2. Review **Set blocked file extensions for attachments** and ensure all executable, script and disk-image extensions are listed (semicolon-separated).
3. Save changes and enable the Sentinel rule `Dataverse - Removal of blocked file extensions`.

## How to verify

- **Automated**: Read `blockedattachments` from the read-only Dataverse Web API `organizations` entity, split on `;`, and verify every mandatory dangerous extension (`exe`, `dll`, `msi`, `ps1`, `bat`, `cmd`, `vbs`, `js`, `hta`, `scr`, `lnk`) is present.
- **Manual**: Inspect **Set blocked file extensions for attachments** under **Settings** > **Product** > **Privacy + Security**.

## References

- [Privacy + Security settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/settings-privacy-security)
- [Security content reference for Power Platform and Dynamics 365 CE | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/power-platform-solution-security-content)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
