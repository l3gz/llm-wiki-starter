#!/usr/bin/env python3
"""Quiet wiki watchdog.

Prints nothing when the wiki passes lint.
Prints actionable lint output and exits non-zero when issues are found.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: wiki_watchdog.py /path/to/wiki")
        return 2

    wiki = Path(sys.argv[1]).expanduser().resolve()
    if not wiki.exists():
        print(f"Wiki path does not exist: {wiki}")
        return 2

    lint_script = Path(__file__).with_name("lint_wiki.py")
    result = subprocess.run(
        [sys.executable, str(lint_script), str(wiki)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    if result.returncode == 0:
        return 0

    print(result.stdout.strip())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
