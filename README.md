# power-platform-security-baseline

ASD Blueprint-style security baseline for Microsoft Power Platform and Copilot Studio, with a read-only assessor, Sentinel analytics rules and playbooks.

> **Status:** v1.0.0 ready. See [CHANGELOG.md](CHANGELOG.md) and [issues](https://github.com/jusso-dev/power-platform-security-baseline/issues).

## Goal

Power Platform and Copilot Studio hold business data, connectors and automation, yet the ASD Blueprint for Secure Cloud has no Power Platform section. This repo fills that gap with:

1. **A baseline (`baseline/`)**: 38 tenant, environment, Dataverse and Copilot Studio settings written in the Blueprint's style (setting, recommended value, rationale, ISM and Essential Eight mapping, how to configure, how to verify), validated against a JSON Schema in CI.
2. **A read-only assessor (`assessor/`)**: a cross-platform Python CLI (`pp-assessor`) that reads tenant and environment settings through supported GET-only admin APIs (or offline JSON fixtures) and reports `pass`, `fail` or `manual` in JSON, CSV and Markdown. It never changes anything.
3. **Sentinel content (`sentinel/`)**: 12 gap-closing analytics rules (YAML + ARM + KQL datatable tests), 6 hunting queries, a security posture workbook and 4 Managed Identity Logic Apps playbooks built on the Microsoft Business Applications solution (3.2.5 or later) and current tables (`PowerPlatformAdminActivity`, `PowerAutomateActivity`, `DataverseActivity`, `CopilotActivity`).

Research verification against Microsoft Learn and `Azure/Azure-Sentinel` (21 November 2026) is recorded in [docs/research/verification.md](docs/research/verification.md).

## Quick start

### 1. Run the read-only assessor against an offline fixture

```bash
git clone https://github.com/jusso-dev/power-platform-security-baseline.git
cd power-platform-security-baseline

python3 -m venv .venv
source .venv/bin/activate
pip install ./assessor

pp-assessor assess \
  --fixture assessor/tests/fixtures/environments_full.json \
  --format all \
  --output ./assessment-report
```

This writes `report.json`, `report.csv` and `report.md` inside `./assessment-report` without connecting to any live tenant. For live read-only assessment using delegated device code or app-only credentials, see [assessor/README.md](assessor/README.md) and [docs/adr/0001-assessor-language-and-auth.md](docs/adr/0001-assessor-language-and-auth.md).

### 2. Deploy Sentinel rules and workbook in one step

Prerequisites: install **Microsoft Business Applications 3.2.5+** and **Microsoft Copilot 3.0.2+** from Content Hub in the [Microsoft Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal) (Azure portal Sentinel retires on **31 March 2027**).

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjusso-dev%2Fpower-platform-security-baseline%2Fmain%2Fsentinel%2Farm%2Fall-in-one-sentinel-deployment.json)

See [sentinel/README.md](sentinel/README.md) for hunting queries, noise tuning notes and [sentinel/playbooks/README.md](sentinel/playbooks/README.md) for individual Managed Identity Logic Apps playbooks.

## Architecture

See [docs/architecture.md](docs/architecture.md) for Mermaid diagrams showing:

- Power Platform, Dataverse and Copilot Studio telemetry flow into Microsoft Sentinel (Defender portal)
- How the read-only Python assessor authenticates and reads settings via GET-only APIs
- Managed Identity Logic Apps incident response playbook flow

## Layout

```text
baseline/        38 baseline items (tenant, environment, copilot-studio), schema and template
assessor/        Read-only Python assessor CLI, checks, guard tests and fixtures
sentinel/        Analytics rules, hunting queries, workbook, playbooks (ARM) and KQL tests
docs/            Architecture diagrams, ADR 0001, branch protection and research verification
scripts/         Style, baseline schema, Sentinel validation, ARM builder and release packager
```

## Related projects

- [microsoft-security-logging-guide](https://github.com/jusso-dev/microsoft-security-logging-guide): which Microsoft security logs matter and how to get them into Sentinel
- [soc-ready-logging](https://github.com/jusso-dev/soc-ready-logging)
- [junction](https://github.com/jusso-dev/junction): Microsoft API runtime (Graph, Defender, Sentinel)

## Disclaimer

This is an independent community project. It is not produced, endorsed or supported by the Australian Signals Directorate (ASD), the Australian Cyber Security Centre (ACSC) or Microsoft. References to ASD publications, the ISM and the Essential Eight point to the official sources; always check the current release.

## Licence

Code (assessor, KQL, templates, playbooks) is under the [MIT License](LICENSE). Documentation and baseline text are under [CC BY 4.0](LICENSE-docs).
