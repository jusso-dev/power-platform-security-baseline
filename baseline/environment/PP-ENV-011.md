---
id: PP-ENV-011
title: Configure extended backup retention for production environments
scope: environment
workload: dataverse
severity: high
recommended_value: Automated system backup retention set to 28 days on production Managed Environments with periodic restore testing
rationale: The default 7-day system backup window can be too short to detect and recover from delayed ransomware, insider mass record deletion or supply-chain corruption.
ism_controls:
  - ISM-1511
  - ISM-1515
essential_eight:
  - Regular backups
configure_summary: Power Platform admin centre > Environments > Select production Managed Environment > Backups > Change retention period to 28 days.
verify_summary: Read environment backupRetentionPeriodInDays via BAP API and assert it is set to 28 days for production environments.
assessor_check_id: pp_env_backup_retention_extended
automated: true
sentinel_rules:
  - Dataverse - Mass deletion of records
  - Power Apps - Multiple apps deleted
  - Power Automate - Unusual bulk deletion of flow resources
references:
  - title: Back up and restore environments - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
  - title: Essential Eight | cyber.gov.au
    url: https://www.cyber.gov.au/essential-eight
last_verified: "2026-11-21"
---

# PP-ENV-011: Configure extended backup retention for production environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Extend automated system backup retention (`backupRetentionPeriodInDays`) from the 7-day default to **28 days** on all production Managed Environments, take manual point-in-time backups before major releases, and periodically test restoring a backup to a sandbox environment.
- **Assessor check ID**: `pp_env_backup_retention_extended` (automated)

## Rationale

Microsoft retains automated Dataverse system backups for 7 days by default. Extending retention to 28 days on Managed Environments provides a much wider recovery window if mass record deletion, corrupted imports or malicious changes are discovered more than a week after the event.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-1511` (performing regular backups of important data and configuration) and `ISM-1515` (testing restoration of backups). Verify against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Directly supports [Regular backups](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Confirm the production environment is a Managed Environment.
2. In the Power Platform admin centre, go to **Manage** > **Environments** > select the environment.
3. Select **Backups** > **Change retention period**.
4. Choose **28 days** and select **Save**.
5. Schedule quarterly restore drills into a sandbox environment.

## How to verify

- **Automated**: Read `properties.backupRetentionPeriodInDays` (or backup configuration metadata) via the read-only BAP environments API and assert `>= 28` for production environments.
- **Manual**: Check **Backups** > **Retention period** in the Power Platform admin centre and verify restore test records.

## References

- [Back up and restore environments - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
- [Essential Eight | cyber.gov.au](https://www.cyber.gov.au/essential-eight)
