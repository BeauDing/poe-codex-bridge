# Installation

This document is the full setup reference for both manual installation and agent-assisted installation.
If a Codex session or another agent is asked to install this repository, point it here.
Raw form for agent fetch flows:

```text
https://raw.githubusercontent.com/BeauDing/poe-codex-bridge/refs/heads/main/docs/installation.md
```

## Prerequisites

For the main Claude-family path:

- `claude` installed and working
- `poe-code` installed and working
- a valid `POE_API_KEY`

For the packaged external review path:

- `python3`
- the `openai` Python package
- a valid `POE_API_KEY`

## Wrapper Setup

Make the shell entrypoints executable:

```bash
chmod +x bin/claude-poe bin/claude-poe-review bin/poe-external-review
```

Then either:

- add the repository `bin/` directory to `PATH`, or
- symlink the three files into a directory already on `PATH`

These three shell entrypoints are the supported public CLI surface:

- `claude-poe`
- `claude-poe-review`
- `poe-external-review`

Example:

```bash
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
```

At this point the basic workspace wrappers are on `PATH`.

## Credential Setup

Create `~/.config/claude-poe.env`:

```bash
POE_API_KEY=your_poe_api_key
POE_API_BASE_URL=https://api.poe.com/v1
CLAUDE_POE_DEFAULT_MODEL=claude-sonnet-4-6
```

The wrappers and the packaged `poe-external-review` entrypoint load this file automatically unless you override it with `CLAUDE_POE_ENV_FILE`.

## Configuration Precedence

Runtime configuration resolves in this order:

1. environment variables already exported in the current shell
2. `CLAUDE_POE_ENV_FILE`, if set
3. the default file `~/.config/claude-poe.env`
4. code-level defaults such as `claude-sonnet-4-6`

You can start from:

```bash
mkdir -p ~/.config
cp config/claude-poe.env.example ~/.config/claude-poe.env
```

If you only need the Claude-family workspace path, the setup can stop here.

## Python Dependency

The packaged review helpers use the OpenAI SDK against Poe's OpenAI-compatible API:

```bash
python3 -m pip install -r requirements.txt
```

This is only required for the packaged `poe-external-review` path and the direct Poe API helpers.

## Optional Config

Copy the example model aliases if you want alias-based routing:

```bash
cp config/model_aliases.example.json config/model_aliases.json
```

Edit the copied file as needed.

## First Smoke Tests

```bash
claude-poe --wrapper-help
claude-poe models
claude-poe-review --wrapper-help
poe-external-review --help
```

If you are validating the workspace path only, the first three commands are enough.
If you are validating the packaged review path as well, include `poe-external-review --help`.

## Advanced Checks

If you want to validate direct Poe model alias routing after credentials are configured:

```bash
python3 scripts/check_model_aliases.py
```
