"""Data models for baseline items, check results and assessment reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class CheckStatus(str, Enum):
    """Outcome of evaluating a baseline item against a tenant or environment."""

    PASS = "pass"
    FAIL = "fail"
    MANUAL = "manual"
    ERROR = "error"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class BaselineReference:
    title: str
    url: str


@dataclass(frozen=True)
class BaselineItem:
    id: str
    title: str
    scope: str
    workload: str
    severity: str
    recommended_value: str
    rationale: str
    ism_controls: list[str]
    essential_eight: list[str]
    configure_summary: str
    verify_summary: str
    assessor_check_id: str | None
    automated: bool
    sentinel_rules: list[str] = field(default_factory=list)
    references: list[BaselineReference] = field(default_factory=list)
    last_verified: str = ""


@dataclass(frozen=True)
class CheckResult:
    baseline_id: str
    check_id: str
    title: str
    scope: str
    workload: str
    severity: str
    status: CheckStatus
    target_id: str
    target_name: str
    details: str
    recommended_value: str
    remediation: str
    ism_controls: list[str] = field(default_factory=list)
    essential_eight: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


@dataclass
class AssessmentReport:
    tenant_id: str
    mode: str
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    schema_version: str = "1.0.0"
    findings: list[CheckResult] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        counts = {status.value: 0 for status in CheckStatus}
        for finding in self.findings:
            counts[finding.status.value] += 1
        counts["total"] = len(self.findings)
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "tenant_id": self.tenant_id,
            "mode": self.mode,
            "summary": self.summary,
            "findings": [item.to_dict() for item in self.findings],
        }
