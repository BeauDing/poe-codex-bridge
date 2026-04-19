# Advanced Workspace Bridge

This path is optional.
Use it only when you specifically need live workspace inspection through Claude Code on Poe.

The public entrypoints remain in `bin/`, while the advanced implementation now lives under `extras/claude-workspace-bridge/`.

## What It Does

Flow:

`Claude Code -> claude-poe -> poe-code wrap claude -> Poe -> Claude-family model`

This path can inspect the current working directory directly and is useful for repository analysis or read-only workspace review.

## Additional Requirements

- `claude` installed and working
- `poe-code` installed and working
- a valid `POE_API_KEY`

## Setup

Make the bridge entrypoints executable:

```bash
chmod +x bin/claude-poe bin/claude-poe-review
```

Add the repository `bin/` directory to `PATH` if you have not already done so:

```bash
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
```

The bridge wrappers read the same runtime config file as the API-first packaged review path:

```bash
~/.config/poe-review.env
```

For compatibility, they also fall back to:

```bash
~/.config/claude-poe.env
```

Optional default model:

```bash
CLAUDE_POE_DEFAULT_MODEL=claude-sonnet-4-6
```

## Basic Commands

Show wrapper help:

```bash
claude-poe --wrapper-help
claude-poe-review --wrapper-help
```

Show the wrapper's known-good model names:

```bash
claude-poe models
```

Run a low-cost request:

```bash
claude-poe --model claude-haiku-4.5 -p "Reply with exactly: pong"
```

Run a read-only workspace review:

```bash
claude-poe-review "Focus on auth checks and brittle tests"
```

## Limits

- this path is Claude-family only
- it is not a generic backend for arbitrary Poe models
- it depends on local `claude` and `poe-code` behavior
- it is more complex to install and troubleshoot than the packaged review path

If you do not need live workspace access, return to the default API-first path in [installation.md](installation.md).
