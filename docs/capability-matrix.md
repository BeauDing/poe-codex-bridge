# Capability Matrix

## Main Path: `claude-poe` / `claude-poe-review`

- Claude Code runtime: yes
- Local workspace access: yes
- Live repo inspection: yes
- Tool use through Claude Code: yes
- Best for code review and repository analysis: yes
- Best for Gemini or other non-Claude models: no

## Auxiliary Path: `poe-external-review`

- Claude Code runtime: no
- Local workspace access: no
- Live repo inspection: no
- Tool use through Claude Code: no
- Packaged local file excerpts: yes
- Best for cross-family second opinion: yes

## Interpretation Rule

If the user wants:

- live inspection of the current repository
- a Claude Code style review pass
- a read-only reviewer that can look at actual uncommitted local state

Use the main Claude-family path.

If the user wants:

- Gemini or another non-Claude model
- a second opinion on selected text, rebuttal, experiment notes, or wording
- structured external review on packaged local artifacts

Use the auxiliary path.

## Important Non-Claim

This repository does not currently provide:

- full Claude Code parity for non-Claude models
- an Anthropic-compatible adapter that translates arbitrary Poe models into a stable Claude Code backend

