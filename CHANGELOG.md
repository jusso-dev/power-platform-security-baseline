# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-21

### Added

- **Research verification** (`docs/research/verification.md`): Verified Microsoft Business Applications (3.2.5+), Microsoft Copilot (3.0.2+ / 3.2.2), active tables (`PowerPlatformAdminActivity`, `PowerAutomateActivity`, `DataverseActivity`, `CopilotActivity`, `AgentsInfo`), retired tables (`PowerAppsActivity`, `PowerPlatformConnectorActivity`, `PowerPlatformDlpActivity`, `Dynamics365Activity`, `LLMActivity`, `AIAgentsInfo`), Sentinel Azure portal retirement (31 March 2027), and the Copilot Studio admin Sentinel logging gap.
- **Security baseline** (`baseline/`): JSON Schema (`baseline-item.schema.json`), Blueprint-style template (`_template.md`) and 38 verified baseline items mapped to ASD ISM controls, Essential Eight strategies and ASD AI security guidance:
  - 14 tenant-level items (`PP-TEN-001` to `PP-TEN-014`)
  - 14 environment-level and Dataverse items (`PP-ENV-001` to `PP-ENV-014`)
  - 10 Copilot Studio and AI agent items (`PP-CS-001` to `PP-CS-010`)
- **Read-only Python assessor** (`assessor/`, `pp-assessor` 1.0.0):
  - ADR 0001 documenting Python 3.11+, delegated and app-only least-privilege authentication, and read-only guardrails
  - GET-only `ReadOnlyHttpClient`, OAuth read-only scope validator, runtime and static AST read-only guard tests
  - 34 automated read-only checks covering every automatable tenant, environment, Dataverse and Copilot Studio item, plus explicit `manual` reporting for the 4 governance-only items
  - Per-run caching validated against a 50-environment scale test fixture
  - JSON, CSV and Markdown output formatters
- **Microsoft Sentinel content** (`sentinel/`):
  - 12 gap-closing scheduled analytics rules (YAML + ARM templates + synthetic KQL datatable tests) across Power Platform admin/DLP, Power Automate, Dataverse and Copilot Studio
  - 6 proactive hunting queries and noise tuning documentation (`TUNING.md`)
  - Power Platform Security Posture workbook (`PowerPlatformSecurityPosture.json` + ARM template + synthetic preview screenshot)
  - 4 Managed Identity Logic Apps playbooks (`PP-Notify-Admin-Team`, `PP-Disable-Risky-Flow`, `PP-Quarantine-Power-App`, `PP-Remove-User-Env-SecurityGroup`) with Deploy to Azure buttons
  - One-step combined Sentinel ARM deployment template (`sentinel/arm/all-in-one-sentinel-deployment.json`)
- **Architecture diagrams and CI/release tooling**:
  - Mermaid diagrams in `docs/architecture.md` for telemetry flow, read-only assessor pipeline and playbook response
  - CI pipeline enforcing style checks (no em dashes, no emojis), markdownlint, lychee link checking, baseline JSON Schema validation, Sentinel KQL/schema/ARM validation and assessor pytest suite
  - Release packaging script (`scripts/package_release.py`) and GitHub Actions release workflow (`.github/workflows/release.yml`)
