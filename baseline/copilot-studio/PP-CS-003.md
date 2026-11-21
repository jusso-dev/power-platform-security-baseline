---
id: PP-CS-003
title: Restrict Copilot Studio publishing channels via data policies
scope: tenant
workload: copilot-studio
severity: high
recommended_value: Direct Line, Omnichannel, Facebook and custom website channels are blocked by default in tenant DLP policies; only approved internal channels (Teams and Microsoft 365 Copilot) are permitted
rationale: Unrestricted publishing channels let makers expose internal AI agents on public websites or consumer messaging platforms outside corporate network and identity controls.
ism_controls:
  - ISM-0263
  - ISM-1585
essential_eight:
  - User application hardening
configure_summary: Power Platform admin centre > Policies > Data policies > Block Direct Line channels, Facebook and unapproved Copilot Studio channels; allow Microsoft Teams + Microsoft 365 Copilot only where approved.
verify_summary: Inspect tenant DLP policies via BAP API and verify unapproved Copilot Studio channel connectors (Direct Line, Facebook) are classified as Blocked.
assessor_check_id: pp_cs_dlp_restrict_channels
automated: true
sentinel_rules: []
references:
  - title: Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention
  - title: Publish an agent to channels - Microsoft Copilot Studio | Microsoft Learn
    url: https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels
  - title: Engaging with artificial intelligence | cyber.gov.au
    url: https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-CS-003: Restrict Copilot Studio publishing channels via data policies

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Copilot Studio
- **Recommended value**: Use Power Platform data policies to **Block** external and unmanaged Copilot Studio channels (**Direct Line channels in Copilot Studio**, **Facebook in Copilot Studio**, **Omnichannel in Copilot Studio** where unused) across default and internal environments, permitting only **Microsoft Teams + Microsoft 365 Copilot** (`Microsoft Teams + Microsoft 365`) for authenticated internal use.
- **Assessor check ID**: `pp_cs_dlp_restrict_channels` (automated)

## Rationale

Publishing an internal agent to Direct Line or social messaging channels opens an external attack surface for prompt injection, sensitive data disclosure and credential phishing. Restricting publishing channels via DLP limits exposure strictly to authenticated corporate channels.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0263` (restricting external communication channels) and `ISM-1585` (hardening cloud AI publishing surfaces). Aligns with ASD's [Engaging with artificial intelligence](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence). Check the latest [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: Supports [User application hardening](https://www.cyber.gov.au/essential-eight).

## How to configure

1. In the Power Platform admin centre, open **Policies** > **Data policies** and edit the tenant baseline policy.
2. Move **Direct Line channels in Copilot Studio** and **Facebook in Copilot Studio** into **Blocked**.
3. Keep **Microsoft Teams + Microsoft 365 in Copilot Studio** in **Business** where internal Teams/M365 Copilot agents are approved.
4. Save changes.

## How to verify

- **Automated**: Inspect tenant DLP policies via the read-only BAP API and confirm Copilot Studio external channel connectors (`shared_pva-directline`, `shared_pva-facebook`) are classified as `Blocked`.
- **Manual**: Review Copilot Studio connectors in **Policies** > **Data policies** and verify channel settings on published agents.

## References

- [Configure data policies for agents - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
- [Publish an agent to channels - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels)
- [Engaging with artificial intelligence | cyber.gov.au](https://www.cyber.gov.au/publication/engaging-with-artificial-intelligence)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
