---
id: PP-CS-005
title: Govern generative answers knowledge sources and restrict public web grounding
scope: tenant
workload: copilot-studio
severity: high
recommended_value: Knowledge sources for generative answers restricted via DLP; SharePoint/OneDrive grounding requires Entra ID authentication and untrusted public websites are blocked where indirect prompt injection is a risk
rationale: Grounding an agent on untrusted public websites alongside internal connectors creates an indirect prompt injection path where malicious web content can steer agent actions and leak internal data.
ism_controls:
  - ISM-0263
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Configure Copilot Studio knowledge source DLP connectors and disable unapproved public web search grounding in environments hosting internal agents.
verify_summary: Inspect tenant DLP policies via BAP API to verify Copilot Studio knowledge source connectors (public web search / unapproved knowledge sources) are governed.
assessor_check_id: pp_cs_dlp_restrict_knowledge_sources
automated: true
sentinel_rules:
  - Copilot - Jailbreak Attempt Detected
references:
  - title: Knowledge sources overview - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
  - title: Generative answers node - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-boost-node
  - title: Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
  - title: Guidelines for secure AI system development | cyber.gov.au
    url: https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-005: Govern generative answers knowledge sources and restrict public web grounding

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Copilot Studio
- **Recommended value**: Restrict generative answers knowledge sources via Power Platform data policies:
  1. Block **Knowledge sources with Bing Web Search in Copilot Studio** (or general public web grounding) in sensitive internal environments that have access to internal actions or connectors.
  2. Permit **Knowledge sources with SharePoint and OneDrive in Copilot Studio** only in **Business** alongside Microsoft Entra ID user authentication so SharePoint permissions are strictly trimmed per user.
  3. Block unapproved custom uploaded document grounding where data classification controls cannot be enforced.
- **Assessor check ID**: `pp_cs_dlp_restrict_knowledge_sources` (automated)

## Rationale

Combining untrusted external web content (Bing search or arbitrary public URLs) with internal enterprise connectors exposes agents to indirect prompt injection (cross-prompt injection attacks), where hidden instructions on a web page trick the model into invoking tools or exfiltrating sensitive internal data.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (preventing unauthorised data egress via AI intermediaries) and `ISM-1585` (enforcing cloud AI input/output trust boundaries). Directly aligns with ASD's [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development) on defending against prompt injection and data poisoning. Verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. In the Power Platform admin centre, go to **Policies** > **Data policies** and edit the policy covering sensitive/internal environments.
2. Place **Knowledge sources with Bing Web Search in Copilot Studio** (and other unapproved external knowledge connectors) into **Blocked**.
3. Keep **Knowledge sources with SharePoint and OneDrive in Copilot Studio** in **Business** only in environments enforcing Entra ID agent authentication (`PP-CS-001` and `PP-CS-002`).
4. In Copilot Studio agent settings, disable **Allow the AI to use its own general knowledge** where factual grounding strictly on internal sources is required.

## How to verify

- **Automated**: Read tenant DLP policies via the read-only BAP API and assert that unapproved public web knowledge source connectors (`shared_pva-knowledge-bing` or equivalent Copilot Studio knowledge connectors) are classified as `Blocked` in baseline policies.
- **Manual**: Review knowledge source connectors in **Policies** > **Data policies** and audit agent **Knowledge** tabs in Copilot Studio.

## References

- [Knowledge sources overview - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio)
- [Generative answers node - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-boost-node)
- [Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
- [Guidelines for secure AI system development | cyber.gov.au](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
