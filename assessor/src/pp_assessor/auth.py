"""Least-privilege read-only authentication helpers for the assessor."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

BAP_DEFAULT_SCOPE = "https://api.bap.microsoft.com/.default"
GRAPH_DEFAULT_SCOPE = "https://graph.microsoft.com/.default"

DELEGATED_GRAPH_READ_SCOPES: tuple[str, ...] = (
    "https://graph.microsoft.com/Policy.Read.All",
    "https://graph.microsoft.com/RoleManagement.Read.Directory",
    "https://graph.microsoft.com/Directory.Read.All",
)

FORBIDDEN_SCOPE_TOKENS: tuple[str, ...] = (
    "readwrite",
    ".write",
    "manage.",
    "full_access",
)


class ScopeSecurityError(ValueError):
    """Raised when a requested OAuth scope exceeds read-only permissions."""


def validate_read_only_scopes(scopes: list[str] | tuple[str, ...]) -> list[str]:
    """Ensure no write or administrative-mutation OAuth scope is requested."""
    validated: list[str] = []
    for scope in scopes:
        lowered = scope.strip().lower()
        if not lowered:
            raise ScopeSecurityError("Empty OAuth scope is not permitted.")
        for forbidden in FORBIDDEN_SCOPE_TOKENS:
            if forbidden in lowered:
                raise ScopeSecurityError(
                    f"Scope '{scope}' violates least-privilege read-only rules."
                )
        validated.append(scope.strip())
    return validated


def dataverse_scope_for_instance(instance_url: str) -> str:
    """Return the read-only resource scope for a Dataverse environment URL."""
    base = instance_url.rstrip("/")
    if not base.startswith("https://"):
        raise ValueError(f"Dataverse instance URL must use HTTPS: {instance_url}")
    return f"{base}/.default"


class TokenProvider(Protocol):
    """Protocol for acquiring OAuth 2.0 bearer tokens for read-only API calls."""

    def get_token(self, scopes: list[str]) -> str:
        """Return a bearer token for the specified read-only scopes."""


@dataclass
class StaticTokenProvider:
    """Offline/testing token provider returning deterministic tokens without network calls."""

    token: str = "fixture-read-only-token"

    def get_token(self, scopes: list[str]) -> str:
        validate_read_only_scopes(scopes)
        return self.token


class MsalAppOnlyTokenProvider:
    """App-only client credentials token provider via MSAL."""

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str | None = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.client_id = client_id
        self._client_secret = client_secret or os.environ.get("PP_ASSESSOR_CLIENT_SECRET")
        if not self._client_secret:
            raise RuntimeError(
                "App-only auth requires PP_ASSESSOR_CLIENT_SECRET or a configured certificate."
            )

    def get_token(self, scopes: list[str]) -> str:
        safe_scopes = validate_read_only_scopes(scopes)
        try:
            import msal  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError(
                "MSAL is required for live authentication. Install with: pip install -e 'assessor[live]'"
            ) from exc

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self._client_secret,
            authority=authority,
        )
        result = app.acquire_token_for_client(scopes=safe_scopes)
        if "access_token" not in result:
            error = result.get("error_description") or result.get("error") or "unknown auth error"
            raise RuntimeError(f"Failed to acquire app-only token: {error}")
        return str(result["access_token"])


class MsalDelegatedTokenProvider:
    """Interactive delegated device-code token provider via MSAL."""

    def __init__(self, tenant_id: str, client_id: str) -> None:
        self.tenant_id = tenant_id
        self.client_id = client_id

    def get_token(self, scopes: list[str]) -> str:
        safe_scopes = validate_read_only_scopes(scopes)
        try:
            import msal  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError(
                "MSAL is required for live authentication. Install with: pip install -e 'assessor[live]'"
            ) from exc

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority=authority,
        )
        flow = app.initiate_device_flow(scopes=safe_scopes)
        if "message" not in flow:
            raise RuntimeError("Failed to initiate Microsoft Entra device code flow.")
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
        if "access_token" not in result:
            error = result.get("error_description") or result.get("error") or "unknown auth error"
            raise RuntimeError(f"Failed to acquire delegated token: {error}")
        return str(result["access_token"])
