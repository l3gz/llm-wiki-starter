# Karpathy LLM Wiki Method

Official source: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

This repo is an implementation starter for Andrej Karpathy's LLM wiki pattern: use an LLM agent to build and maintain a persistent, interlinked markdown knowledge base from raw sources.

## The core idea

A normal RAG workflow uploads files, retrieves chunks at query time, and asks the model to synthesize an answer from scratch each time. That works, but the knowledge does not compound. The model has to rediscover the same fragments and rebuild the same synthesis on every subtle question.

The LLM wiki pattern is different. The agent reads raw sources once, extracts the important information, and integrates it into a durable wiki. The wiki sits between the user and the raw documents. It becomes a persistent, compounding artifact where:

- entities have pages
- concepts have pages
- relationships are explicit through `[[wikilinks]]`
- contradictions are preserved and flagged
- summaries are revised as newer sources arrive
- useful query answers can be filed back into the wiki
- provenance points back to source material

The user does not manually maintain the wiki. The user curates sources, asks questions, reviews direction, and decides what matters. The LLM handles the bookkeeping: summarizing, filing, linking, updating, and keeping the index and log current.

Karpathy's framing is useful: Obsidian is the IDE, the LLM is the programmer, and the wiki is the codebase.

## Where this applies

The pattern is domain-agnostic. The official idea lists several contexts where a compounding LLM wiki is useful:

- Personal: track your own goals, health, psychology, and self-improvement by filing journal entries, articles, and podcast notes into a structured picture that builds up over time.
- Research: go deep on a topic over weeks or months, read papers, articles, and reports, and incrementally build a comprehensive wiki with an evolving thesis.
- Reading a book: file each chapter as you go and build pages for characters, themes, and plot threads with the LLM handling all the cross-referencing, so you finish with a rich companion wiki (think fan wikis like Tolkien Gateway, but personal).
- Business or team: an internal wiki maintained by LLMs and fed by chat threads, meeting transcripts, project documents, and customer calls, optionally with humans reviewing updates, staying current because the LLM does the maintenance nobody wants to do.
- Competitive analysis, due diligence, trip planning, course notes, and hobby deep-dives: anything where you accumulate knowledge over time and want it organized rather than scattered.

## Three-layer architecture

The official idea has three layers. This starter repo maps directly to them.

### 1. Raw sources

Raw sources are the source of truth. They live under `raw/` and should be treated as immutable after ingestion.

Examples:

- `raw/articles/` for clipped articles and web pages
- `raw/papers/` for papers and research documents
- `raw/transcripts/` for calls, interviews, podcasts, and meetings
- `raw/documents/` for briefs, notes, and internal documents
- `raw/books/` for book notes, licensed excerpts, public-domain books, or user-provided reading packs
- `raw/assets/` for images, diagrams, and attachments

The agent reads from raw sources but does not rewrite them. Corrections and synthesis belong in wiki pages.

### 2. Synthesized wiki

The synthesized wiki is the LLM-maintained layer. In this starter repo it uses:

- `entities/` for people, organizations, products, tools, places, and named things
- `concepts/` for ideas, frameworks, themes, processes, and reusable abstractions
- `comparisons/` for side-by-side analyses
- `queries/` for filed answers that are valuable enough to keep
- `index.md` as the navigable catalog
- `log.md` as the chronological record

The agent owns this layer. It creates and updates pages, adds links, revises summaries, records conflicts, and keeps the structure coherent.

### Hybrid: existing content alongside synthesized pages

Most users do not start from scratch. They arrive with existing document collections - client folders, project files, research, deliverables.

The hybrid model keeps both:

- **Legacy/topical folders** (e.g. `docs/`, `clients/`, `projects/`): working documents that stay where they are. They do not need frontmatter or index entries.
- **Synthesized folders** (`entities/`, `concepts/`, `comparisons/`, `queries/`): cross-cutting knowledge pages that distill across multiple sources.

Declare your legacy folders in `SCHEMA.md` under `## Content folders` so the lint includes them in wikilink resolution. Neither layer needs to migrate to the other.

### 3. Schema

The schema is the instruction contract for the agent. In this repo it is `SCHEMA.md`.

The schema tells the LLM:

- what folders mean
- how to name files
- what frontmatter to use
- when to create a new page
- how to cite sources
- how to update `index.md`
- how to append to `log.md`
- how to handle contradictions and low-confidence claims

Karpathy notes that this schema is the key configuration file. It turns a generic chatbot into a disciplined wiki maintainer. It should evolve with the domain as the user and agent learn what works.

## Operations

### Ingest

Ingest means adding one or more raw sources into the wiki.

A good ingest flow:

1. Add the source under the right `raw/` folder.
2. Read the source and identify the key claims, entities, concepts, dates, relationships, and open questions.
3. Check `index.md` and existing pages before creating new pages.
4. Create or update synthesized pages.
5. Add `[[wikilinks]]` between related pages.
6. Preserve contradictions instead of silently overwriting older claims.
7. Update `index.md` with new or changed pages.
8. Append a dated entry to `log.md`.
9. Report what changed and what still needs review.

Karpathy prefers involved, one-source-at-a-time ingestion, but the pattern also supports batch ingestion if the schema defines the workflow clearly.

### Query

Query means asking questions against the wiki.

The agent should read `index.md` first, locate relevant pages, inspect the cited sources when needed, and synthesize an answer. The answer can be returned in chat, but if it has durable value it should become a page under `queries/`, `comparisons/`, or another appropriate folder.

Examples of filed query outputs:

- a comparison table
- a research synthesis
- a decision memo
- a source-backed answer
- a slide deck outline
- a chart or data note
- a list of unresolved questions to research next

This is one of the main compounding loops: good questions become new wiki artifacts instead of disappearing into chat history.

### Lint and maintenance

Lint means health-checking the wiki as it grows.

A maintenance pass should look for:

- stale claims superseded by newer sources
- contradictions that are not clearly marked
- orphan pages with no useful inbound or outbound links
- important repeated concepts that lack their own page
- missing source references
- broken `[[wikilinks]]`
- missing `index.md` entries
- vague low-confidence claims that need review
- data gaps that suggest future sources or searches

This repo includes `scripts/lint_wiki.py` and `scripts/wiki_watchdog.py` as lightweight maintenance helpers. They do not replace agent judgment, but they give the agent and user a repeatable local check.

## Index and log

Karpathy calls out two special files that make the wiki navigable at moderate scale.

### `index.md`

`index.md` is content-oriented. It is the map of the wiki.

It should list the highest-value pages by category with links and short summaries - a curated catalog, not an exhaustive file listing. At small to medium scale, a well-maintained index can remove the need for heavier embedding infrastructure. At larger scale, keep the index curated (20-30 key pages plus a folder map) rather than trying to list every page.

### `log.md`

`log.md` is chronological. It records what happened and when.

Use consistent headings so the log is easy for both humans and shell tools to scan, for example:

```markdown
## [2026-07-02] ingest | Source Title
## [2026-07-02] query | Comparison of X and Y
## [2026-07-02] lint | Weekly wiki health check
```

The log helps the agent understand recent context and helps the user audit how the wiki evolved.

## Optional tools

The official idea is intentionally tool-agnostic. The wiki is just markdown plus conventions. Tools are optional accelerators.

Useful tools include:

- Obsidian for browsing, graph view, attachments, Dataview, and human review
- Obsidian Web Clipper for converting web pages to markdown sources
- QMD for local markdown search with BM25, vector search, reranking, CLI access, and MCP access
- Git for version history, branching, review, and collaboration
- Marp for slide decks generated from wiki pages
- Hindsight or another memory layer for optional agent memory outside the wiki

The wiki should remain useful even without these tools.

## Why this works

The hard part of a knowledge base is not only reading. It is maintenance.

Humans stop maintaining wikis because cross-linking, updating summaries, preserving contradictions, and keeping structure consistent becomes tedious. LLM agents are good at this kind of repeated bookkeeping. They can update many files in one pass, keep links current, and fold new evidence into old synthesis.

The human role is judgment: choose sources, guide emphasis, ask good questions, and decide what matters. The LLM role is upkeep: read, summarize, connect, file, revise, and log.

Karpathy connects the idea to Vannevar Bush's Memex: a personal, curated knowledge store with associative trails between documents. The missing maintenance worker is now the LLM.

## How to use this starter repo

This repo turns the abstract pattern into a practical starting point.

1. Generate a new wiki with `scripts/init_wiki.py` or `scripts/install_wizard.py`.
2. Open the generated folder in Obsidian or your editor.
3. Point Hermes or another coding agent at the wiki folder.
4. Ask the agent to read `SCHEMA.md`, `index.md`, and recent `log.md` entries before doing anything.
5. Add one raw source.
6. Ask the agent to ingest it according to `SCHEMA.md`.
7. Review the pages it created or updated.
8. Ask a question worth keeping and file the answer back into the wiki.
9. Run lint or a maintenance pass periodically.
10. Update `SCHEMA.md` whenever the workflow needs sharper rules.

The important rule: do not treat this as a static folder template. Treat it as a living knowledge codebase that the LLM maintains over time.

## Design principles

- Source-first: raw sources stay separate from synthesized wiki pages.
- Persistent synthesis: knowledge is compiled once and kept current.
- Plain markdown: the wiki is readable without special infrastructure.
- Agent-maintained: the LLM writes and updates the wiki, with human review.
- Linked structure: `[[wikilinks]]` make relationships explicit.
- Traceable claims: important claims point back to sources.
- Append-only history: `log.md` records meaningful operations.
- Schema discipline: `SCHEMA.md` defines how the agent behaves.
- Modular tooling: QMD, Obsidian, Hindsight, and Marp are optional, not required.
