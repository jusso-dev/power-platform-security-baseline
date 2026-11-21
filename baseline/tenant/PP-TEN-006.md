---
id: PP-TEN-006
title: Block high-risk HTTP, file transfer and consumer connectors in tenant DLP baseline
scope: tenant
workload: power-platform
severity: critical
recommended_value: Tenant-wide DLP policy blocks HTTP, HTTP with Microsoft Entra ID, FTP/SFTP, Gmail, Outlook.com, Dropbox and Google Drive unless explicitly approved in an isolated environment
rationale: Raw HTTP and consumer connectors allow trivial data exfiltration from corporate SaaS sources and bypass domain-level DLP boundaries if left in Non-business alongside internal connectors.
ism_controls:
  - ISM-0263
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Data policies > Place high-risk connectors and unapproved custom connector URL patterns in Blocked.
verify_summary: Inspect tenant-wide DLP policies via BAP API and verify high-risk connector IDs (HTTP, FTP, consumer email and consumer cloud storage) are classified as Blocked.
assessor_check_id: pp_ten_dlp_blocks_high_risk_connectors
automated: true
sentinel_rules:
  - C4 - Flow created or edited with consumer, file-share or raw HTTP connectors
  - Power Platform - Connector added to a sensitive environment
references:
  - title: Data policies - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-006: Block high-risk HTTP, file transfer and consumer connectors in tenant DLP baseline

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Power Platform
- **Recommended value**: Classify raw HTTP (`shared_http`), FTP/SFTP (`shared_ftp`, `shared_sftpwithssh`), consumer email (`shared_gmail`, `shared_outlook`), and consumer file storage (`shared_dropbox`, `shared_googledrive`) connectors as **Blocked** in the tenant baseline DLP policy. Restrict custom connector URL patterns to explicitly allow-listed organisational domains.
- **Assessor check ID**: `pp_ten_dlp_blocks_high_risk_connectors` (automated)

## Rationale

Flows and apps using raw HTTP POST requests or consumer storage connectors are a primary exfiltration path from Power Platform. Placing these connectors in **Blocked** enforces preventive control; where an integration legitimately requires HTTP, grant an exception only in a dedicated, Managed Environment with endpoint filtering.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (controlling data export channels) and `ISM-1585` (blocking unauthorised cloud egress). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Open the tenant baseline DLP policy in the Power Platform admin centre (**Policies** > **Data policies**).
2. Move HTTP, HTTP Webhook, FTP, SFTP - SSH, Gmail, Outlook.com, Dropbox, Google Drive and social media connectors to the **Blocked** group.
3. Under **Custom connector patterns**, set `*` to **Blocked** and add allow-list patterns only for approved internal API domains.
4. Save and update the policy.

## How to verify

- **Automated**: Read tenant DLP policies via the read-only BAP API and assert that the required baseline high-risk connector identifiers appear in the `Blocked` connector group of an active tenant-wide or default-environment policy.
- **Manual**: Review the **Blocked** connector list and **Custom connector patterns** of every tenant DLP policy in the Power Platform admin centre.

## References

- [Data policies - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
