# Security baseline

This directory contains Microsoft Power Platform and Copilot Studio security baseline items written in the style of the [ASD Blueprint for Secure Cloud](https://blueprint.asd.gov.au/). Each item specifies a setting, recommended value, rationale, [Information Security Manual (ISM)](https://www.cyber.gov.au/ism) and [Essential Eight](https://www.cyber.gov.au/essential-eight) mapping, configuration steps, verification steps and official references.

This is an independent community baseline and is not produced, endorsed or supported by ASD, ACSC or Microsoft.

## Directory layout

- `schema/baseline-item.schema.json`: JSON Schema (Draft 2020-12) used by CI to validate every item's YAML front matter.
- `_template.md`: Authoring template for new baseline items.
- `examples/`: Example item used to verify schema validation.
- `tenant/`: Tenant-level baseline items (`PP-TEN-###`).
- `environment/`: Environment-level and Dataverse baseline items (`PP-ENV-###`).
- `copilot-studio/`: Copilot Studio and agent baseline items (`PP-CS-###`).

## Validation

Run the baseline validator locally before opening a pull request:

```bash
python3 scripts/validate_baseline.py
```

The validator checks that:

1. `baseline/schema/baseline-item.schema.json` is a valid Draft 2020-12 JSON Schema.
2. Every Markdown file under `baseline/tenant/`, `baseline/environment/`, `baseline/copilot-studio/` and `baseline/examples/` (plus `_template.md`) has valid YAML front matter conforming to the schema.
3. Baseline item IDs and non-null `assessor_check_id` values are unique across active baseline items.
4. Every item contains all required Blueprint-style Markdown sections.
