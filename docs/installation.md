# Installation

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

Example:

```bash
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
```

## Credential Setup

Create `~/.config/claude-poe.env`:

```bash
POE_API_KEY=your_poe_api_key
POE_API_BASE_URL=https://api.poe.com/v1
CLAUDE_POE_DEFAULT_MODEL=claude-sonnet-4-6
```

The wrappers and the packaged `poe-external-review` entrypoint load this file automatically unless you override it with `CLAUDE_POE_ENV_FILE`.

You can start from:

```bash
cp config/claude-poe.env.example ~/.config/claude-poe.env
```

## Python Dependency

The packaged review helpers use the OpenAI SDK against Poe's OpenAI-compatible API:

```bash
python3 -m pip install -r requirements.txt
```

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
python3 scripts/check_model_aliases.py
```
