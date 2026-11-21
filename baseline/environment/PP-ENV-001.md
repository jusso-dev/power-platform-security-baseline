---
id: PP-ENV-001
title: Assign a Microsoft Entra security group to every non-default environment
scope: environment
workload: dataverse
severity: high
recommended_value: Non-empty securityGroupId assigned to every non-default environment
rationale: Without an environment security group, every licensed user in the tenant is synchronised into Dataverse and can potentially access apps or records if overly broad sharing or security roles occur.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - Restrict administrative privileges
configure_summary: Power Platform admin centre > Manage > Environments > Select environment > Edit > Assign a dedicated Microsoft Entra security group.
verify_summary: Read each non-default environment via the BAP API and verify properties.linkedEnvironmentMetadata.securityGroupId is a non-empty, non-zero GUID.
assessor_check_id: pp_env_security_group_assigned
automated: true
sentinel_rules:
  - C1 - Tenant isolation disabled or environment security group changed
  - Dataverse - Guest user exfiltration following Power Platform defense impairment
references:
  - title: Control user access to environments with security groups and licenses - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/control-user-access
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-ENV-001: Assign a Microsoft Entra security group to every non-default environment

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Dataverse
- **Recommended value**: Bind every non-default environment (production, sandbox and developer) to a dedicated Microsoft Entra security group (`securityGroupId` set to a valid group GUID, not `00000000-0000-0000-0000-000000000000`). Note that the default environment cannot have a security group assigned.
- **Assessor check ID**: `pp_env_security_group_assigned` (automated)

## Rationale

When no security group is assigned to an environment with a Dataverse database, all licensed Microsoft Entra users are added as users in that environment. Assigning a security group restricts environment entry strictly to group members and limits blast radius if an app or record is shared broadly.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (enforcing need-to-know access control) and `ISM-1585` (isolating cloud environment access). Verify against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight) by bounding who can enter sensitive environments.

## How to configure

1. Create a dedicated Microsoft Entra security group for the environment's authorised users.
2. Open the Power Platform admin centre > **Manage** > **Environments** and select the environment.
3. Select **Edit** under **Details**, select **Security group**, choose the group and save.

## How to verify

- **Automated**: Inspect `properties.linkedEnvironmentMetadata.securityGroupId` on each non-default environment returned by the read-only BAP environments endpoint and confirm it is present and not the all-zeros GUID.
- **Manual**: Check **Details** > **Security group** on each non-default environment in the Power Platform admin centre.

## References

- [Control user access to environments with security groups and licenses - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/control-user-access)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
