---
id: PP-ENV-014
title: Govern Dataverse application users, TDS SQL endpoint and Virtual Network integration
scope: environment
workload: dataverse
severity: high
recommended_value: Least-privilege security roles on application users, TDS endpoint disabled unless required, and Azure Virtual Network support enabled for sensitive private integrations
rationale: Over-privileged service principals (application users) and an exposed Tabular Data Stream (TDS) SQL endpoint enable silent, high-volume data extraction outside interactive MFA sessions.
ism_controls:
  - ISM-0445
  - ISM-1585
essential_eight:
  - Restrict administrative privileges
configure_summary: Review S2S application user security roles, disable the TDS endpoint under environment Features if unused, and configure Power Platform Virtual Network support for private data sources.
verify_summary: Manual review of Dataverse application users, custom security roles and VNet enterprise policy attachment, supplemented by Sentinel monitoring for TDS and application user anomalies.
assessor_check_id: pp_env_app_users_and_tds_governed
automated: false
sentinel_rules:
  - Dataverse - New non-interactive identity granted access
  - Dataverse - Anomalous application user activity
  - Dataverse - Suspicious use of TDS endpoint
references:
  - title: Manage application users in the Power Platform admin center | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users
  - title: Use SQL to query data (TDS endpoint) - Dataverse | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-sql-query
  - title: Virtual Network support overview - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/vnet-support-overview
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-014: Govern Dataverse application users, TDS SQL endpoint and Virtual Network integration

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**:
  1. Never assign the built-in `System Administrator` role to Dataverse application users (Microsoft Entra service principals) unless strictly required for automated CI/CD ALM pipelines; use minimal custom security roles instead.
  2. Disable the **TDS endpoint** (`Settings` > `Product` > `Features` > `TDS endpoint`) in environments that do not require read-only SQL/Power BI DirectQuery access.
  3. Use **Azure Virtual Network support** for Managed Environments that connect to internal APIs or private Azure services rather than exposing public endpoints.
- **Assessor check ID**: `pp_env_app_users_and_tds_governed` (manual)

## Rationale

Non-interactive application users authenticate via client secrets or certificates and bypass interactive user MFA prompts. If granted `System Administrator` or combined with an open TDS SQL endpoint, a leaked app credential permits bulk read or modification across the entire environment.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0445` (restricting privileged non-interactive accounts) and `ISM-1585` (hardening cloud API and network boundaries). Verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight).

## How to configure

1. In the Power Platform admin centre, select the environment > **Settings** > **Users + permissions** > **Application users** and review every registered app's security roles against least privilege.
2. Navigate to **Settings** > **Product** > **Features** and disable **TDS endpoint** where SQL querying is not required.
3. For sensitive integrations, configure a Power Platform Virtual Network enterprise policy following Microsoft Learn guidance.

## How to verify

- **Automated**: Manual governance review (`manual`) because determining whether each application user's custom security role or TDS usage is business-justified requires organisational context.
- **Manual**: Audit **Application users**, **Features** > **TDS endpoint**, and **Enterprise policies** (Virtual Network) quarterly, and enable the Sentinel rules `Dataverse - New non-interactive identity granted access`, `Dataverse - Anomalous application user activity`, and `Dataverse - Suspicious use of TDS endpoint`.

## References

- [Manage application users in the Power Platform admin center | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users)
- [Use SQL to query data (TDS endpoint) - Dataverse | Microsoft Learn](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-sql-query)
- [Virtual Network support overview - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/vnet-support-overview)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
