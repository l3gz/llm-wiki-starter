# Wiki Maintenance Cron

This repo includes a lightweight lint script for manual or scheduled wiki maintenance.

## Manual check

```bash
python3 scripts/lint_wiki.py /path/to/wiki
```

## What the lint checks

The bundled lint is intentionally simple and safe:

- required root files exist: `SCHEMA.md`, `index.md`, `log.md`
- synthesized pages have frontmatter
- synthesized pages are listed in `index.md`
- simple `[[wikilinks]]` do not point to obviously missing pages

## Recommended Hermes cron prompt

Use this as a recurring maintenance job prompt inside Hermes. Replace `/path/to/wiki` with the actual wiki path.

```text
You are maintaining a local LLM wiki at /path/to/wiki.

Before doing anything, read:
1. /path/to/wiki/SCHEMA.md
2. /path/to/wiki/index.md
3. the most recent entries in /path/to/wiki/log.md

Run the wiki lint script if available:
python3 /path/to/llm-wiki-starter/scripts/lint_wiki.py /path/to/wiki

Then inspect and report only actionable issues:
- broken wikilinks
- pages missing from index.md
- missing or malformed frontmatter
- pages with confidence: low
- pages marked needs-review
- pages over 200 lines that may need splitting
- raw sources whose sha256 frontmatter no longer matches their body
- stale pages that have not been updated recently, if the schema defines a stale threshold

Do not rewrite the wiki automatically unless explicitly asked. Return a concise maintenance report with:
1. critical issues
2. cleanup suggestions
3. recommended next action
```

## Example Hermes CLI cron setup

From a Hermes-enabled environment:

```bash
hermes cron create "0 9 * * 1" \
  --name "Weekly wiki maintenance" \
  --prompt-file docs/wiki-maintenance-prompt.txt
```

If your Hermes CLI does not support `--prompt-file`, create the job interactively with `hermes cron create` and paste the prompt above.

## Script-only watchdog pattern

If you only want alerts when lint fails, run `scripts/wiki_watchdog.py` from a normal cron/systemd job or a Hermes script-only cron. It stays quiet when the wiki passes and prints issues when it fails.

```bash
python3 scripts/wiki_watchdog.py /path/to/wiki
```

A silent successful run makes it safe for watchdog-style scheduling.
