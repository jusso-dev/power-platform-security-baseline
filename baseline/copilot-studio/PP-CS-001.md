---
id: PP-CS-001
title: Require Microsoft Entra ID end-user authentication on Copilot Studio agents
scope: environment
workload: copilot-studio
severity: critical
recommended_value: Every Copilot Studio agent uses Authenticate with Microsoft (Entra ID) or approved manual OAuth2; No authentication is prohibited for internal agents
rationale: Agents configured with No authentication allow unauthenticated users to invoke topics, connectors and generative answers, exposing internal knowledge sources to anonymous queries and prompt injection.
ism_controls:
  - ISM-0407
  - ISM-1507
  - ISM-1585
essential_eight:
  - Multi-factor authentication
configure_summary: Copilot Studio > Agent > Settings > Security > Authentication > Select Authenticate with Microsoft (or approved Authenticate manually with Entra ID).
verify_summary: Query the Dataverse bot table via GET /api/data/v9.2/bots and confirm no active bot uses authenticationmode 1 (No authentication).
assessor_check_id: pp_cs_agent_auth_required
automated: true
sentinel_rules:
  - C9 - Copilot Studio agent configured with No authentication
references:
  - title: Configure user authentication in Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication
  - title: Security and governance in Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
  - title: Guidelines for secure AI system development | cyber.gov.au
    url: https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-001: Require Microsoft Entra ID end-user authentication on Copilot Studio agents

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Copilot Studio
- **Recommended value**: Configure every internal Copilot Studio agent to use **Authenticate with Microsoft** (`authenticationmode` set to Entra ID / Teams authentication) or explicitly approved **Authenticate manually** with Microsoft Entra ID OAuth 2.0 and `Require users to sign in` enabled. Never permit **No authentication** (`authenticationmode == 1`) on agents with access to corporate knowledge or actions.
- **Assessor check ID**: `pp_cs_agent_auth_required` (automated)

## Rationale

When an agent is published with **No authentication**, SharePoint and Dataverse delegated security trimming cannot apply and anyone reaching the endpoint can interact with the agent anonymously. Enforcing Microsoft Entra ID authentication ensures Conditional Access, MFA and user-level access control are preserved across every interaction.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (enforcing authenticated access), `ISM-1507` (MFA for enterprise cloud services) and `ISM-1585` (securing cloud AI endpoints). Aligns with ASD's [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development) (secure deployment and access control). Always verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Multi-factor authentication](https://www.cyber.gov.au/essential-eight) when enforced via Microsoft Entra ID Conditional Access.

## How to configure

1. Open the agent in Microsoft Copilot Studio.
2. Go to **Settings** > **Security** > **Authentication**.
3. Select **Authenticate with Microsoft** (for Teams, Power Apps and M365 Copilot channels) or **Authenticate manually** bound to an approved Microsoft Entra app registration with **Require users to sign in** enabled.
4. Republish the agent and enforce preventive blocking via `PP-CS-002`.

## How to verify

- **Automated**: Call the read-only Dataverse Web API (`GET <instanceUrl>/api/data/v9.2/bots?$select=botid,name,authenticationmode,authenticationtrigger,statecode`) and verify no active bot (`statecode == 0`) has `authenticationmode == 1` (No authentication).
- **Manual**: Review **Settings** > **Security** > **Authentication** for each published agent in Copilot Studio.

## References

- [Configure user authentication in Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication)
- [Security and governance in Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance)
- [Guidelines for secure AI system development | cyber.gov.au](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
