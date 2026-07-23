# QMD Integration

QMD is an external CLI for querying local markdown knowledge bases.

This repo does not vendor QMD. Install QMD separately and point it at the generated wiki folder.

## Links

- QMD GitHub: <https://github.com/tobi/qmd>
- QMD npm package: <https://www.npmjs.com/package/@tobilu/qmd>
- QMD package name: `@tobilu/qmd`

## Install

Requires Node.js.

```bash
npm install -g @tobilu/qmd
qmd status
```

## Add a wiki collection

From inside the generated wiki folder:

```bash
cd /path/to/wiki
qmd collection add
qmd status
```

QMD names the collection from the current folder. If you need a different name, use QMD's collection management commands:

```bash
qmd collection list
qmd collection rename <old-name> <new-name>
```

## Search examples

```bash
qmd search "customer avatar" -c <collection-name> --format json -n 5
qmd query "Find source-backed claims about the main offer" -c <collection-name> --format json -n 5
qmd get qmd://<collection-name>/index.md
```

For fast local search without LLM reranking:

```bash
qmd query "brand voice examples" -c <collection-name> --no-rerank --format json -n 10
```

## Refresh after wiki edits

After adding or changing wiki pages:

```bash
qmd update
```

If vector search is configured, refresh embeddings:

```bash
qmd embed
```

## Agent rule

Use QMD to find candidate pages, then read the full markdown files before making claims. Snippets are navigation, not proof.

## MCP integration

QMD can expose an MCP server for agents and IDEs:

```bash
qmd mcp
```

QMD also ships version-matched agent instructions:

```bash
qmd skills get qmd --full
qmd skill install
```

Use these when wiring QMD into an agent runtime.

## What belongs in this repo

This repo owns:

- wiki folder structure
- schema conventions
- source and page templates
- lint/watchdog scripts
- integration notes

QMD owns:

- its CLI
- its index
- embeddings
- MCP server
- search/rerank behavior
