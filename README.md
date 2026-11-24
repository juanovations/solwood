# Solwood

A new project, set up for Claude Code with [ECC](https://github.com/affaan-m/ECC) [Ponytail](https://github.com/DietrichGebert/ponytail) and the [Graphify](https://github.com/Graphify-Labs/graphify) skill.

## Getting started with Claude Code

1. Install Claude Code 2.1 or newer, Node.js 18+, and Git.
2. Open this folder in Claude Code. It reads `.claude/settings.json`, which declares the ECC and Ponytail marketplaces and enables the `ecc@ecc` and `ponytail@ponytail` plugins for this project. Accept the prompts to trust the marketplaces and install the plugins.
3. Optional: run `/plugin configure ecc@ecc` to pick a hook profile (`minimal`, `standard` or `strict`; default `standard`) or turn hooks off.
4. Optional: run `/plugin configure ponytail@ponytail` to change Ponytail's settings. By default it logs each task's cost and token use to a local CSV under `~/.config/ponytail/` and sends nothing off your machine.
5. Optional, for `/graphify`: install the Graphify CLI with `uv tool install graphifyy` (needed for `/graphify` and the Graphify hooks). Then run `/graphify .` in Claude Code to build a knowledge graph of the repo in `graphify-out/`.

## What's included

| Path | Purpose |
|---|---|
| `.claude/settings.json` | Enables the ECC and Ponytail plugins at project scope |
| `.claude/rules/ecc/common/` | ECC's language-agnostic rules (coding style, security, testing, git workflow) |
| `.claude/skills/graphify/` | Graphify's `/graphify` skill; its hooks are in `.claude/settings.json` |
| `CLAUDE.md` | Project instructions for Claude Code |
