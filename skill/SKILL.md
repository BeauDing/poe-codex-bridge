---
name: poe-codex-bridge
description: Use Poe's API-first packaged review path on selected local materials, with an optional advanced Claude Code through Poe bridge when live workspace access is required.
---
# poe-codex-bridge

Use this skill when the task calls for:

- a packaged external review through Poe on selected local files
- an optional advanced Claude workspace review through Poe when live repo access is truly required

## When To Use It

Use the packaged review path by default.

It is the right default when:

- the user wants Poe API review without live workspace access
- a packaged external critique is enough
- live workspace access is not required
- the task is rebuttal review, claim review, experiment critique, or decision cross-check

Use the optional workspace path only when the model must inspect the current repository directly.

## Paths

### Default packaged external review path

Use:

- `poe-review`

### Optional Claude-family workspace path

Use:

- `claude-poe`
- `claude-poe-review`

## Core Rule

Do not describe the packaged API review path as having full Claude Code parity.
It is a packaged review path, not a live workspace agent path.

## Practical Guidance

- prefer `poe-review` as the general entrypoint
- prefer exact model ids or alias routing for packaged review
- prefer `claude-poe-review` only when the task is specifically a read-only workspace review
- prefer `claude-poe` only when Claude Code style live inspection is required
