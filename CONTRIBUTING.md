# Contributing

Thanks for helping build this baseline.

## How work happens

1. Pick an open issue from the [issue tracker](https://github.com/jusso-dev/power-platform-security-baseline/issues).
2. Pull the latest `main` branch and create a feature branch named `feat/<issue-number>-short-name` (for example `feat/4-tenant-baseline`).
3. Keep each pull request focused on one issue and include `Closes #<issue-number>` in the pull request description.
4. Wait for all CI checks to pass before merging. Maintainers squash-merge pull requests into `main` and delete the source branch.
5. Never force push to `main`. See [docs/branch-protection.md](docs/branch-protection.md) for the recommended repository protection rules.

## Style rules

- **Plain Australian English**: use Australian spelling (organisation, licence, analyse, behaviour, centre, defence, artefact).
- **No em dashes and no emojis**: use commas, colons, parentheses or separate sentences instead of em dashes, and avoid all emoji characters. CI enforces this automatically.
- **Official sources**: every factual claim about a Microsoft product, API, log table or Australian Signals Directorate (ASD) publication must link to an official source on `learn.microsoft.com`, `github.com/Azure/Azure-Sentinel` or `cyber.gov.au`.
- **No endorsement claims**: do not claim or imply official endorsement, approval or support by ASD, the Australian Cyber Security Centre (ACSC) or Microsoft.
- **No secrets or real tenant data**: never commit credentials, tokens, real tenant IDs, subscription IDs, environment URLs or customer data. Use placeholder GUIDs such as `00000000-0000-0000-0000-000000000000` and example domains such as `yourdomain.gov.au` or `contoso.onmicrosoft.com`.
- **Read-only assessor**: the assessor must only call read-only endpoints. Never introduce HTTP write verbs (`POST`, `PUT`, `PATCH`, `DELETE`) in assessor API clients.

## Running checks locally

Before opening a pull request, run the same checks that CI runs:

```bash
# Style check (banned characters: em dashes, emojis, accidental secret patterns)
python3 scripts/check_style.py

# Markdown linting (requires Node.js)
npx --yes markdownlint-cli2

# Link checking (requires lychee)
lychee --config .lychee.toml .
```

When baseline schema validation, Sentinel validation or assessor tests are present, run those scripts as well:

```bash
# Baseline schema validation (once baseline/schema exists)
python3 scripts/validate_baseline.py

# Assessor tests (once assessor/ exists)
pytest assessor/tests
```

## Licensing

By contributing, you agree that code contributions are licensed under the [MIT License](LICENSE) and documentation or baseline prose contributions are licensed under [CC BY 4.0](LICENSE-docs).
