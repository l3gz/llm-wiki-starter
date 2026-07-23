# CodeGraph Integration

[CodeGraph](https://github.com/colbymchenry/codegraph) is a deep code knowledge graph tool with 20+ language support, MCP integration for coding agents, and auto-sync via file watchers. It complements Graphify by focusing on call-path analysis and impact testing rather than community detection.

## What it does

- Deep multi-language AST extraction (Python, TypeScript, Go, Rust, Java, C#, Swift, Kotlin, and more)
- MCP integration for agents that support it (e.g. Hermes, Claude Code)
- Auto-sync via native OS file watchers (inotify on Linux) - no manual rebuild needed
- Call-path analysis with dynamic-dispatch hops
- Test impact analysis (`codegraph affected`)
- FTS5 full-text symbol search
- 20+ language support vs Graphify's effective ~2 (bash + generic file)

## How it complements this wiki and Graphify

| Question | Use |
|----------|-----|
| "Where is the documentation about X?" | QMD |
| "What calls this function? How does A connect to B?" | Graphify |
| "How does X work? What does changing X affect?" | CodeGraph |

**Graphify** = community detection, multi-repo merge, semantic relationship types
**CodeGraph** = deep call paths, impact analysis, symbol search, auto-sync

They coexist. CodeGraph does not replace Graphify.

## Installation

```bash
# Install the CLI
curl -fsSL https://codegraph.dev/install.sh | bash

# Index a repository
cd your-project
codegraph init .

# Verify
codegraph status
```

## Usage

The CLI works for any user or agent:

```bash
codegraph query "how does authentication work"
codegraph affected --file src/auth.py    # what tests are affected by changes to auth.py
codegraph search "UserService"           # FTS5 symbol search
```

If your agent supports MCP, wire the integration so the agent gets a native exploration tool - for Hermes that is `codegraph install --target=hermes --yes`; other agents have equivalent MCP server configuration. Once wired, the agent can trace call paths, run impact analysis, and search symbols directly.

## Important notes

- `.codegraph/` is rebuildable runtime state. Add it to `.gitignore`.
- Auto-sync means the graph stays current as files change - no manual `update` command needed (unlike Graphify).
- Manage the MCP wiring through the installer (`codegraph install`) rather than hand-editing agent config files.
- CodeGraph and Graphify can both be installed on the same project without conflict.
