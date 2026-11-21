"""Strictly read-only HTTP transport enforcing GET-only API calls."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Callable

ALLOWED_HTTP_METHODS = frozenset({"GET"})


class ReadOnlyViolationError(RuntimeError):
    """Raised when any caller attempts to issue a non-GET HTTP request."""


class HttpRequestError(RuntimeError):
    """Raised when a read-only GET request fails with an HTTP or transport error."""

    def __init__(self, status_code: int | None, url: str, message: str) -> None:
        super().__init__(f"GET {url} failed ({status_code}): {message}")
        self.status_code = status_code
        self.url = url


class ReadOnlyHttpClient:
    """HTTP client restricted strictly to GET requests.

    Any attempt to execute a write verb raises ReadOnlyViolationError before
    any network socket is opened.
    """

    def __init__(
        self,
        timeout_seconds: float = 30.0,
        opener: Callable[[urllib.request.Request, float], Any] | None = None,
    ) -> None:
        self._timeout = timeout_seconds
        self._opener = opener or self._default_open

    @staticmethod
    def _default_open(request: urllib.request.Request, timeout: float) -> Any:
        return urllib.request.urlopen(request, timeout=timeout)

    def _assert_read_only(self, method: str) -> str:
        normalised = method.strip().upper()
        if normalised not in ALLOWED_HTTP_METHODS:
            raise ReadOnlyViolationError(
                f"HTTP method '{method}' is blocked by the read-only assessor guard. Only GET is permitted."
            )
        return normalised

    def request_json(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        verb = self._assert_read_only(method)
        req_headers = {
            "Accept": "application/json",
            "User-Agent": "power-platform-security-baseline-assessor/0.1.0",
        }
        if headers:
            req_headers.update(headers)

        req = urllib.request.Request(url=url, headers=req_headers, method=verb)
        try:
            with self._opener(req, self._timeout) as response:
                raw = response.read().decode("utf-8")
                if not raw.strip():
                    return {}
                parsed = json.loads(raw)
                return parsed if isinstance(parsed, dict) else {"value": parsed}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            raise HttpRequestError(exc.code, url, body) from exc
        except urllib.error.URLError as exc:
            raise HttpRequestError(None, url, str(exc.reason)) from exc

    def get_json(
        self,
        url: str,
        access_token: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        headers: dict[str, str] = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        if extra_headers:
            headers.update(extra_headers)
        return self.request_json("GET", url, headers=headers)

    def get_paginated(
        self,
        url: str,
        access_token: str | None = None,
        items_key: str = "value",
        next_link_keys: tuple[str, ...] = ("@odata.nextLink", "nextLink"),
        max_pages: int = 100,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        next_url: str | None = url
        pages = 0

        while next_url and pages < max_pages:
            payload = self.get_json(next_url, access_token=access_token)
            items = payload.get(items_key, [])
            if isinstance(items, list):
                results.extend(item for item in items if isinstance(item, dict))
            next_url = None
            for key in next_link_keys:
                candidate = payload.get(key)
                if isinstance(candidate, str) and candidate.startswith("https://"):
                    next_url = candidate
                    break
            pages += 1

        return results
