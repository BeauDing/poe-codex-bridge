# poe-codex-bridge

This repository is for running review-style workflows through Poe.

The default path is simple: package a few local files, send them to a Poe model, and get back a structured second opinion. That is the main product surface now, and it works well for rebuttal review, claim checking, experiment critique, and decision cross-checks.

There is also an optional advanced path for running Claude Code through Poe on Claude-family models, but that is no longer the default setup or the main story of the repository.

If you want the smallest setup and the clearest behavior, start with the packaged review path.

## Quick Start

Install the default packaged-review path:

```bash
chmod +x bin/poe-external-review bin/poe-review
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
python3 -m pip install -r requirements.txt
mkdir -p ~/.config
cp config/poe-review.env.example ~/.config/poe-review.env
```

Then run a low-cost packaged review:

```bash
poe-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply examples/test-fixtures/reply.md
```

For the default API-first flow, the preferred runtime config file is `~/.config/poe-review.env`. Only `POE_API_KEY` is required. `POE_API_BASE_URL` is optional. For compatibility, the wrappers still fall back to `~/.config/claude-poe.env`.

For a human reader, the README should be enough to understand what this repository is for and how to get started. The full [docs/installation.md](docs/installation.md) file is mainly there as a step-by-step setup reference for Codex or other agents. If you want an agent to install this repository, point it there directly instead of asking it to infer setup from the homepage. A good prompt is:

```text
Open and follow instructions from https://github.com/BeauDing/poe-codex-bridge/blob/main/docs/installation.md
```

## What You Can Use It For

The default packaged-review path supports:

- rebuttal review
- paper claim review
- experiment critique
- decision cross-checks
- exact model ids or alias-based routing through Poe's OpenAI-compatible API

## Main Review Modes

- `rebuttal-review`: skeptical rebuttal assessment with minimal edits
- `paper-claim-review`: claim-evidence alignment check
- `experiment-critique`: experiment sufficiency and next-step review
- `decision-cross-check`: independent second opinion on wording, decisions, or plans

## Model Selection

- pass `--model <poe-model-id>` for an exact target model
- use `--model auto` plus alias config for stable local routing
- edit [config/model_aliases.example.json](config/model_aliases.example.json) and copy it to `config/model_aliases.json` if you want alias-based defaults

`poe-review` is the short default command. `poe-external-review` remains the explicit underlying entrypoint.

## Optional Advanced Path

If you specifically need live workspace inspection through Claude Code, use the advanced path described in [docs/advanced-workspace-bridge.md](docs/advanced-workspace-bridge.md). That path requires extra local tooling and is intentionally documented separately so the default setup stays simple.

## Repository Layout Note

The top-level commands and docs reflect the API-first packaged-review workflow. The optional Claude workspace bridge implementation lives under [`extras/claude-workspace-bridge/`](extras/claude-workspace-bridge/). Short continuity notes for future sessions live in [HANDOFF.md](HANDOFF.md).

## More Details

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Advanced Workspace Bridge](docs/advanced-workspace-bridge.md)
- [Gemini Packaged Review Example](examples/gemini_packaged_review.md)
- [Advanced Claude Workspace Review Example](examples/claude_workspace_review.md)
