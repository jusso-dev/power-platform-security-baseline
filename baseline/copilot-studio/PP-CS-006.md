---
id: PP-CS-006
title: Enforce DLP controls on Copilot Studio skills, HTTP actions and plugin connectors
scope: tenant
workload: copilot-studio
severity: critical
recommended_value: Skills, HTTP requests and unapproved plugin/MCP connectors blocked by default in Copilot Studio DLP policies; connector action filtering restricts write actions where read-only suffices
rationale: Unrestricted agent tools and HTTP actions let prompt-injected or misconfigured agents invoke arbitrary external APIs, modify corporate records or exfiltrate conversation context.
ism_controls:
  - ISM-0263
  - ISM-1405
  - ISM-1585
essential_eight:
  - Application control
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Data policies > Block Copilot Studio Skills and HTTP request connectors, and enforce connector action controls on approved Business connectors.
verify_summary: Read tenant DLP policies via BAP API and confirm Skills in Copilot Studio and HTTP request connectors are classified as Blocked.
assessor_check_id: pp_cs_dlp_block_skills_and_http
automated: true
sentinel_rules:
  - Copilot - Plugin Created by Non-Admin User
  - Copilot - Plugin tampering
references:
  - title: Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
  - title: Security and governance in Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance
  - title: Guidelines for secure AI system development | cyber.gov.au
    url: https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-006: Enforce DLP controls on Copilot Studio skills, HTTP actions and plugin connectors

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Copilot Studio
- **Recommended value**: Place **Skills with Copilot Studio** (`shared_pva-skills`) and **HTTP requests in Copilot Studio** (alongside standard `shared_http`) in the **Blocked** group of tenant baseline DLP policies. Use Power Platform connector action filtering on allowed **Business** connectors so agents only receive explicitly approved actions rather than unrestricted write/delete operations.
- **Assessor check ID**: `pp_cs_dlp_block_skills_and_http` (automated)

## Rationale

Generative orchestration allows Copilot Studio agents to select and invoke registered actions, skills and connectors dynamically based on natural-language prompts. Blocking unapproved skills and raw HTTP requests prevents an agent from calling arbitrary external endpoints or chaining tools across trust boundaries.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (controlling egress channels), `ISM-1405` (restricting unauthorised external code/tool execution) and `ISM-1585` (least-privilege cloud AI tool execution). Aligns with ASD's [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development). Verify against the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [Application control](https://www.cyber.gov.au/essential-eight) and [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Open the Power Platform admin centre > **Policies** > **Data policies**.
2. Edit the tenant baseline policy and move **Skills with Copilot Studio**, **HTTP** and unapproved plugin connectors to **Blocked**.
3. For approved connectors in **Business**, select **Configure connector** > **Connector actions** and disallow high-impact write/delete actions where agents only require read access.
4. Save and update the policy.

## How to verify

- **Automated**: Read tenant DLP policies via the read-only BAP API and assert that `shared_pva-skills` (Skills with Copilot Studio) and `shared_http` are classified in the `Blocked` group of an active baseline policy.
- **Manual**: Review Copilot Studio connectors and connector action controls in **Policies** > **Data policies**.

## References

- [Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
- [Security and governance in Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/security-and-governance)
- [Guidelines for secure AI system development | cyber.gov.au](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
