"""Read-only baseline check implementations."""

from pp_assessor.checks.environment import register_environment_checks
from pp_assessor.checks.tenant import register_tenant_checks

__all__ = ["register_tenant_checks", "register_environment_checks"]
