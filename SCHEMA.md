# Wiki Schema

## Domain

This starter schema is for a client or project knowledge base. Customize this section for the exact business, research area, product, or client.

## Core model

The wiki has three layers:

1. Raw sources: immutable source material in `raw/`
2. Synthesized wiki: agent-maintained pages in `entities/`, `concepts/`, `comparisons/`, and `queries/`
3. Schema: this file, which constrains structure, naming, tags, source handling, and update rules

## Hybrid model

Most users do not start from scratch. They arrive with an existing document collection - client folders, project files, research, deliverables - that already has a structure that works for them.

The hybrid model says: **both are valid permanent homes**.

- **Legacy/topical content folders** (e.g. `docs/`, `clients/`, `projects/`, `research/`): single-source content that lives where it already is. These are working documents, not knowledge-graph nodes. They do not need frontmatter or index entries.
- **Synthesized folders** (`entities/`, `concepts/`, `comparisons/`, `queries/`): cross-cutting pages that distill knowledge across multiple sources. These are the agent-maintained layer. They need frontmatter, tags, and index entries.

Neither needs to migrate to the other. Over time, as the agent synthesizes knowledge from legacy sources, synthesized pages accumulate and the wiki becomes more structured. But legacy folders are not temporary - they are the permanent home for working documents.

## Content folders

### Synthesized folders (lint-enforced)

The lint checks these folders for synthesized pages (frontmatter, tags, wikilinks):

```text
entities/          People, organizations, products, brands, tools
concepts/          Topics, frameworks, offers, processes, ideas
comparisons/       Side-by-side analysis pages
queries/           Filed answers worth keeping
```

### Declared content folders (not lint-enforced)

To add your own content folders (legacy/topical), list them below.
Declared folders are included in wikilink resolution but are not lint-enforced for frontmatter or tags.

<!-- lint:content-folders
docs/
clients/
projects/
research/
-->
<!-- Uncomment and edit the lines inside the lint:content-folders block above to declare your folders. -->

If you have no custom folders yet, the starter folders work standalone.

## Directory structure

```text
raw/articles/      Web articles, posts, pages, clippings
raw/papers/        Papers, PDFs, research documents
raw/transcripts/   Calls, podcasts, interviews, meetings
raw/documents/     Internal docs, notes, briefs, and source files
raw/books/         Book notes, licensed excerpts, public-domain books, or client-provided reading packs
raw/assets/        Images, diagrams, attachments
entities/          People, organizations, products, brands, tools
concepts/          Topics, frameworks, offers, processes, ideas
comparisons/       Side-by-side analysis pages
queries/           Filed answers worth keeping
```

## What does NOT belong in the wiki

The wiki lives inside a working directory, and working directories collect build artifacts. These do not belong in the wiki:

- `node_modules/`, `package-lock.json`, `.next/`, `dist/`, `build/`
- `.git/` worktrees or submodule internals
- Bundled application repos or cloned codebases (keep app code in sibling folders)
- Session snapshots, log dumps, or temporary exports
- Binary executables or compiled assets
- `.env` files or any credential files

Keep application code in sibling folders, not inside the wiki. The wiki is for knowledge, not for running software.

## File naming

- Lowercase filenames
- Hyphens instead of spaces
- Descriptive names
- Date-prefix raw sources when useful, for example `2026-07-01-client-call.md`

## Wiki page frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: []
sources: []
status: current | draft | needs-review | archived
confidence: high | medium | low
---
```

## Raw source frontmatter

```yaml
---
source_url: ""
ingested: YYYY-MM-DD
sha256: ""
source_type: article | paper | transcript | document | book | note
---
```

Compute `sha256` over the body content below the closing frontmatter block when possible.

## Conventions

- `raw/` files are immutable after ingestion. Corrections go into synthesized wiki pages.
- `index.md` is a curated catalog, not an exhaustive file listing. List the 20-30 highest-value pages with one-line descriptions, plus a folder map. Do not try to index every page - that makes the index unreadable.
- Every meaningful operation must be appended to `log.md`.
- Use `[[wikilinks]]` to connect related pages.
- Every synthesized page should have at least two outbound links when possible.
- Do not create pages for passing mentions.
- Prefer updating an existing page over creating a duplicate.
- Mark unsupported or weak claims with `confidence: low` or `status: needs-review`.
- If sources conflict, preserve both claims with dates and sources instead of silently overwriting.
- Do not store secrets, API keys, private tokens, passwords, or credential values in the wiki.

## Re-running the wizard

`init_wiki.py` refuses to overwrite existing `SCHEMA.md`, `index.md`, `log.md`, `README.md`, and `INTEGRATIONS.md` unless you pass `--force`. Re-running with `--force` will overwrite those starter files wholesale, which means any local edits you made to `SCHEMA.md` (for example the Domain section, tag taxonomy, or conventions) will be clobbered. Customizations to `raw/` and synthesized pages are not touched. If you only want to add more raw material or synthesized pages, do not re-run the wizard: edit the wiki directly.

## Tag taxonomy

Customize this list before production use.

**Business:**
- `business` `brand` `product` `offer` `avatar` `customer` `client` `project` `campaign`
- `copywriting` `funnel` `sales` `lead-gen` `retention` `objection` `proof`

**Content and media:**
- `transcript` `podcast` `email` `ad` `video` `social` `landing-page`

**Research and strategy:**
- `research` `framework` `process` `strategy` `decision` `comparison` `query` `needs-review`

**People and organizations:**
- `person` `company` `tool` `source`

Rule: every tag on a synthesized page should come from this taxonomy. Add new tags here before using them. The lint loads this taxonomy dynamically and rejects unauthorized tags.

## Page thresholds

Create a page when:

- an entity or concept is central to one important source, or
- it appears across two or more sources, or
- it will be reused by future prompts or workflows.

Do not create a page for:

- minor passing mentions
- details outside the domain
- claims with no source and no user confirmation

## Update policy

When adding new source material:

1. Save the source in `raw/` with raw-source frontmatter.
2. Check `index.md` and existing pages for duplicates.
3. Update or create synthesized pages.
4. Add cross-links.
5. Update `index.md` if the page is high-value enough to be in the curated index.
6. Append to `log.md`.
7. Report created or updated files.

## Integration policy

- QMD, Obsidian, Hermes, and Hindsight are external tools.
- Tool setup details belong in `INTEGRATIONS.md`.
- This wiki remains useful without any external tool because it is plain markdown.
- If an external tool writes into the wiki, it must follow this schema and log meaningful changes.
