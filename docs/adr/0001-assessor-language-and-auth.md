# ADR 0001: Assessor implementation language, authentication and read-only architecture

- **Status**: Accepted
- **Date**: 2026-11-21
- **Issue**: #7

## Context

The repository requires a cross-platform, read-only security assessor that inspects Microsoft Power Platform, Dataverse and Copilot Studio tenant and environment settings against the Markdown baseline under `baseline/` and outputs JSON, CSV and Markdown reports.

Two candidate runtimes were considered: PowerShell 7 and Python 3.11+.

## Decision

### 1. Implementation language: Python 3.11+

We selected **Python 3.11+** calling documented Microsoft REST APIs directly (`api.bap.microsoft.com`, `api.powerplatform.com`, `graph.microsoft.com`, and per-environment Dataverse Web API `https://<org>.crm.dynamics.com/api/data/v9.2/`).

Reasons:

- **True cross-platform parity**: Several legacy Power Platform administration PowerShell modules (`Microsoft.PowerApps.Administration.PowerShell`) still carry Windows PowerShell 5.1 dependencies or limited macOS/Linux support, whereas Python calling REST APIs works identically on Linux, macOS, Windows and GitHub Actions runners.
- **Minimal dependency footprint**: Python's standard library provides HTTP (`urllib.request`), JSON, CSV, `argparse`, `dataclasses` and `ast` (enabling static read-only guard tests without heavy external tooling). Only `pyyaml` is required at runtime to load baseline front matter, with `msal` as an optional extra for live Microsoft Entra ID authentication.
- **Single tooling stack**: Repository style validation (`scripts/check_style.py`) and baseline JSON Schema validation (`scripts/validate_baseline.py`) already use Python, simplifying CI and contributor onboarding.

### 2. Authentication and least-privilege read-only permissions

The assessor supports three execution modes through a `TokenProvider` interface:

1. **Offline fixture mode (`--fixture <file>`)**: Evaluates a JSON snapshot of API responses without any network traffic or tenant credentials. Used by default in unit tests, CI and air-gapped reviews.
2. **Delegated interactive / device-code mode (`--auth delegated`)**: Uses Microsoft Authentication Library (MSAL) public client device-code flow so an auditor signs in interactively with a least-privileged reader identity (for example Power Platform read-only admin scope plus Microsoft Entra Global Reader or Security Reader).
3. **App-only service principal mode (`--auth app-only`)**: Uses MSAL confidential client credentials (certificate or federated workload identity preferred over client secrets) for unattended CI or scheduled posture audits.

Required read-only permissions (no `.ReadWrite.` permissions are requested or accepted):

- **Power Platform Admin API (`https://api.bap.microsoft.com/.default`)**: Service principal registered as a Power Platform management application or delegated user with read access to tenant settings, DLP policies, tenant isolation, enterprise policies, environment groups and environments ([Power Platform API overview](https://learn.microsoft.com/en-us/rest/api/power-platform/)).
- **Microsoft Graph (`https://graph.microsoft.com/.default` or delegated read scopes)**:
  - `Policy.Read.All` (read external collaboration / authorisation policy for guest restrictions)
  - `RoleManagement.Read.Directory` (count standing Power Platform Administrator and Dynamics 365 Administrator role assignments)
  - `Directory.Read.All` (resolve tenant metadata)
- **Dataverse Web API (`https://<org>.crm.dynamics.com/.default`)**: Application user or delegated auditor granted a minimal custom read-only Dataverse security role with Read privilege on the `organization` and `bot` tables only ([Manage application users](https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users)).

### 3. Defence-in-depth read-only enforcement

To guarantee the assessor can never mutate tenant configuration:

- `ReadOnlyHttpClient` only accepts HTTP `GET` and raises `ReadOnlyViolationError` if any other HTTP method is requested.
- `validate_read_only_scopes` rejects any Microsoft Graph scope containing `Write` or `ReadWrite`.
- Automated CI tests (`assessor/tests/test_read_only_guard.py`) perform both runtime checks and an Abstract Syntax Tree (AST) scan over every Python module in `assessor/src/` to fail the build if any HTTP write verb (`POST`, `PUT`, `PATCH`, `DELETE`) is introduced.

### 4. Output formats

Every assessment produces identical structured findings renderable as:

- **JSON**: Machine-readable schema suitable for SIEM ingestion (for example into a Sentinel custom table) or automated diffing.
- **CSV**: Flat tabular export for spreadsheets, GRC tools and audit evidence packs.
- **Markdown**: Human-readable report in ASD Blueprint style (plain Australian English, no em dashes, no emojis).

## Consequences

- Live tenant runs require registering a read-only Entra application or using delegated sign-in with MSAL (`pip install -e "assessor[live]"`).
- Checks for settings without a supported read-only API (such as Purview Audit activation or bespoke application user role reviews) are explicitly emitted with status `manual` rather than guessed.

## References

- [Microsoft Power Platform API reference | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/power-platform/)
- [Manage application users in the Power Platform admin center | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users)
- [Microsoft Graph permissions reference | Microsoft Learn](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
