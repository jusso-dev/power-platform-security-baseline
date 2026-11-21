# power-platform-security-baseline

ASD Blueprint-style security baseline for Microsoft Power Platform and Copilot Studio, with a read-only assessor, Sentinel analytics rules and playbooks.

> **Status:** early build. Work is tracked in [issues](https://github.com/jusso-dev/power-platform-security-baseline/issues).

## Goal

Power Platform and Copilot Studio hold business data, connectors and automation, yet the ASD Blueprint for Secure Cloud has no Power Platform section. This repo fills that gap with:

1. **A baseline**: every tenant and environment setting that matters for security, written in the Blueprint's style (setting, recommended value, rationale, ISM and Essential Eight mapping, how to configure, how to verify).
2. **A read-only assessor**: a cross-platform tool that reads tenant and environment settings through supported admin APIs and reports pass, fail or manual for each baseline item. It never changes anything.
3. **Sentinel content**: analytics rules, hunting queries, a workbook and Logic Apps playbooks for Power Platform, Power Automate, Dataverse and Copilot Studio, built on the Microsoft Business Applications solution (3.2.5 or later) and the live tables PowerPlatformAdminActivity, the Power Automate activity table and DataverseActivity.

Research input from 21 Nov 2026 is in `docs/research/pp-sentinel-research.tsx`. Treat it as a starting point and re-verify every claim against Microsoft Learn before it lands in the baseline.

## Layout

```text
baseline/        Baseline items, one Markdown file per setting
assessor/        Read-only assessor (code, tests)
sentinel/        Analytics rules, hunting queries, workbook, playbooks (ARM/Bicep)
docs/            Guides, research input, architecture diagrams
```

## Related projects

- [microsoft-security-logging-guide](https://github.com/jusso-dev/microsoft-security-logging-guide): which Microsoft security logs matter and how to get them into Sentinel
- [soc-ready-logging](https://github.com/jusso-dev/soc-ready-logging)
- [junction](https://github.com/jusso-dev/junction): Microsoft API runtime (Graph, Defender, Sentinel)

## Disclaimer

This is an independent community project. It is not produced, endorsed or supported by the Australian Signals Directorate (ASD), the Australian Cyber Security Centre (ACSC) or Microsoft. References to ASD publications, the ISM and the Essential Eight point to the official sources; always check the current release.

## Licence

Code (assessor, KQL, templates, playbooks) is under the [MIT License](LICENSE). Documentation and baseline text are under [CC BY 4.0](LICENSE-docs).
