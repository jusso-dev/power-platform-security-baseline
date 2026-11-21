"""Allow running the assessor via `python -m pp_assessor`."""

from pp_assessor.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
