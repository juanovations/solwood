# CLAUDE.md

Guidance for Claude Code when working in the Solwood repository.

## Project

Solwood is a new project. Describe what it does, its stack, and how to run and test it here as it takes shape.

## ECC

This repo uses [ECC](https://github.com/affaan-m/ECC) as a project-scoped Claude Code plugin (`ecc@ecc`, declared in `.claude/settings.json`).

- Skills, agents, commands and hooks come from the plugin. Use `/ecc:configure-ecc` to change the hook profile or other ECC settings.
- Always-loaded rules live in `.claude/rules/ecc/common`. When the stack is chosen, copy the matching language pack (for example `rules/typescript` or `rules/python` from the ECC repo) into `.claude/rules/ecc/`.
- Do not also run a manual ECC install into this project; stacking installs duplicates skills and hooks.
