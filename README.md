# Solwood

Solwood's first development: a 6-unit, 2-bedroom build-to-rent apartment building on land Solwood owns.

## Feasibility

```bash
python3 feasibility/proforma.py
```

This reads `feasibility/inputs.json` and writes [`feasibility/REPORT.md`](feasibility/REPORT.md). The inputs are placeholders: replace them with your land value, construction quotes, local rents, operating costs and loan terms. Run the tests with `python3 -m unittest discover feasibility`.

## Tooling

Set up for Claude Code with [ECC](https://github.com/affaan-m/ECC), [Ponytail](https://github.com/DietrichGebert/ponytail), [Founder](https://github.com/Jakeschincariol/founder-skill), [claude-mem](https://github.com/thedotmack/claude-mem), and the [Graphify](https://github.com/Graphify-Labs/graphify), [Archify](https://github.com/tt-a1i/archify) and [Napkin](https://github.com/blader/napkin) skills.

## Getting started with Claude Code

1. Install Claude Code 2.1 or newer, Node.js 18+, and Git.
2. Open this folder in Claude Code. It reads `.claude/settings.json`, which declares the ECC, Ponytail, Founder and claude-mem marketplaces and enables the `ecc@ecc`, `ponytail@ponytail`, `founder-skill@founder-skill` and `claude-mem@thedotmack` plugins for this project. Accept the prompts to trust the marketplaces and install the plugins.
3. Optional: run `/plugin configure ecc@ecc` to pick a hook profile (`minimal`, `standard` or `strict`; default `standard`) or turn hooks off.
4. Optional: run `/plugin configure ponytail@ponytail` to change Ponytail's settings. By default it logs each task's cost and token use to a local CSV under `~/.config/ponytail/` and sends nothing off your machine.
5. Optional, for `/graphify`: install the Graphify CLI with `uv tool install graphifyy` (needed for `/graphify` and the Graphify hooks). Then run `/graphify .` in Claude Code to build a knowledge graph of the repo in `graphify-out/`.
6. For claude-mem: run `npx claude-mem install` once on your machine to set up its worker. Run `npx claude-mem telemetry disable` if you don't want anonymous usage analytics.

## What's included

| Path | Purpose |
|---|---|
| `.claude/settings.json` | Enables the ECC, Ponytail, Founder and claude-mem plugins at project scope; Graphify hooks |
| `.claude/rules/ecc/common/` | ECC's language-agnostic rules (coding style, security, testing, git workflow) |
| `.claude/skills/graphify/` | Graphify's `/graphify` skill; its hooks are in `.claude/settings.json` |
| `.claude/skills/archify/` | Archify's diagram and explainer skill (needs Node.js 18+) |
| `.claude/skills/napkin/` | Napkin: Claude keeps a shared runbook of lessons learned |
| `.claude/napkin.md` | The shared napkin runbook (committed) |
| `CLAUDE.md` | Project instructions for Claude Code |
