# Copilot Studio and agent baseline items

This directory contains 10 security baseline items for Microsoft Copilot Studio and AI agents, mapped to ASD ISM controls and ASD AI security guidance ([Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development) and [Engaging with artificial intelligence](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence)).

> **Logging gap notice**: Microsoft Purview documents Copilot Studio maker/admin events (`BotCreate`, `BotDelete`, `BotUpdateOperation-*`), but Microsoft does not document a dedicated Sentinel table that receives them. Preventive data policies (`PP-CS-002`, `PP-CS-003`, `PP-CS-005`, `PP-CS-006`) and Dataverse `bot` table auditing (`PP-CS-009`) are therefore essential. See [docs/research/verification.md](../../docs/research/verification.md).

| ID | Scope | Title | Severity | Automated | Assessor check ID |
| --- | --- | --- | --- | --- | --- |
| [PP-CS-001](PP-CS-001.md) | Environment | Require Microsoft Entra ID end-user authentication on Copilot Studio agents | Critical | Yes | `pp_cs_agent_auth_required` |
| [PP-CS-002](PP-CS-002.md) | Tenant | Block unauthenticated Copilot Studio chat via Power Platform data policies | Critical | Yes | `pp_cs_dlp_block_no_auth_chat` |
| [PP-CS-003](PP-CS-003.md) | Tenant | Restrict Copilot Studio publishing channels via data policies | High | Yes | `pp_cs_dlp_restrict_channels` |
| [PP-CS-004](PP-CS-004.md) | Environment | Enforce web channel security on Copilot Studio agents using web or Direct Line | High | Yes | `pp_cs_web_channel_security` |
| [PP-CS-005](PP-CS-005.md) | Tenant | Govern generative answers knowledge sources and restrict public web grounding | High | Yes | `pp_cs_dlp_restrict_knowledge_sources` |
| [PP-CS-006](PP-CS-006.md) | Tenant | Enforce DLP controls on Copilot Studio skills, HTTP actions and plugin connectors | Critical | Yes | `pp_cs_dlp_block_skills_and_http` |
| [PP-CS-007](PP-CS-007.md) | Environment | Restrict Copilot Studio agent sharing limits in Managed Environments | High | Yes | `pp_cs_agent_sharing_limits` |
| [PP-CS-008](PP-CS-008.md) | Environment | Restrict Copilot Studio maker access and govern agent creation environments | Medium | No (Manual) | `pp_cs_maker_restrictions` |
| [PP-CS-009](PP-CS-009.md) | Environment | Enable Dataverse bot table auditing and CopilotActivity ingestion | Critical | Yes | `pp_cs_audit_and_sentinel_coverage` |
| [PP-CS-010](PP-CS-010.md) | Tenant | Govern Copilot Studio conversation transcript retention and Defender Agent 365 posture visibility | Medium | No (Manual) | `pp_cs_transcript_and_agent365_governance` |
