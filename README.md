# poe-codex-bridge

Bridge tooling for running Claude Code through Poe on Claude-family models, with an auxiliary packaged-review path for Gemini or other non-Claude second opinions.

## What This Repository Is For

This repository exposes two paths:

- Workspace path: live Claude-family workspace access through Poe
- Packaged review path: direct Poe API review on selected local materials

Use the workspace path when the model should inspect the current repository directly.
Use the packaged review path when a packaged second opinion is enough, or when the target model is not Claude-family.

## Core Boundary

The workspace path is the main product claim.
The packaged review path is useful, but it is not full Claude Code parity and does not provide live workspace access.

This repository is primarily a local bridge and wrapper toolset.
The [`skill/`](skill) directory is optional skill-facing packaging, not the main product surface.

## Quick Start

For manual setup, the shortest path is:

```bash
chmod +x bin/claude-poe bin/claude-poe-review bin/poe-external-review
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
mkdir -p ~/.config
cp config/claude-poe.env.example ~/.config/claude-poe.env
```

If you plan to use the packaged review path, also install:

```bash
python3 -m pip install -r requirements.txt
```

Then try one of the entrypoints:

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

For full step-by-step setup, validation, and troubleshooting, see [docs/installation.md](docs/installation.md).
If you are using Codex or another agent to install this repository, point it to [docs/installation.md](docs/installation.md) rather than relying on the abbreviated README flow.

## More Details

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Capability Matrix](docs/capability-matrix.md)
- [Limitations](docs/limitations.md)
- [Release Checklist](docs/release-checklist.md)
- [OSS Plan](docs/oss.md)
