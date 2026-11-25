# Napkin Runbook

## Curation Rules
- Re-prioritize on every read.
- Keep recurring, high-value notes only.
- Max 10 items per category.
- Each item includes date + "Do instead".

## Execution & Validation (Highest Priority)
1. **[2026-11-25] Adding a new tool to Solwood means docs too**
   Do instead: after installing a plugin or skill, update the matching sections in `CLAUDE.md` and `README.md` in the same commit.
2. **[2026-11-25] Inspect third-party repos before adding them**
   Do instead: clone to a scratch path outside the repo, check for hooks, network calls and dependencies, then report before copying anything in.

## Shell & Command Reliability
1. **[2026-11-25] ECC's Fact-Forcing Gate blocks the first Bash call each session and any `rm -rf`**
   Do instead: state the user's request and what the command does (for deletes: files touched, rollback, the user's exact words), then retry.
2. **[2026-11-25] `graphify extract .` refuses to run without an LLM API key when docs exist**
   Do instead: use `graphify extract . --code-only` for a local, keyless graph, or ask the user for a key.
3. **[2026-11-25] `git push` prints "push negotiation failed"**
   Do instead: ignore it if the ref update line appears; confirm with `git status -sb` after `git fetch`.

## Domain Behavior Guardrails
1. **[2026-11-25] `claude plugin install --scope project` reorders `.claude/settings.json`**
   Do instead: check the diff only adds the new plugin and marketplace; the Graphify hooks must stay.
2. **[2026-11-25] ECC security and testing rules outrank Ponytail's "write less"**
   Do instead: when they conflict, follow ECC.

## User Directives
1. **[2026-11-25] A bare repo link is not a request to install it**
   Do instead: inspect it, summarize what it is and how it would install, and ask before adding it to Solwood.
2. **[2026-11-25] `.claude/napkin.md` is committed and shared**
   Do instead: keep entries free of secrets and personal details; commit napkin updates with related work.
