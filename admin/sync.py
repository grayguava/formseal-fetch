#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

EXPORT_TOOL = ROOT / "export-tool" / "fetch-export.py"
DECRYPT_TOOL = ROOT / "decrypt-tool" / "decrypt-and-split.py"
CLEANUP_TOOL = ROOT / "cleanup-tool" / "cleanup-exports.py"


def run_step(title: str, script: Path) -> None:
    print()
    print("=" * 40)
    print(title)
    print("=" * 40)

    if not script.exists():
        print(f"ERROR: script not found: {script}")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=script.parent,
    )

    if result.returncode != 0:
        print()
        print(f"ERROR: {title} failed (exit code {result.returncode})")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="FormSeal Sync (Online -> Offline)"
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Skip cleanup step",
    )
    args = parser.parse_args()

    print()
    print("FormSeal Sync")
    print("Mode: Online -> Offline")
    print()

    # STEP 1 — EXPORT
    run_step(
        "[1/3] EXPORT (ONLINE)",
        EXPORT_TOOL,
    )

    # STEP 2 — DECRYPT + SPLIT
    run_step(
        "[2/3] DECRYPT + SPLIT (OFFLINE)",
        DECRYPT_TOOL,
    )

    # STEP 3 — CLEANUP
    if not args.no_cleanup:
        run_step(
            "[3/3] CLEANUP RAW EXPORTS (OFFLINE)",
            CLEANUP_TOOL,
        )
    else:
        print()
        print("[3/3] CLEANUP skipped")

    print()
    print("=" * 40)
    print("SYNC COMPLETE")
    print("All steps executed successfully.")
    print("=" * 40)


if __name__ == "__main__":
    main()
