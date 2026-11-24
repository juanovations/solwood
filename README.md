# Solwood

A new project, set up for Claude Code with [ECC](https://github.com/affaan-m/ECC).

## Getting started with Claude Code

1. Install Claude Code 2.1 or newer, Node.js 18+, and Git.
2. Open this folder in Claude Code. It reads `.claude/settings.json`, which declares the ECC marketplace and enables the `ecc@ecc` plugin for this project. Accept the prompt to trust the marketplace and install the plugin.
3. Optional: run `/plugin configure ecc@ecc` to pick a hook profile (`minimal`, `standard` or `strict`; default `standard`) or turn hooks off.

## What's included

| Path | Purpose |
|---|---|
| `.claude/settings.json` | Enables the ECC plugin at project scope |
| `.claude/rules/ecc/common/` | ECC's language-agnostic rules (coding style, security, testing, git workflow) |
| `CLAUDE.md` | Project instructions for Claude Code |
