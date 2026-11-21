# Environment-level baseline items

This directory contains 14 environment-level security baseline items for Microsoft Power Platform and Dataverse.

| ID | Title | Severity | Automated | Assessor check ID |
| --- | --- | --- | --- | --- |
| [PP-ENV-001](PP-ENV-001.md) | Assign a Microsoft Entra security group to every non-default environment | High | Yes | `pp_env_security_group_assigned` |
| [PP-ENV-002](PP-ENV-002.md) | Enable Dataverse auditing and user access logging in production environments | Critical | Yes | `pp_env_dataverse_auditing_enabled` |
| [PP-ENV-003](PP-ENV-003.md) | Enable Dataverse read auditing on sensitive production environments | Medium | Yes | `pp_env_dataverse_read_auditing` |
| [PP-ENV-004](PP-ENV-004.md) | Enable Dataverse SAS logging to Microsoft Purview | Medium | Yes | `pp_env_sas_logging_purview` |
| [PP-ENV-005](PP-ENV-005.md) | Configure explicit Dataverse audit log retention period | Medium | Yes | `pp_env_audit_retention_configured` |
| [PP-ENV-006](PP-ENV-006.md) | Enable Dataverse IP firewall on sensitive Managed Environments | High | Yes | `pp_env_ip_firewall_enabled` |
| [PP-ENV-007](PP-ENV-007.md) | Enable IP address-based cookie binding in Dataverse | High | Yes | `pp_env_cookie_binding_enabled` |
| [PP-ENV-008](PP-ENV-008.md) | Enforce explicit user session and inactivity timeouts | Medium | Yes | `pp_env_session_timeout_configured` |
| [PP-ENV-009](PP-ENV-009.md) | Enforce canvas app and solution flow sharing limits in Managed Environments | High | Yes | `pp_env_sharing_limits_configured` |
| [PP-ENV-010](PP-ENV-010.md) | Enforce Solution Checker in Block mode on production Managed Environments | Medium | Yes | `pp_env_solution_checker_block` |
| [PP-ENV-011](PP-ENV-011.md) | Configure extended backup retention for production environments | High | Yes | `pp_env_backup_retention_extended` |
| [PP-ENV-012](PP-ENV-012.md) | Enable Microsoft Customer Lockbox for Managed Environments | Medium | Yes | `pp_env_customer_lockbox_enabled` |
| [PP-ENV-013](PP-ENV-013.md) | Maintain strict blocked file extensions in Dataverse attachment settings | High | Yes | `pp_env_blocked_file_extensions` |
| [PP-ENV-014](PP-ENV-014.md) | Govern Dataverse application users, TDS SQL endpoint and Virtual Network integration | High | No (Manual) | `pp_env_app_users_and_tds_governed` |
