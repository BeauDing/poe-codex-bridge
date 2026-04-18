# poe-codex-bridge

Run Claude Code through Poe for Claude-family models, with an optional direct Poe API path for packaged external review on non-Claude models.

## What This Repository Is

`poe-codex-bridge` has two execution paths with different capabilities:

- Main path: `Claude Code via Poe` for Claude-family models with live local workspace access.
- Auxiliary path: direct Poe API review for Gemini or other non-Claude models on packaged local materials.

The main path is the product claim.
The auxiliary path is useful, but it is not full Claude Code parity.

## Capability Split

| Capability | `claude-poe` / `claude-poe-review` | `poe-external-review` |
| --- | --- | --- |
| Uses Claude Code runtime | Yes | No |
| Sees current workspace directly | Yes | No |
| Can inspect local repo state live | Yes | No |
| Best for code review / repo inspection | Yes | Limited |
| Best for cross-family second opinion | No | Yes |
| Supports Gemini or other non-Claude models | No | Yes |

See [docs/capability-matrix.md](docs/capability-matrix.md) for the longer version.

The repository is named `poe-codex-bridge`, but the public CLI surface still consists of the workspace commands and the packaged review command.
`claude-poe models` prints this wrapper's known-good model names, not Poe's live model catalog.

## Quick Start

### 1. Put the wrappers on your `PATH`

Make the entrypoints executable, then add [`bin/`](bin) to your `PATH` or symlink the three files into a directory already on `PATH`:

```bash
chmod +x bin/claude-poe bin/claude-poe-review bin/poe-external-review
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
```

If you want the packaged `poe-external-review` path, install the Python dependency too:

```bash
python3 -m pip install -r requirements.txt
```

### 2. Create the shared Poe config

You can start from the example file:

```bash
mkdir -p ~/.config
cp config/claude-poe.env.example ~/.config/claude-poe.env
```

The wrappers and the packaged `poe-external-review` path both read `~/.config/claude-poe.env` by default, unless you override it with `CLAUDE_POE_ENV_FILE`.
The file should contain:

```bash
POE_API_KEY=your_poe_api_key
POE_API_BASE_URL=https://api.poe.com/v1
CLAUDE_POE_DEFAULT_MODEL=claude-sonnet-4-6
```

### 3. Run one of the supported commands

For live Claude-family workspace access:

```bash
claude-poe --wrapper-help
claude-poe -p "Summarize the key modules in this repository"
claude-poe-review "Focus on auth and permissions"
```

For packaged non-Claude external review:

```bash
poe-external-review \
  --model-alias balanced_alt \
  --mode experiment-critique \
  --current-reply reply.md \
  --evidence-notes evidence.md
```

For the full installation flow, configuration precedence, alias routing, and smoke tests, see [docs/installation.md](docs/installation.md).

## Repository Layout

- [`bin/`](bin): shell entrypoints
- [`scripts/`](scripts): Python implementation helpers and advanced tooling
- [`config/`](config): model alias examples
- [`docs/`](docs): architecture, installation, capability matrix, limitations, and planning notes
- [`examples/`](examples): sanitized usage examples
- [`skill/`](skill): optional Codex skill packaging

## Scope

This repository is for:

- running Claude Code through Poe for Claude-family models
- read-only workspace review through Poe-backed Claude Code
- packaged external review on local materials through direct Poe API

This repository is not for:

- claiming all Poe models have full Claude Code workspace parity
- shipping an Anthropic-compatible adapter for non-Claude Claude Code execution
- primary drafting through external review scripts

## Key Docs

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Capability Matrix](docs/capability-matrix.md)
- [Limitations](docs/limitations.md)
- [Release Checklist](docs/release-checklist.md)
- [OSS Plan](docs/oss.md)
