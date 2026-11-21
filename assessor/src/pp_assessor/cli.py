"""Command-line interface for the read-only Power Platform security assessor."""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Sequence

from pp_assessor.auth import MsalAppOnlyTokenProvider, MsalDelegatedTokenProvider
from pp_assessor.checks import register_environment_checks, register_tenant_checks
from pp_assessor.engine import (
    CheckRegistry,
    FixtureDataProvider,
    LiveApiDataProvider,
    ReadOnlyDataProvider,
    run_assessment,
)
from pp_assessor.formatters import write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pp-assessor",
        description="Read-only security baseline assessor for Microsoft Power Platform and Copilot Studio.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    assess = sub.add_parser("assess", help="Run a read-only baseline assessment.")
    source = assess.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--fixture",
        type=pathlib.Path,
        help="Path to an offline JSON fixture file (no live tenant connection).",
    )
    source.add_argument(
        "--auth",
        choices=("delegated", "app-only"),
        help="Live read-only Microsoft Entra authentication mode.",
    )
    assess.add_argument(
        "--tenant-id",
        help="Microsoft Entra tenant GUID (required for live auth modes).",
    )
    assess.add_argument(
        "--client-id",
        help="Microsoft Entra application (client) GUID (required for live auth modes).",
    )
    assess.add_argument(
        "--baseline-dir",
        type=pathlib.Path,
        default=None,
        help="Optional override path to the baseline/ directory.",
    )
    assess.add_argument(
        "--scope",
        choices=("all", "tenant", "environment"),
        default="all",
        help="Filter baseline items by scope (default: all).",
    )
    assess.add_argument(
        "--format",
        choices=("json", "csv", "markdown", "all"),
        default="markdown",
        help="Output format (default: markdown).",
    )
    assess.add_argument(
        "--output",
        type=pathlib.Path,
        default=None,
        help="Output file path (or directory when --format all). Prints to stdout if omitted.",
    )
    return parser


def default_registry() -> CheckRegistry:
    """Return a CheckRegistry populated with all implemented read-only checks."""
    registry = CheckRegistry()
    register_tenant_checks(registry)
    register_environment_checks(registry)
    return registry


def _build_provider(args: argparse.Namespace) -> ReadOnlyDataProvider:
    if args.fixture is not None:
        return FixtureDataProvider.from_file(args.fixture)

    if not args.tenant_id or not args.client_id:
        raise ValueError("--tenant-id and --client-id are required when using --auth.")

    if args.auth == "app-only":
        token_provider = MsalAppOnlyTokenProvider(
            tenant_id=args.tenant_id,
            client_id=args.client_id,
        )
        return LiveApiDataProvider(
            tenant_id=args.tenant_id,
            token_provider=token_provider,
            delegated=False,
        )

    token_provider = MsalDelegatedTokenProvider(
        tenant_id=args.tenant_id,
        client_id=args.client_id,
    )
    return LiveApiDataProvider(
        tenant_id=args.tenant_id,
        token_provider=token_provider,
        delegated=True,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "assess":
        if args.format == "all" and args.output is None:
            parser.error("--output directory is required when --format all is specified.")

        provider = _build_provider(args)
        scopes = None if args.scope == "all" else {args.scope}
        report = run_assessment(
            provider=provider,
            registry=default_registry(),
            baseline_dir=args.baseline_dir,
            scopes=scopes,
        )
        rendered = write_report(report, fmt=args.format, output_path=args.output)
        if args.output is None:
            sys.stdout.write(next(iter(rendered.values())))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
