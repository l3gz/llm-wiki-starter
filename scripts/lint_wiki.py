#!/usr/bin/env python3
"""Lightweight lint checks for an LLM wiki (hybrid model).

Checks the synthesized knowledge folders - where curated pages live - for:
  1. Required structural files (SCHEMA.md, index.md, log.md)
  2. Frontmatter on all synthesized pages
  3. Tag compliance against the taxonomy declared in SCHEMA.md
  4. Broken wikilinks (code-block-aware: ignores [[links]] inside code blocks)

Declared content folders (from SCHEMA.md ## Content folders) are included
in wikilink resolution but are not lint-enforced for frontmatter or tags.

Legacy/topical folders (clients/, docs/, projects/, etc.) are working
documents, not knowledge-graph nodes. They are skipped by default.

Usage:
  python3 lint_wiki.py /path/to/wiki
  python3 lint_wiki.py /path/to/wiki --strict-index  # require every page in index
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Synthesized knowledge folders - always lint-enforced
SYNTHESIZED_DIRS = ['entities', 'concepts', 'comparisons', 'queries']
REQUIRED = ['SCHEMA.md', 'index.md', 'log.md']

# Exclude these subdirs from lint even inside content dirs
EXCLUDE_SUBDIRS = {
    'node_modules', '.git', '.next', 'dist', 'build',
    'Archive', 'archive', 'Old', 'exports', '__pycache__',
}
EXCLUDE_BASENAMES = {'README.md'}

# Pages above this count: missing-index becomes a warning, not an error
INDEX_THRESHOLD = 30


def collect_synthesized_files(root: Path) -> list[Path]:
    """Collect .md files from the four synthesized folders."""
    files: list[Path] = []
    for d in SYNTHESIZED_DIRS:
        dirpath = root / d
        if not dirpath.is_dir():
            continue
        for path in dirpath.rglob('*.md'):
            rel_parts = path.relative_to(root).parts
            if any(part in EXCLUDE_SUBDIRS for part in rel_parts):
                continue
            if path.name in EXCLUDE_BASENAMES:
                continue
            files.append(path)
    return files


def collect_content_files(root: Path, content_dirs: list[str]) -> list[Path]:
    """Collect .md files from user-declared content folders (for wikilink resolution)."""
    files: list[Path] = []
    for d in content_dirs:
        dirpath = root / d.rstrip('/')
        if not dirpath.is_dir():
            continue
        for path in dirpath.rglob('*.md'):
            rel_parts = path.relative_to(root).parts
            if any(part in EXCLUDE_SUBDIRS for part in rel_parts):
                continue
            if path.name in EXCLUDE_BASENAMES:
                continue
            files.append(path)
    return files


def parse_content_dirs(root: Path) -> list[str]:
    """Parse user-declared content folders from SCHEMA.md.

    Looks for an HTML comment block: <!-- lint:content-folders ... -->
    Each non-empty line inside the block is a folder name.
    """
    schema = root / 'SCHEMA.md'
    if not schema.exists():
        return []
    text = schema.read_text(encoding='utf-8')
    m = re.search(r'<!--\s*lint:content-folders\s*\n(.*?)-->', text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    dirs: list[str] = []
    for line in block.splitlines():
        line = line.strip().rstrip('/')
        if not line or line.startswith('#') or line.startswith('<!--'):
            continue
        # Take the top-level folder name only
        top = line.split('/')[0]
        if top and top not in SYNTHESIZED_DIRS and top not in dirs:
            dirs.append(top)
    return dirs


def extract_tags(text: str) -> list[str]:
    """Extract tags from frontmatter tags: [...] line."""
    m = re.search(r'^tags:\s*\[([^\]]*)\]', text, re.MULTILINE)
    if not m:
        return []
    return [t.strip().strip('"\'').lower() for t in m.group(1).split(',') if t.strip()]


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and inline code so lint ignores example wikilinks."""
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]*`', '', text)
    return text


def extract_wikilinks(text: str) -> list[str]:
    """Extract [[link]] targets, stripping alias and hash. Ignores code blocks."""
    text = strip_code_blocks(text)
    return [m.strip() for m in re.findall(r'\[\[([^\]|#]+)', text) if m.strip()]


def load_taxonomy(root: Path) -> set[str] | None:
    """Load tag taxonomy from SCHEMA.md so there is a single source of truth.

    Parses backtick-wrapped tags from the '## Tag taxonomy' section.
    Returns None if SCHEMA.md is missing or the section cannot be parsed.
    """
    schema = root / 'SCHEMA.md'
    if not schema.exists():
        return None
    text = schema.read_text(encoding='utf-8')
    m = re.search(r'^## Tag taxonomy\s*\n(.*?)(?=\n## |\Z)', text, re.MULTILINE | re.DOTALL)
    if not m:
        return None
    section = m.group(1)
    tags: set[str] = set()
    for t in re.findall(r'`([^`]+)`', section):
        t = t.strip().lower()
        # Accept hyphens but not slashes, commas, or spaces
        if ' ' not in t and '/' not in t and ',' not in t:
            tags.add(t)
    return tags if tags else None


def main() -> int:
    parser = argparse.ArgumentParser(description='Lint checks for an LLM wiki (hybrid model).')
    parser.add_argument('path', nargs='?', default='.', help='Wiki path')
    parser.add_argument('--strict-index', action='store_true',
                        help='Require every synthesized page in index.md (default: relaxed above 30 pages)')
    args = parser.parse_args()
    root = Path(args.path).resolve()
    issues: list[str] = []
    warnings: list[str] = []

    # 1. Required structural files
    for name in REQUIRED:
        if not (root / name).exists():
            issues.append(f'missing required file: {name}')

    page_files = collect_synthesized_files(root)
    content_dirs = parse_content_dirs(root)
    content_files = collect_content_files(root, content_dirs)
    taxonomy = load_taxonomy(root)

    # 2. Frontmatter + tags on each synthesized page
    index_text = ''
    index_path = root / 'index.md'
    if index_path.exists():
        index_text = index_path.read_text(encoding='utf-8')

    for page in page_files:
        text = page.read_text(encoding='utf-8')
        rel = page.relative_to(root).as_posix()

        # Frontmatter check
        if not text.startswith('---'):
            issues.append(f'missing frontmatter: {rel}')
            continue  # skip further checks if no frontmatter

        # Tag taxonomy check (only if taxonomy loaded)
        if taxonomy:
            for tag in extract_tags(text):
                if tag not in taxonomy:
                    issues.append(f'unauthorized tag "{tag}" in {rel}')

    # 3. Index check (curated index model)
    strict = args.strict_index or len(page_files) <= INDEX_THRESHOLD
    for page in page_files:
        rel = page.relative_to(root).as_posix()
        if page.stem not in index_text and rel not in index_text:
            if strict:
                issues.append(f'page not listed in index.md: {rel}')
            else:
                warnings.append(f'page not in curated index: {rel}')

    # 4. Broken wikilinks (code-block-aware)
    all_files = page_files + content_files
    all_stems = {p.stem for p in all_files}
    all_rel_paths = {p.relative_to(root).as_posix() for p in all_files}
    # Also allow linking to folders and structural pages
    known_targets = all_stems | all_rel_paths | set(content_dirs) | {'index', 'log', 'SCHEMA'}

    for page in page_files:
        text = page.read_text(encoding='utf-8')
        rel = page.relative_to(root).as_posix()
        for link in extract_wikilinks(text):
            link_stem = Path(link).stem
            link_rel = link.lstrip('./')
            if link_stem in all_stems:
                continue
            if link_rel in all_rel_paths:
                continue
            if link in known_targets:
                continue
            issues.append(f'possible broken wikilink: [[{link}]] in {rel}')

    # Report
    if warnings:
        for w in sorted(warnings):
            print(f'  WARNING: {w}')

    if issues:
        print(f'Wiki lint found {len(issues)} issue(s):')
        for issue in sorted(issues):
            print(f'  - {issue}')
        if warnings:
            print(f'({len(warnings)} warning(s) not shown above)')
        return 1

    if warnings:
        print(f'Wiki lint passed with {len(warnings)} warning(s): {root} ({len(page_files)} synthesized files checked)')
    else:
        print(f'Wiki lint passed: {root} ({len(page_files)} synthesized files checked)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
