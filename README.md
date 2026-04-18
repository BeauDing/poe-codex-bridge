# poe-codex-bridge

Skill repository for using Claude Code through Poe on Claude-family models, with an auxiliary packaged-review path for Gemini or other non-Claude second opinions.

## What This Skill Is For

This repository exposes two paths:

- Workspace path: live Claude-family workspace access through Poe
- Packaged review path: direct Poe API review on selected local materials

Use the workspace path when the model should inspect the current repository directly.
Use the packaged review path when a packaged second opinion is enough, or when the target model is not Claude-family.

## Core Boundary

The workspace path is the main product claim.
The packaged review path is useful, but it is not full Claude Code parity and does not provide live workspace access.

## Quick Start

1. Put the wrappers on your `PATH`:

```bash
chmod +x bin/claude-poe bin/claude-poe-review bin/poe-external-review
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
```

If you plan to use the packaged review path, also install:

```bash
python3 -m pip install -r requirements.txt
```

2. Create the shared Poe config:

```bash
mkdir -p ~/.config
cp config/claude-poe.env.example ~/.config/claude-poe.env
```

3. Use one of the entrypoints:

```bash
claude-poe --wrapper-help
claude-poe-review "Focus on auth and permissions"
```

```bash
poe-external-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply reply.md
```

## More Details

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Capability Matrix](docs/capability-matrix.md)
- [Limitations](docs/limitations.md)
- [Release Checklist](docs/release-checklist.md)
