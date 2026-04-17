---
name: poe-codex-bridge
description: Use Claude Code through Poe for Claude-family workspace access, or use the packaged direct Poe API path for non-Claude external review on selected local materials.
---
# poe-codex-bridge

Use this repository when the task calls for either:

- Claude-family review or coding work through Poe with live workspace access
- a packaged second opinion through Poe on selected local files

## Execution Paths

### Claude-family workspace path

Use:

- `claude-poe`
- `claude-poe-review`

Choose this path when the model should inspect the current repository directly.

### Packaged external review path

Use:

- `poe-external-review`
- `scripts/send_and_summarize.py`

Choose this path when the user explicitly wants Gemini or another non-Claude model, or when a packaged external critique is enough.

## Core Rule

Do not describe the packaged non-Claude path as having full Claude Code parity.
It is a packaged review path, not a live workspace agent path.
