#!/usr/bin/env python3
"""Interactive and non-interactive installer for LLM Wiki Starter."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INIT = HERE / 'init_wiki.py'


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f' [{default}]' if default else ''
    value = input(f'{prompt}{suffix}: ').strip()
    return value or (default or '')


def build_command(args: argparse.Namespace) -> list[str]:
    cmd = [sys.executable, str(INIT), '--name', args.name, '--domain', args.domain, '--output', args.output]
    if args.force:
        cmd.append('--force')
    return cmd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Guided wizard for creating a new LLM wiki.')
    parser.add_argument('--name', help='Wiki display name')
    parser.add_argument('--domain', help='What this wiki covers')
    parser.add_argument('--output', help='Output directory')
    parser.add_argument('--force', action='store_true', help='Overwrite existing starter files')
    parser.add_argument('--yes', action='store_true', help='Run non-interactively. Requires --name, --domain, and --output.')
    parser.add_argument('--dry-run', action='store_true', help='Print the init command without running it')
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.yes:
        missing = [field for field in ('name', 'domain', 'output') if not getattr(args, field)]
        if missing:
            raise SystemExit(f'--yes requires: {", ".join("--" + m for m in missing)}')
    else:
        print('LLM Wiki Starter Wizard')
        print('-----------------------')
        args.name = args.name or ask('Wiki name', 'Example Wiki')
        args.domain = args.domain or ask('Domain / purpose', 'Knowledge base for Example Project')
        args.output = args.output or ask('Output folder', './example-wiki')
        if not args.force:
            args.force = ask('Overwrite starter files if present? yes/no', 'no').lower() in {'y', 'yes'}

    cmd = build_command(args)
    if args.dry_run:
        print('Would run:', ' '.join(cmd))
        return 0
    return subprocess.call(cmd)


if __name__ == '__main__':
    raise SystemExit(main())
