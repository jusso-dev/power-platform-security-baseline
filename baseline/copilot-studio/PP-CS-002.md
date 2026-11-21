---
id: PP-CS-002
title: Block unauthenticated Copilot Studio chat via Power Platform data policies
scope: tenant
workload: copilot-studio
severity: critical
recommended_value: The 'Chat without Microsoft Entra ID authentication in Copilot Studio' DLP connector is placed in the Blocked group across tenant DLP policies
rationale: Preventive DLP enforcement stops makers from publishing anonymous Copilot Studio agents before they ever go live, closing the gap created by limited Sentinel admin logging for Copilot Studio.
ism_controls:
  - ISM-0407
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Data policies > Move 'Chat without Microsoft Entra ID authentication in Copilot Studio' to Blocked.
verify_summary: Inspect tenant DLP policies via BAP API and confirm the Copilot Studio no-authentication connector is classified in Blocked.
assessor_check_id: pp_cs_dlp_block_no_auth_chat
automated: true
sentinel_rules:
  - C9 - Copilot Studio agent configured with No authentication
references:
  - title: Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
  - title: Guidelines for secure AI system development | cyber.gov.au
    url: https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-002: Block unauthenticated Copilot Studio chat via Power Platform data policies

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Copilot Studio
- **Recommended value**: Place the Copilot Studio governance connector **Chat without Microsoft Entra ID authentication in Copilot Studio** (`shared_pva-no-auth` / `Chat without Microsoft Entra ID authentication`) in the **Blocked** group of the tenant baseline DLP policy covering all internal environments.
- **Assessor check ID**: `pp_cs_dlp_block_no_auth_chat` (automated)

## Rationale

Prevention is significantly stronger than post-hoc detection for Copilot Studio, particularly because Microsoft does not document a dedicated Sentinel table for Copilot Studio maker/admin Purview audit events. Blocking unauthenticated chat in a data policy prevents any maker from publishing an agent without Microsoft Entra ID authentication.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0407` (enforcing authentication by policy) and `ISM-1585` (preventive cloud governance controls). Aligns with ASD's [Guidelines for secure AI system development](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development) (secure by default). Check the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. Open the Power Platform admin centre > **Policies** > **Data policies**.
2. Edit the tenant baseline DLP policy (or create a policy scoped to all environments except explicitly approved public-website environments).
3. Search for **Chat without Microsoft Entra ID authentication in Copilot Studio** and move it to **Blocked**.
4. Save and update the policy.

## How to verify

- **Automated**: Read tenant DLP policies via the read-only BAP API and assert that the Copilot Studio unauthenticated chat connector appears in the `Blocked` connector group of an active tenant-wide policy.
- **Manual**: Review **Policies** > **Data policies** in the Power Platform admin centre and confirm the connector is blocked.

## References

- [Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
- [Guidelines for secure AI system development | cyber.gov.au](https://www.cyber.gov.au/publication/guidelines-for-secure-ai-system-development)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
