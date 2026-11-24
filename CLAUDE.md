# CLAUDE.md

Guidance for Claude Code when working in the Solwood repository.

## Project

Solwood is a new project. Describe what it does, its stack, and how to run and test it here as it takes shape.

## ECC

This repo uses [ECC](https://github.com/affaan-m/ECC) as a project-scoped Claude Code plugin (`ecc@ecc`, declared in `.claude/settings.json`).

- Skills, agents, commands and hooks come from the plugin. Use `/ecc:configure-ecc` to change the hook profile or other ECC settings.
- Always-loaded rules live in `.claude/rules/ecc/common`. When the stack is chosen, copy the matching language pack (for example `rules/typescript` or `rules/python` from the ECC repo) into `.claude/rules/ecc/`.
- Do not also run a manual ECC install into this project; stacking installs duplicates skills and hooks.

## Ponytail

This repo also enables [Ponytail](https://github.com/DietrichGebert/ponytail) (`ponytail@ponytail`), which steers Claude toward the simplest solution that works: YAGNI, standard library first, no unrequested abstractions, and tests for risky logic.

- Its skills include `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt` and `/ponytail-help`.
- Where Ponytail's "write less" guidance and an ECC rule disagree, ECC's security and testing rules win.

## Graphify

The `/graphify` skill from [Graphify](https://github.com/Graphify-Labs/graphify) lives in `.claude/skills/graphify/` (installed with `graphify install --project`).

- It needs the Graphify CLI on PATH: `uv tool install graphifyy` (or `pipx install graphifyy`).
- `.claude/settings.json` runs `graphify hook-guard` before Bash, Grep, Read and Glob calls to nudge Claude toward the graph, and after context compaction. The hooks fail open and only advise (strict mode is off). Without the CLI on PATH they print a harmless `command not found` error.
- Graph output goes to `graphify-out/`, which is git-ignored.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. When the answer is under a Markdown heading, `graphify section "<heading>"` prints that section's text, so the .md need not be opened. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
