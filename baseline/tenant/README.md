# Tenant-level baseline items

This directory contains 14 tenant-level security baseline items for Microsoft Power Platform.

| ID | Title | Severity | Automated | Assessor check ID |
| --- | --- | --- | --- | --- |
| [PP-TEN-001](PP-TEN-001.md) | Restrict production and sandbox environment creation to administrators | High | Yes | `pp_ten_restrict_prod_env_creation` |
| [PP-TEN-002](PP-TEN-002.md) | Restrict trial environment creation to administrators | Medium | Yes | `pp_ten_restrict_trial_env_creation` |
| [PP-TEN-003](PP-TEN-003.md) | Disable self-service product trials and purchases for Power Platform | Medium | Yes | `pp_ten_disable_self_service_purchases` |
| [PP-TEN-004](PP-TEN-004.md) | Enable tenant isolation for cross-tenant connector connections | Critical | Yes | `pp_ten_tenant_isolation_enabled` |
| [PP-TEN-005](PP-TEN-005.md) | Apply a restrictive Data Loss Prevention policy to the default environment | Critical | Yes | `pp_ten_default_env_dlp_policy` |
| [PP-TEN-006](PP-TEN-006.md) | Block high-risk HTTP, file transfer and consumer connectors in tenant DLP baseline | Critical | Yes | `pp_ten_dlp_blocks_high_risk_connectors` |
| [PP-TEN-007](PP-TEN-007.md) | Enable default environment routing for new makers | Medium | Yes | `pp_ten_default_env_routing` |
| [PP-TEN-008](PP-TEN-008.md) | Activate Managed Environments on production and default environments | High | Yes | `pp_ten_managed_environments_enabled` |
| [PP-TEN-009](PP-TEN-009.md) | Restrict guest user access and external sharing in Power Platform | High | Yes | `pp_ten_guest_access_restricted` |
| [PP-TEN-010](PP-TEN-010.md) | Restrict Power Platform and Dynamics 365 Administrator roles with PIM | Critical | Yes | `pp_ten_admin_role_least_privilege` |
| [PP-TEN-011](PP-TEN-011.md) | Configure Customer-Managed Keys for sensitive production environments | Medium | Yes | `pp_ten_cmk_configured` |
| [PP-TEN-012](PP-TEN-012.md) | Enable tenant-level analytics and capacity monitoring | Low | Yes | `pp_ten_tenant_level_analytics` |
| [PP-TEN-013](PP-TEN-013.md) | Organise Managed Environments into environment groups with baseline rules | Medium | Yes | `pp_ten_environment_groups_configured` |
| [PP-TEN-014](PP-TEN-014.md) | Enable Microsoft Purview auditing and Sentinel Business Applications ingestion | Critical | No (Manual) | `pp_ten_purview_audit_enabled` |
