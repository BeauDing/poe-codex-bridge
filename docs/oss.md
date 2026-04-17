# Open Source Plan

This file tracks open-source preparation work for this repository.

The current focus is the `Poe + Claude Code` line, with packaged `Poe External Review` kept as a secondary capability inside the broader repository.

## Packaging Decision

- the public repository should be framed around `Claude Code via Poe`
- the main public claim should be Claude-family local workspace access through Poe
- direct Poe API review for Gemini or other non-Claude models should remain an auxiliary path
- do not market the repository as "any Poe model in Claude Code" without an actual Anthropic-compatible adapter for non-Claude models

## Repository Shape

Preferred repository name:

- `poe-codex-bridge`

Current layout:

- `bin/claude-poe`
- `bin/claude-poe-review`
- `bin/poe-external-review`
- `scripts/`
- `config/`
- `docs/`
- `examples/`
- `skill/`

## Product Boundary

### Main claim

- `Claude Code via Poe` is the core product story
- Claude-family models get local workspace access through the existing wrappers
- this is the tested and strongest path

### Auxiliary claim

- direct Poe API review for Gemini or other non-Claude models remains available
- this path is useful for second opinions and external review on packaged local materials
- this path should not be described as equivalent to full Claude Code workspace access

## Minimum Release Bar

Do not publish the first public repository until the following conditions are satisfied:

- the exported tooling runs in a clean environment outside the current local setup
- no local machine paths, usernames, unpublished text, or sensitive raw artifacts remain
- the README explains the capability split between execution paths
- at least two sanitized example cases are included and reproducible
- required environment variables are documented
- known limitations are stated explicitly

## Remaining Work

- decide whether to add a `LICENSE` file and which license to use
- validate at least one `claude-poe-review` workspace case from the new repo
- validate at least one Gemini packaged-review case from the new repo
- clean any remaining machine-specific assumptions from helper scripts and docs
