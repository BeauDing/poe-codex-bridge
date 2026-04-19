# Installation

This document is the agent-oriented setup reference.
Humans should usually start with the repository `README.md` and use this file only when they want the full step-by-step setup details.

If a Codex session or another agent is asked to install this repository, point it here.
Repository file view:

```text
https://github.com/BeauDing/poe-codex-bridge/blob/main/docs/installation.md
```

## Default Setup: API-First Packaged Review

### Fastest Path

```bash
./scripts/install.sh
```

### Prerequisites

- `python3`
- the `openai` Python package from `requirements.txt`
- a valid `POE_API_KEY`

### Wrapper Setup

Make the default packaged-review entrypoint executable:

```bash
chmod +x bin/poe-review
```

Then either:

- add the repository `bin/` directory to `PATH`, or
- symlink `bin/poe-review` into a directory already on `PATH`

Example:

```bash
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
```

Treat `poe-review` as the normal packaged-review command. The longer internal wrapper name exists for implementation structure, not as the main user-facing command.

### Credential Setup

Create `~/.config/poe-review.env`:

```bash
POE_API_KEY=your_poe_api_key
POE_API_BASE_URL=https://api.poe.com/v1
```

The preferred runtime config file is `~/.config/poe-review.env`.
For compatibility, the wrappers also check `~/.config/claude-poe.env`.
For API-first packaged review, `CLAUDE_POE_DEFAULT_MODEL` is not required.

You can start from:

```bash
mkdir -p ~/.config
cp config/poe-review.env.example ~/.config/poe-review.env
```

### Python Dependency

The packaged review helpers use the OpenAI SDK against Poe's OpenAI-compatible API:

```bash
python3 -m pip install -r requirements.txt
```

### Optional Alias Config

Copy the example model aliases if you want alias-based routing:

```bash
cp config/model_aliases.example.json config/model_aliases.json
```

Edit the copied file as needed.

### First Smoke Tests

```bash
poe-review --help
```

Recommended low-cost real request:

```bash
poe-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply examples/test-fixtures/reply.md \
  --language English \
  --max-output-tokens 1200
```

### Advanced Checks

If you want to validate alias routing after credentials are configured:

```bash
python3 scripts/check_model_aliases.py
```

## Optional Advanced Setup: Claude Workspace Bridge

Only use this path if you specifically need live workspace inspection through Claude Code.

### Additional Prerequisites

- `claude` installed and working
- `poe-code` installed and working

### Additional Wrapper Setup

Make the bridge entrypoints executable:

```bash
chmod +x bin/claude-poe bin/claude-poe-review
```

If you want the helper script to include those advanced wrappers during setup:

```bash
./scripts/install.sh --advanced-claude-bridge
```

They use the same runtime config file as the API-first path.
If you want a default bridge model, add this optional line to `~/.config/poe-review.env`:

```bash
CLAUDE_POE_DEFAULT_MODEL=claude-sonnet-4-6
```

### Optional Advanced Smoke Tests

```bash
claude-poe --wrapper-help
claude-poe models
claude-poe-review --wrapper-help
```

Recommended low-cost real request:

```bash
claude-poe --model claude-haiku-4.5 -p "Reply with exactly: pong"
```

For usage notes and boundaries, see [advanced-workspace-bridge.md](advanced-workspace-bridge.md).

## Configuration Precedence

Runtime configuration resolves in this order:

1. environment variables already exported in the current shell
2. `POE_REVIEW_ENV_FILE`, if set
3. `CLAUDE_POE_ENV_FILE`, if set
4. the preferred default file `~/.config/poe-review.env`
5. the legacy default file `~/.config/claude-poe.env`
6. code-level defaults such as `claude-sonnet-4-6`
