---
id: PP-CS-008
title: Restrict Copilot Studio maker access and govern agent creation environments
scope: environment
workload: copilot-studio
severity: medium
recommended_value: Copilot Studio maker licences and Environment Maker role restricted to authorised makers inside dedicated, Managed Environments rather than the default environment
rationale: Unrestricted agent authoring in the default environment leads to shadow AI sprawl, unmonitored knowledge connections and inconsistent governance.
ism_controls:
  - ISM-0407
  - ISM-1405
  - ISM-1585
essential_eight:
  - Restrict administrative privileges
configure_summary: Assign Copilot Studio user licences via Entra groups, restrict Environment Maker permissions in production environments, and route makers to governed Copilot Studio environments.
verify_summary: Manual review of Copilot Studio licence assignment groups, Environment Maker security role members and default environment authoring controls.
assessor_check_id: pp_cs_maker_restrictions
automated: false
sentinel_rules: []
references:
  - title: Working with environments in Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/environments-first-run-experience
  - title: Security and governance in Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
  - title: Engaging with artificial intelligence | cyber.gov.au
    url: https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-008: Restrict Copilot Studio maker access and govern agent creation environments

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Copilot Studio
- **Recommended value**: Restrict Copilot Studio agent authoring to approved makers via Microsoft Entra group-based licence assignment, route makers out of the default environment (`PP-TEN-007`), and grant the **Environment Maker** and **Bot Author** Dataverse security roles only to trained makers inside dedicated, Managed Environments with environment security groups (`PP-ENV-001`).
- **Assessor check ID**: `pp_cs_maker_restrictions` (manual)

## Rationale

Every user granted a Copilot Studio author licence and Environment Maker role can create new agents, connect data sources and publish drafts. Restricting authoring privileges to governed environments ensures security review, DLP enforcement and Dataverse `bot` table auditing apply to every agent from creation.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (least-privilege authoring roles), `ISM-1405` (preventing shadow AI proliferation) and `ISM-1585` (cloud AI governance). Aligns with ASD's [Engaging with artificial intelligence](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Restrict administrative privileges](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Disable self-service Copilot Studio trials (`PP-TEN-003`) and assign **Microsoft Copilot Studio User License** strictly through an approved Microsoft Entra security group.
2. Create dedicated Managed Environments for Copilot Studio authoring and production hosting, each bound to a security group (`PP-ENV-001`).
3. Remove unnecessary **Environment Maker** assignments in production environments and promote agents via managed solutions.

## How to verify

- **Automated**: Manual governance review (`manual`) because verifying whether each maker group and licence assignment matches organisational approval requires HR and business-owner context.
- **Manual**: Audit Microsoft Entra licence assignment groups for Copilot Studio and review **Environment Maker** / **Bot Author** Dataverse security role memberships per environment.

## References

- [Working with environments in Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/environments-first-run-experience)
- [Security and governance in Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance)
- [Engaging with artificial intelligence | cyber.gov.au](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
