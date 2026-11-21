---
id: PP-CS-010
title: Govern Copilot Studio conversation transcript retention and Defender Agent 365 posture visibility
scope: tenant
workload: copilot-studio
severity: medium
recommended_value: Conversation transcript retention aligned with privacy/records policy, and Microsoft Defender AI agent inventory (AgentsInfo via Agent 365 where licensed) monitored for risky agents
rationale: Conversation transcripts can accumulate sensitive user prompts and AI responses in Dataverse; meanwhile, unmonitored agents lack unified posture visibility unless tracked via Power Platform inventory or Defender Agent 365.
ism_controls:
  - ISM-0585
  - ISM-0859
  - ISM-1585
essential_eight: []
configure_summary: Configure conversation transcript bulk-deletion retention in Dataverse and onboard Copilot Studio agent security to Microsoft Agent 365 (AgentsInfo) or Power Platform inventory.
verify_summary: Manual verification of Dataverse conversationtranscript bulk-delete jobs and Microsoft Defender XDR AgentsInfo inventory (or Power Platform inventory if Agent 365 is not licensed).
assessor_check_id: pp_cs_transcript_and_agent365_governance
automated: false
sentinel_rules: []
references:
  - title: View, export and manage conversation transcripts - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-transcripts-studio
  - title: Transition Microsoft Copilot Studio and Microsoft Foundry agent security capabilities to Microsoft Agent 365 | Microsoft Learn
    url: https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/transition-agent-security-to-agent-365
  - title: AI agent inventory in Microsoft Defender | Microsoft Learn
    url: https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-inventory
  - title: Power Platform inventory - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/power-platform-inventory
  - title: Engaging with artificial intelligence | cyber.gov.au
    url: https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-010: Govern Copilot Studio conversation transcript retention and Defender Agent 365 posture visibility

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Copilot Studio
- **Recommended value**:
  1. Review and configure the Dataverse `conversationtranscript` retention period (default 30 days) in each agent environment to match organisational privacy, FOI and records obligations, and restrict read permissions on `conversationtranscript` to authorised roles.
  2. Maintain a live inventory of all Copilot Studio agents, owners, knowledge sources and authentication modes using **Power Platform inventory** and, where licensed for **Microsoft Agent 365** (required from 1 July 2026 for Defender AI agent inventory and real-time runtime protection), query the unified `AgentsInfo` table in Microsoft Defender XDR Advanced Hunting (replacing the deprecated `AIAgentsInfo` table).
- **Assessor check ID**: `pp_cs_transcript_and_agent365_governance` (manual)

## Rationale

Copilot Studio stores user prompts and model responses in Dataverse `conversationtranscript` records by default, creating both a privacy/data-minimisation obligation and a forensic record. On the posture side, effective 1 July 2026 Microsoft requires a Microsoft Agent 365 licence for Defender AI agent security capabilities and replaced `AIAgentsInfo` with `AgentsInfo` (see [docs/research/verification.md](../../docs/research/verification.md)). Organisations without Agent 365 must rely on Power Platform inventory and the read-only assessor in this repository to maintain agent visibility.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0585` (monitoring security posture), `ISM-0859` (governing log and transcript retention) and `ISM-1585` (maintaining cloud AI asset inventory). Aligns with ASD's [Engaging with artificial intelligence](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence) and [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development). Verify against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. In each agent environment, review the Dataverse bulk-deletion job for `conversationtranscript` records and set retention to match organisational policy.
2. Confirm only authorised administrators or compliance reviewers hold read privilege on `conversationtranscript`.
3. Enable **Power Platform inventory** in the Power Platform admin centre to track all agents across environments.
4. Where licensed for Microsoft Agent 365, complete onboarding in the Microsoft Defender portal and migrate any saved Advanced Hunting queries from `AIAgentsInfo` to `AgentsInfo`.

## How to verify

- **Automated**: Manual governance review (`manual`) because transcript retention policy and Agent 365 licensing decisions are organisation-specific.
- **Manual**: Review Dataverse bulk-deletion rules for `conversationtranscript` and confirm agents appear in Power Platform inventory or Microsoft Defender XDR `AgentsInfo`.

## References

- [View, export and manage conversation transcripts - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-transcripts-studio)
- [Transition Microsoft Copilot Studio and Microsoft Foundry agent security capabilities to Microsoft Agent 365 | Microsoft Learn](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/transition-agent-security-to-agent-365)
- [AI agent inventory in Microsoft Defender | Microsoft Learn](https://learn.microsoft.com/en-us/defender-xdr/security-for-ai/ai-agent-inventory)
- [Power Platform inventory - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/power-platform-inventory)
- [Research verification record](../../docs/research/verification.md)
- [Engaging with artificial intelligence | cyber.gov.au](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
