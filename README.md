# poe-codex-bridge

`poe-codex-bridge` is a small API-first tool for running external reviews through [Poe](https://poe.com/).

It lets Codex package a focused set of local materials, send them to a Poe model, and get back a structured second opinion for rebuttal review, claim checking, experiment critique, and decision cross-checks.

The repository intentionally stays on one path only:

- packaged local context
- Poe's OpenAI-compatible API
- no live workspace inspection
- no remote execution

## Quick Start

Install the default packaged-review path:

```bash
./scripts/install.sh
```

Then run a low-cost packaged review:

```bash
./bin/poe-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply examples/test-fixtures/reply.md
```

Create `~/.config/poe-review.env` with:

```bash
POE_API_KEY=your_poe_api_key
POE_API_BASE_URL=https://api.poe.com/v1
```

Only `POE_API_KEY` is required. `POE_API_BASE_URL` is optional.

If you prefer to do the setup manually instead of using the helper script:

```bash
chmod +x bin/poe-review
export PATH="/path/to/poe-codex-bridge/bin:$PATH"
python3 -m pip install -r requirements.txt
mkdir -p ~/.config
cp config/poe-review.env.example ~/.config/poe-review.env
```

For a human reader, this README should be enough to understand the tool and get started. The full [docs/installation.md](docs/installation.md) file is mainly there as a step-by-step setup reference for Codex or other agents. If you want an agent to install this repository, point it there directly instead of asking it to infer setup from the homepage. A good prompt is:

```text
Open and follow instructions from https://github.com/BeauDing/poe-codex-bridge/blob/main/docs/installation.md
```

## What You Can Use It For

This packaged-review path supports:

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

Use `poe-review` as the default packaged-review command.

## Why It Exists

- keep Codex as the primary worker
- add an external reviewer without giving it live repo access
- make Poe model choice explicit and reproducible
- keep the public surface small enough to install and reason about quickly

## Repository Layout Note

The top-level commands and docs all reflect the same API-first packaged-review workflow. This repository is meant to stay small, explicit, and safe for open-source release.

## More Details

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Gemini Packaged Review Example](examples/gemini_packaged_review.md)
