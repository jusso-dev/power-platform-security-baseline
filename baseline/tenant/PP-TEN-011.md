---
id: PP-TEN-011
title: Configure Customer-Managed Keys for sensitive production environments
scope: tenant
workload: dataverse
severity: medium
recommended_value: Enterprise encryption policy using Azure Key Vault Customer-Managed Keys (CMK) applied to sensitive production Managed Environments
rationale: Customer-Managed Keys provide organisational control over data-at-rest key lifecycle, rotation and cryptographic revocation in Azure Key Vault or Managed HSM.
ism_controls:
  - ISM-0459
  - ISM-1453
essential_eight: []
configure_summary: Create an Azure Key Vault encryption enterprise policy in Power Platform admin centre and assign sensitive Managed Environments to it.
verify_summary: Read enterprise policies via the BAP API to verify at least one active Encryption (CMK) policy exists for sensitive production environments.
assessor_check_id: pp_ten_cmk_configured
automated: true
sentinel_rules: []
references:
  - title: Manage your customer-managed encryption key - Power Platform | Microsoft Learn
    url: https://learn.microsoft.com/en-us/power-platform/admin/customer-managed-key
  - title: Information Security Manual (ISM) | cyber.gov.au
    url: https://www.cyber.gov.au/ism
last_verified: "2026-11-21"
---

# PP-TEN-011: Configure Customer-Managed Keys for sensitive production environments

## Setting and recommended value

- **Scope**: Tenant
- **Workload**: Dataverse
- **Recommended value**: For environments storing OFFICIAL: Sensitive, PROTECTED or regulated data, configure a Power Platform **Enterprise Policy** for **Customer-Managed Keys (CMK)** backed by an Azure Key Vault (with soft-delete and purge protection enabled) or Azure Key Vault Managed HSM, and apply it to those Managed Environments.
- **Assessor check ID**: `pp_ten_cmk_configured` (automated)

## Rationale

While Microsoft encrypts Dataverse data at rest by default using Microsoft-managed keys, Customer-Managed Keys let the organisation control key generation, rotation schedules and emergency key revocation in its own Azure subscription, supporting regulatory and sovereignty requirements.

## ISM and Essential Eight mapping

- **ISM controls**: Supports `ISM-0459` (cryptographic key management) and `ISM-1453` (protecting sensitive data at rest with approved cryptographic controls). Confirm against the current [Information Security Manual](https://www.cyber.gov.au/ism).
- **Essential Eight**: No Essential Eight strategy maps directly.

## How to configure

1. Provision an Azure Key Vault (with soft-delete and purge protection enabled) or Managed HSM in an approved Australian Azure region.
2. Create an RSA encryption key and register a Power Platform Encryption Enterprise Policy following Microsoft Learn instructions.
3. In the Power Platform admin centre, go to **Manage** > **Policies** > **Enterprise policies** and apply the encryption policy to each sensitive Managed Environment.

## How to verify

- **Automated**: Query the read-only BAP enterprise policies endpoint (`GET https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform/enterprisePolicies`) and confirm at least one active `Encryption` policy is linked to sensitive environments.
- **Manual**: Review **Manage** > **Policies** > **Enterprise policies** in the Power Platform admin centre and confirm Key Vault purge protection and key rotation policies in Azure.

## References

- [Manage your customer-managed encryption key - Power Platform | Microsoft Learn](https://learn.microsoft.com/en-us/power-platform/admin/customer-managed-key)
- [Information Security Manual | cyber.gov.au](https://www.cyber.gov.au/ism)
