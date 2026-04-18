---
name: poe-codex-bridge
description: Use Claude Code through Poe for Claude-family workspace access, or use the packaged direct Poe API path for non-Claude external review on selected local materials.
---
# poe-codex-bridge

Use this skill when the task calls for either:

- Claude-family review or coding work through Poe with live workspace access
- a packaged second opinion through Poe on selected local files

## When To Use It

Use the workspace path when the model should inspect the current repository directly.

Use the packaged review path when:

- the user explicitly wants Gemini or another non-Claude model
- a packaged external critique is enough
- live workspace access is not required

## Paths

### Claude-family workspace path

Use:

- `claude-poe`
- `claude-poe-review`

### Packaged external review path

Use:

- `poe-external-review`

## Core Rule

Do not describe the packaged non-Claude path as having full Claude Code parity.
It is a packaged review path, not a live workspace agent path.

## Practical Guidance

- prefer `claude-poe` as the general workspace entrypoint
- prefer `claude-poe-review` when the task is specifically a read-only code review
- prefer `poe-external-review` only when packaged review is acceptable or a non-Claude model is required
