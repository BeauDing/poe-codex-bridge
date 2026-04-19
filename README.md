# poe-codex-bridge

API-first skill and wrapper tooling for packaged external review through Poe.
The default path packages selected local materials, sends them to a Poe model, and returns a compact review summary.

An optional advanced path is also included for running Claude Code through Poe on Claude-family models, but that is not the default product surface.

## What This Repository Is For

Primary path:

- packaged external review on selected local files
- exact-model or alias-based routing through Poe's OpenAI-compatible API
- structured review modes for rebuttals, claim checks, experiment critique, and decision cross-checks

Optional advanced path:

- Claude Code workspace access through Poe for Claude-family models only

If you want the smallest setup and the clearest boundary, use the packaged review path.

## Quick Start

Install the default API-first path:

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

The preferred runtime config file is now `~/.config/poe-review.env`.
For compatibility, the wrappers still fall back to `~/.config/claude-poe.env`.
For API-first use, only `POE_API_KEY` and optionally `POE_API_BASE_URL` matter.

## Main Review Modes

- `rebuttal-review`: skeptical rebuttal assessment with minimal edits
- `paper-claim-review`: claim-evidence alignment check
- `experiment-critique`: experiment sufficiency and next-step review
- `decision-cross-check`: independent second opinion on wording, decisions, or plans

## Model Selection

- pass `--model <poe-model-id>` for an exact target model
- use `--model auto` plus alias config for stable local routing
- edit [config/model_aliases.example.json](config/model_aliases.example.json) and copy it to `config/model_aliases.json` if you want alias-based defaults

Command note:

- `poe-review` is the short default alias
- `poe-external-review` remains the underlying explicit entrypoint

## Optional Advanced Path

If you specifically need live workspace inspection through Claude Code, see [docs/advanced-workspace-bridge.md](docs/advanced-workspace-bridge.md).
That path requires additional local tooling and is intentionally documented as advanced setup.

## Repository Layout Note

- top-level packaged-review commands and docs reflect the default API-first product surface
- optional Claude workspace bridge implementation lives under [`extras/claude-workspace-bridge/`](extras/claude-workspace-bridge/)
- short continuity notes for future sessions live in [HANDOFF.md](HANDOFF.md)

## More Details

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Advanced Workspace Bridge](docs/advanced-workspace-bridge.md)
- [Gemini Packaged Review Example](examples/gemini_packaged_review.md)
- [Advanced Claude Workspace Review Example](examples/claude_workspace_review.md)
