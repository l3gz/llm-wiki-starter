# Graphify Integration

[Graphify](https://github.com/Graphify-Labs/graphify) is a codebase knowledge graph tool. It parses code with tree-sitter AST (deterministic, no LLM for code) and produces a queryable graph of calls, imports, references, and paths between components.

## What it does

- Turns any folder of code into a knowledge graph you can query instead of grepping
- Code is parsed locally with tree-sitter - no LLM, nothing leaves your machine
- Every edge is tagged EXTRACTED (explicit in source) or INFERRED (resolved by graphify)
- Produces three files: `graph.html` (interactive), `GRAPH_REPORT.md` (summary), `graph.json` (queryable)

## How it complements this wiki

This wiki stores curated knowledge pages. QMD searches those pages by text. Graphify maps your code's structure - a different question type:

| Question | Use |
|----------|-----|
| "Where is the documentation about X?" | QMD |
| "What calls this function? How does A connect to B?" | Graphify |

## Installation

```bash
# Recommended (isolated environment)
uv tool install graphifyy[anthropic,sql]

# Alternative
pipx install graphifyy[anthropic,sql]
```

## Usage

```bash
# Build a code-only graph (instant, no API key needed)
cd your-project
graphify . --code-only

# Build a full graph including docs (requires an API key for semantic pass)
graphify . --backend claude

# Query the graph
graphify explain "main_function"
graphify path "module_a" "module_b"
graphify query "how does authentication work"
```

## Agent integration

Any agent can use the graph through the CLI: tell your agent to run `graphify query` / `graphify explain` / `graphify path` for code-structure questions before reading source files. Graphify also ships agent-specific helpers (e.g. `graphify hermes install` for Hermes) that write those rules into your agent's instruction file for you.

## Important notes

- `graphify-out/` is rebuildable runtime state. Add it to `.gitignore`.
- Code parsing is free (tree-sitter, no API cost). The semantic pass over docs/images costs API tokens.
- The graph is per-repo. For multi-repo ecosystems, use `graphify merge-graphs` to combine.
