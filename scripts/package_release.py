#!/usr/bin/env python3
"""Package release artefacts (assessor wheel/sdist, Sentinel bundle, baseline bundle and SHA-256 sums)."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import subprocess
import sys
import zipfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def zip_directory(source_dir: pathlib.Path, out_zip: pathlib.Path) -> int:
    count = 0
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.name == ".DS_Store":
                continue
            arcname = path.relative_to(REPO_ROOT).as_posix()
            zf.write(path, arcname)
            count += 1
    return count


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build release artefacts into dist/.")
    parser.add_argument("--version", default="1.0.0", help="Semantic version without leading 'v'.")
    parser.add_argument(
        "--out-dir",
        type=pathlib.Path,
        default=REPO_ROOT / "dist",
        help="Output directory for built release artefacts.",
    )
    args = parser.parse_args()

    out_dir: pathlib.Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    for existing in out_dir.iterdir():
        if existing.is_file():
            existing.unlink()

    # Build pp-assessor wheel and sdist
    subprocess.run(
        [sys.executable, "-m", "build", "--outdir", str(out_dir), str(REPO_ROOT / "assessor")],
        check=True,
    )

    sentinel_zip = out_dir / f"sentinel-content-v{args.version}.zip"
    s_files = zip_directory(REPO_ROOT / "sentinel", sentinel_zip)
    print(f"Packaged {sentinel_zip.name} ({s_files} files)")

    baseline_zip = out_dir / f"baseline-v{args.version}.zip"
    b_files = zip_directory(REPO_ROOT / "baseline", baseline_zip)
    print(f"Packaged {baseline_zip.name} ({b_files} files)")

    checksums: list[str] = []
    for artefact in sorted(p for p in out_dir.iterdir() if p.is_file()):
        checksums.append(f"{sha256_file(artefact)}  {artefact.name}")
    (out_dir / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(f"Wrote SHA256SUMS.txt ({len(checksums)} artefacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
