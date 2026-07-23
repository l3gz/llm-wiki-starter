#!/usr/bin/env python3
"""Create a new LLM wiki from this starter repo.

Two modes:
- Subfolder (default): --output ./example-wiki creates the wiki in its own folder.
- Project root: --output . lays the wiki files at the current directory's root,
  so a project folder has SCHEMA.md, raw/, entities/ right at the top.

Root mode safety: the target directory must be empty apart from .git (a freshly
cloned or newly initialized repo). Use --force to install into a directory that
already has content; existing wiki files are then overwritten.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRS = [
    'raw/articles',
    'raw/papers',
    'raw/transcripts',
    'raw/documents',
    'raw/books',
    'raw/assets',
    'entities',
    'concepts',
    'comparisons',
    'queries',
]

DOMAIN_PLACEHOLDER = (
    'This starter schema is for a client or project knowledge base. Customize this section for the exact business, research area, product, or client.'
)


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f'Refusing to overwrite existing file: {path}. Use --force.')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def check_root_target(out: Path, force: bool) -> None:
    """Refuse to dump wiki files into a directory that already has content."""
    existing = [p.name for p in out.iterdir() if p.name != '.git']
    if existing and not force:
        raise SystemExit(
            f'{out} is not empty ({len(existing)} entries, e.g. {sorted(existing)[:3]}). '
            'Refusing to install a wiki at the root of a non-empty directory. '
            'Use a subfolder output, or --force to install anyway.'
        )


def integrations_doc(name: str, output_path: Path) -> str:
    return f'''# {name} Integrations

This wiki is plain markdown and works without external tools, with any LLM agent. The tools below are optional layers.

## QMD

- GitHub: https://github.com/tobi/qmd
- npm: https://www.npmjs.com/package/@tobilu/qmd
- Purpose: local search, hybrid query, vector search, and MCP access over markdown collections.

Setup from inside this wiki:

```bash
cd {output_path}
npm install -g @tobilu/qmd
qmd collection add
qmd status
qmd update
```

Search examples:

```bash
qmd search "important concept" -c <collection-name> --format json -n 5
qmd query "Find pages about the core offer" -c <collection-name> --no-rerank --format json -n 10
```

Rule: use QMD to find candidate pages, then read the full markdown files before making claims.

## Obsidian

- Website: https://obsidian.md
- Help: https://help.obsidian.md

Open this folder as an Obsidian vault. Keep attachments in `raw/assets/`. Wikilinks like `[[page-name]]` work out of the box.

## Graphify

- GitHub: https://github.com/Graphify-Labs/graphify
- Purpose: codebase knowledge graph (tree-sitter AST, no LLM for code). Answers "what calls X?" and "how does A connect to B?".

```bash
uv tool install graphifyy[anthropic,sql]
cd your-code-repo
graphify . --code-only
graphify query "how does authentication work"
```

## CodeGraph

- GitHub: https://github.com/colbymchenry/codegraph
- Purpose: deep call-path analysis, test impact, symbol search across 20+ languages, with MCP integration for agents that support it.

```bash
curl -fsSL https://codegraph.dev/install.sh | bash
cd your-code-repo
codegraph init .
```

## Agent memory

Some agent ecosystems ship their own long-term memory layers (for example Hindsight for Hermes). Those are configured through the agent, not through this wiki. If a memory-derived insight is worth keeping, write it to a synthesized page or `queries/` and append to `log.md` - the wiki stays the canonical knowledge store.
'''


def main() -> int:
    parser = argparse.ArgumentParser(description='Create a new LLM wiki.')
    parser.add_argument('--name', required=True, help='Wiki display name')
    parser.add_argument('--domain', required=True, help='What this wiki covers')
    parser.add_argument('--output', required=True, help='Output directory (use . to install at the current/project root)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing starter files; allow install into a non-empty directory')
    args = parser.parse_args()

    out = Path(args.output).expanduser().resolve()
    today = dt.date.today().isoformat()

    out.mkdir(parents=True, exist_ok=True)
    check_root_target(out, args.force)

    for d in DIRS:
        (out / d).mkdir(parents=True, exist_ok=True)
        (out / d / '.gitkeep').write_text('', encoding='utf-8')

    schema = (ROOT / 'SCHEMA.md').read_text(encoding='utf-8')
    schema = schema.replace(DOMAIN_PLACEHOLDER, args.domain)

    index = f'''# {args.name} Index

> Curated catalog of high-value pages. Not an exhaustive file listing.
> List the 20-30 most important pages with one-line descriptions, plus a folder map.
> Last updated: {today} | Total pages: 0

## Folder map

- `raw/` - immutable source material
- `entities/` - people, organizations, products, tools
- `concepts/` - topics, frameworks, offers, processes
- `comparisons/` - side-by-side analyses
- `queries/` - filed answers worth keeping

## Featured pages

_Add the highest-value pages here with one-line descriptions. The index is
curated, not exhaustive - you do not need to list every page._

## Entities

## Concepts

## Comparisons

## Queries
'''

    log = f'''# {args.name} Log

> Chronological record of wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`

## [{today}] create | Wiki initialized
- Name: {args.name}
- Domain: {args.domain}
- Created with llm-wiki-starter.
- Structure created: SCHEMA.md (hybrid model, content folders, noise policy, tag taxonomy), index.md (curated catalog), log.md, INTEGRATIONS.md, raw/, entities/, concepts/, comparisons/, queries/.
- The wiki supports both fresh-start and hybrid use (existing document collections alongside synthesized folders). See SCHEMA.md ## Hybrid model.
'''

    readme = f'''# {args.name}

{args.domain}

## Start here

1. Read `SCHEMA.md`.
2. Read `index.md`.
3. Read recent `log.md`.
4. Read `INTEGRATIONS.md` if you want QMD, Obsidian, Graphify, or CodeGraph setup notes.
5. Add source material under `raw/`.
6. Create synthesized pages under `entities/`, `concepts/`, `comparisons/`, and `queries/`.
7. If you have existing content folders (clients, projects, docs), declare them in `SCHEMA.md` under `## Content folders`. They will be included in wikilink resolution but not lint-enforced.

## Agent prompt

Paste into any agent working in this wiki:

```text
Before doing anything, read SCHEMA.md, index.md, and recent log.md. Follow the schema exactly. Do not invent unsupported facts. Keep raw sources immutable. Update index.md and log.md after meaningful changes.
```
'''

    write_file(out / 'SCHEMA.md', schema, args.force)
    write_file(out / 'index.md', index, args.force)
    write_file(out / 'log.md', log, args.force)
    write_file(out / 'README.md', readme, args.force)
    write_file(out / 'INTEGRATIONS.md', integrations_doc(args.name, out), args.force)

    print(f'Created LLM wiki: {out}')
    print('Created: SCHEMA.md, index.md, log.md, README.md, INTEGRATIONS.md, raw/, entities/, concepts/, comparisons/, queries/')
    print('Next: add raw sources under raw/ and ask your agent to orient from SCHEMA.md, index.md, and log.md.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
