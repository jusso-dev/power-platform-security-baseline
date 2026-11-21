"""Read-only guard tests ensuring the assessor can never issue write operations."""

from __future__ import annotations

import ast
import pathlib
import pytest

from pp_assessor.auth import ScopeSecurityError, validate_read_only_scopes
from pp_assessor.http_client import ReadOnlyHttpClient, ReadOnlyViolationError

ASSESSOR_SRC_DIR = pathlib.Path(__file__).resolve().parent.parent / "src" / "pp_assessor"
FORBIDDEN_HTTP_VERBS = {"POST", "PUT", "PATCH", "DELETE"}
FORBIDDEN_METHOD_ATTRS = {"post", "put", "patch", "delete"}


@pytest.mark.parametrize("verb", ["POST", "PUT", "PATCH", "DELETE", "post", "Patch", "HEAD"])
def test_http_client_blocks_non_get_verbs(verb: str) -> None:
    called = False

    def fake_opener(req, timeout):  # pragma: no cover - must never run
        nonlocal called
        called = True
        raise AssertionError("Opener should never be called for non-GET verbs")

    client = ReadOnlyHttpClient(opener=fake_opener)
    with pytest.raises(ReadOnlyViolationError):
        client.request_json(verb, "https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform/tenantSettings")
    assert called is False


def test_http_client_permits_get() -> None:
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self) -> bytes:
            return b'{"status":"ok"}'

    captured = {}

    def fake_opener(req, timeout):
        captured["method"] = req.get_method()
        captured["url"] = req.full_url
        return FakeResponse()

    client = ReadOnlyHttpClient(opener=fake_opener)
    data = client.get_json("https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform/tenantSettings")
    assert captured["method"] == "GET"
    assert data == {"status": "ok"}


@pytest.mark.parametrize(
    "bad_scope",
    [
        "https://graph.microsoft.com/Policy.ReadWrite.All",
        "https://graph.microsoft.com/RoleManagement.ReadWrite.Directory",
        "https://graph.microsoft.com/Directory.Write.All",
        "",
    ],
)
def test_auth_rejects_write_scopes(bad_scope: str) -> None:
    with pytest.raises(ScopeSecurityError):
        validate_read_only_scopes([bad_scope])


def test_static_ast_forbids_write_verbs_in_assessor_source() -> None:
    """Parse every Python file under assessor/src and fail if any write verb is used."""
    violations: list[str] = []

    for py_file in sorted(ASSESSOR_SRC_DIR.rglob("*.py")):
        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(py_file))
        rel = py_file.relative_to(ASSESSOR_SRC_DIR).as_posix()

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr.lower() in FORBIDDEN_METHOD_ATTRS:
                    violations.append(
                        f"{rel}:{node.lineno}: forbidden write method call '.{node.func.attr}()'"
                    )
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value.strip().upper() in FORBIDDEN_HTTP_VERBS:
                    violations.append(
                        f"{rel}:{node.lineno}: forbidden HTTP write verb literal '{node.value}'"
                    )

    assert not violations, "Read-only AST guard detected write operations:\n" + "\n".join(violations)
