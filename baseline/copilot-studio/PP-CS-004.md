---
id: PP-CS-004
title: Enforce web channel security on Copilot Studio agents using web or Direct Line
scope: environment
workload: copilot-studio
severity: high
recommended_value: Web channel security (Require secured access) enabled on every agent published to web or custom Direct Line channels
rationale: Without web channel security enabled, anyone who discovers an agent's embedded bot identifier or public token endpoint can initiate unauthorised conversations from arbitrary origins.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Copilot Studio > Agent > Settings > Security > Web channel security > Enable Require secured access and exchange Direct Line secrets server-side only.
verify_summary: Read Dataverse bot configuration via GET /api/data/v9.2/bots and confirm web channel security (isWebChannelSecurityEnabled / directLineSecurity) is enabled on bots exposing web channels.
assessor_check_id: pp_cs_web_channel_security
automated: true
sentinel_rules: []
references:
  - title: Configure web channel security - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-web-security
  - title: Guidelines for secure AI system development | cyber.gov.au
    url: https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-004: Enforce web channel security on Copilot Studio agents using web or Direct Line

## Setting and recommended value

- **Scope**: Environment
- **Workload**: Copilot Studio
- **Recommended value**: Where an exception permits publishing an agent to a custom website or Direct Line channel, enable **Web channel security** (`Require secured access`) so clients must present a short-lived Direct Line token generated server-side using a protected secret, rather than connecting anonymously via an embedded URL.
- **Assessor check ID**: `pp_cs_web_channel_security` (automated)

## Rationale

Standard unauthenticated web embed snippets expose the agent endpoint directly in client-side HTML. Enabling Web channel security prevents unauthorised third-party sites from embedding or abusing the agent and ensures secrets are never placed in browser JavaScript.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (preventing unauthorised client invocation) and `ISM-1585` (securing web-exposed cloud endpoints). Aligns with ASD's [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development). Verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Open the agent in Microsoft Copilot Studio.
2. Go to **Settings** > **Security** > **Web channel security**.
3. Turn **Require secured access** to **On** and select **Save**.
4. Store the generated Direct Line secret in Azure Key Vault and exchange it for a short-lived token in your backend web service.

## How to verify

- **Automated**: Read active bots from Dataverse (`GET <instanceUrl>/api/data/v9.2/bots`) and check that any bot with web/Direct Line channels configured enforces `webChannelSecurityEnabled` (in `configuration` JSON).
- **Manual**: Inspect **Settings** > **Security** > **Web channel security** for each web-published agent.

## References

- [Configure web channel security - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-web-security)
- [Guidelines for secure AI system development | cyber.gov.au](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
