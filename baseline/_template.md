---
id: PP-TEN-000
title: Short descriptive title of the setting
scope: tenant
workload: power-platform
severity: high
recommended_value: Concise statement of the required setting value
rationale: Plain-language explanation of the security risk mitigated by this setting.
ism_controls:
  - ISM-0407
essential_eight:
  - Restrict administrative privileges
configure_summary: Power Platform admin centre > Settings > Tenant settings > Example setting.
verify_summary: GET read-only Power Platform tenant settings endpoint and assert the expected property value.
assessor_check_id: pp_ten_example_setting
automated: true
sentinel_rules: []
references:
  - title: Tenant settings - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-000: Short descriptive title of the setting

## Setting and recommended value

- **Scope**: Tenant (or Environment)
- **Workload**: Power Platform
- **Recommended value**: State the exact recommended configuration.
- **Assessor check ID**: `pp_ten_example_setting` (automated or manual)

## Rationale

Explain the threat model, what happens if left at Microsoft's default, and how the recommended value reduces exposure.

## ISM and Essential Eight mapping

- **ISM controls**: List the relevant ISM control identifiers and explain how this setting supports them. Always check the current release of the [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: State the relevant strategy from the [Essential Eight](https://www.cyber.gov.au/essential-eight), or note that no strategy maps directly.

## How to configure

1. Sign in to the Power Platform admin centre as a Power Platform Administrator.
2. Navigate to the setting location and apply the recommended value.
3. Save changes and record the change in your configuration management log.

## How to verify

- **Automated**: Describe the read-only API call and property evaluated by the assessor (or state "Manual only" if no supported read-only API exposes the setting).
- **Manual**: Describe how an auditor confirms the configuration in the Power Platform admin centre or Purview portal.

## References

- [Tenant settings - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
