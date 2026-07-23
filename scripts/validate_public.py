#!/usr/bin/env python3
"""Public-artifact leak gate for the LLM Wiki Starter.

Scans the repo's text surfaces for private/persona/deployment identity and
long numeric platform IDs. Keep denylist strings encoded so the public repo
does not itself spell the identifiers it blocks. Decoded only at runtime.
"""
from __future__ import annotations

import codecs
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_ENCODED_FORBIDDEN = [
    'Tvysblyr',
    'Ze Ebobg',
    'Mhpx',
    'Dhragva',
    'Znggrhf',
    'Zbzb',
    'Pncgnva Arzb',
    'y3tm',
    'y3tmm',
    'IZ1',
    'TebjguFdhner',
    'Crgr',
    'Xlba',
    'Xlba Sbhaqngvba',
    'xlba-sbhaqngvba',
    'XlbaPynj',
    'NV_Sbhaqngvba',
]
_FORBIDDEN_TERMS = [codecs.decode(term, 'rot_13') for term in _ENCODED_FORBIDDEN]


def _term_pattern(term: str) -> str:
    return r'\s*'.join(re.escape(part) for part in re.split(r'\s+', term.strip()))


FORBIDDEN = re.compile(
    r'\b(?:' + '|'.join(_term_pattern(term) for term in _FORBIDDEN_TERMS) + r')\b|[0-9]{17,19}',
    re.IGNORECASE,
)

TEXT_EXTENSIONS = {
    '.css',
    '.html',
    '.json',
    '.md',
    '.py',
    '.sh',
    '.txt',
    '.yaml',
    '.yml',
}

# Everything shipped publicly, except git internals and this validator's own
# encoded denylist (decoded only in memory).
SCAN_ROOTS = ['README.md', 'SCHEMA.md', 'index.md', 'log.md', 'docs', 'scripts', 'templates']
SELF = Path(__file__).resolve()


def fail(msg: str) -> int:
    print(f'public validation failed: {msg}', file=sys.stderr)
    return 1


def _iter_scan_files() -> list[Path]:
    files: list[Path] = []
    for item in SCAN_ROOTS:
        path = ROOT / item
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        for candidate in path.rglob('*'):
            if candidate.is_file() and candidate.suffix.lower() in TEXT_EXTENSIONS:
                files.append(candidate)
    return files


def main() -> int:
    for path in _iter_scan_files():
        if path.resolve() == SELF:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if FORBIDDEN.search(text):
            return fail(f'{path.relative_to(ROOT)} leaks private/persona/deployment identity')
    print('public validation passed: no private/persona/deployment identity found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
