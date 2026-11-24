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

The `/graphify` skill from [Graphify](https://github.com/Graphify-Labs/graphify) lives in `.claude/skills/graphify/` (copied from upstream, skill files only).

- It needs the Graphify CLI on PATH: `uv tool install graphifyy` (or `pipx install graphifyy`).
- No Graphify hooks are installed in this repo, so nothing intercepts Claude's reads or searches. Do not run `graphify install`, `graphify claude install` or `graphify hook install` here unless the team decides to turn hooks on.
- Graph output goes to `graphify-out/`, which is git-ignored.
