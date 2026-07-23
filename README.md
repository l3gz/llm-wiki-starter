# LLM Wiki Starter

> Public starter release: `v0.18.2`.
> Plain markdown. Works with any LLM agent.

A starter repo for building an agent-readable knowledge base from day one.

This repo is based on Andrej Karpathy's LLM wiki pattern: keep raw source material separate from synthesized wiki pages, use a schema to constrain the agent, and let knowledge compound instead of re-summarizing the same documents over and over.

The wiki is plain markdown. It works with any LLM agent - Hermes, Claude Code, Codex, or anything else that can read files and follow instructions. Agent-specific customization (profiles, memory providers, orchestration) is deliberately out of scope: each agent ecosystem has its own tooling for that, and the wiki should not care which one you use.

## What this gives you

- A clean folder structure for business, client, research, or project knowledge
- A `SCHEMA.md` that tells the agent how to behave
- A source-first workflow for transcripts, PDFs, docs, links, books, and notes
- Obsidian-friendly markdown with `[[wikilinks]]`
- A small installer that lays the wiki directly at your project root (or in a subfolder)
- Optional search and navigation tools that work for any agent: QMD (local text/vector search), Graphify and CodeGraph (code knowledge graphs)
- A lightweight wiki lint script and optional maintenance cron/watchdog prompt

## External integrations

This repo does not vendor external tools. It links to them and explains how to connect a generated wiki.

- QMD: <https://github.com/tobi/qmd> and <https://www.npmjs.com/package/@tobilu/qmd>
- Obsidian: <https://obsidian.md> and <https://help.obsidian.md>
- Graphify (codebase knowledge graph): <https://github.com/Graphify-Labs/graphify>. See `docs/graphify-integration.md`.
- CodeGraph (deep code analysis): <https://github.com/colbymchenry/codegraph>. See `docs/codegraph-integration.md`.

## Structure

```text
your-project/            <- the wiki lives at your project root
├── SCHEMA.md
├── index.md
├── log.md
├── INTEGRATIONS.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   ├── documents/
│   ├── books/
│   └── assets/
├── entities/
├── concepts/
├── comparisons/
└── queries/
```

## Quick start

Install the wiki into an existing (or new, empty) project folder - the wiki files land at that folder's root:

```bash
mkdir my-project && cd my-project
python3 /path/to/llm-wiki-starter/scripts/init_wiki.py --name "My Project Wiki" --domain "Knowledge base for My Project" --output .
```

Or create a wiki in its own subfolder:

```bash
python3 scripts/init_wiki.py --name "Example Wiki" --domain "Knowledge base for Example Project" --output ./example-wiki
```

Guided wizard:

```bash
python3 scripts/install_wizard.py
```

Then point your agent at the wiki and ask it to read:

1. `SCHEMA.md`
2. `index.md`
3. recent `log.md`
4. `INTEGRATIONS.md` if you want QMD, Obsidian, Graphify, or CodeGraph setup notes

## Recommended agent prompt

Paste this into any agent working in the wiki:

```text
You are helping me build and maintain this knowledge base.

Before doing anything, read SCHEMA.md, index.md, and the most recent entries in log.md.

Follow the wiki rules:
- raw/ is immutable source material
- entities/, concepts/, comparisons/, and queries/ are synthesized wiki pages
- every page needs frontmatter
- every meaningful update needs index.md and log.md updates
- use [[wikilinks]] between related pages
- do not invent facts not supported by sources

After orientation, ask me for the first source to ingest or the first question to answer from the wiki.
```

## Maintenance

Run a manual lint check:

```bash
python3 scripts/lint_wiki.py /path/to/wiki
```

Run a quiet watchdog check (prints only on failure):

```bash
python3 scripts/wiki_watchdog.py /path/to/wiki
```

For recurring maintenance, see:

```text
docs/wiki-maintenance-cron.md
```

The maintenance job is optional. It can periodically lint the wiki, flag broken links, stale pages, missing index entries, low-confidence pages, and source drift.

## Integration docs

- `docs/how-the-llm-wiki-works.md` - the pattern explained
- `docs/karpathy-method.md` - the original method
- `docs/qmd-integration.md`
- `docs/graphify-integration.md`
- `docs/codegraph-integration.md`
- `docs/obsidian-setup.md`
- `docs/wiki-maintenance-cron.md`
