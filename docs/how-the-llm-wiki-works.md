# How the LLM Wiki Works

The LLM wiki is a markdown knowledge base designed for agent use.

Instead of dumping everything into one prompt or relying only on vector retrieval, the agent compiles source material into a structured wiki:

- raw sources stay untouched
- useful facts become entity and concept pages
- comparisons and query answers get filed when they are worth reusing
- `index.md` acts as the curated map (not an exhaustive file listing)
- `SCHEMA.md` acts as the operating contract
- `log.md` makes the wiki auditable over time

## Hybrid model

Most users do not start from scratch. They arrive with existing documents, client folders, project files, and research that already has a structure.

The wiki supports both:

- **Fresh start**: use the four synthesized folders (`entities/`, `concepts/`, `comparisons/`, `queries/`) as your knowledge graph.
- **Hybrid**: keep your existing content folders where they are. Declare them in `SCHEMA.md` under `## Content folders`. The lint includes them in wikilink resolution but does not enforce frontmatter or tags on them. Over time, the agent synthesizes cross-cutting knowledge pages that reference your legacy content.

Neither mode is temporary. Legacy folders are the permanent home for working documents. Synthesized folders are the permanent home for cross-cutting knowledge.

## Main advantage

The wiki compounds. The next answer starts from organized knowledge, not from scratch.

## Agent workflow

Every session should start with orientation:

1. Read `SCHEMA.md`
2. Read `index.md`
3. Read recent `log.md`
4. Search existing pages before creating new ones
5. Save source material under `raw/`
6. Update synthesized pages with links and sources
7. Update navigation (curated index) and log
