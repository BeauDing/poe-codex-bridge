# poe-codex-bridge

`poe-codex-bridge` is a small bridge for running packaged external reviews through [Poe](https://poe.com/).

Use it when you want Codex to stay the main worker, but you also want a second opinion from a Poe-hosted model on a bounded set of local materials.

## What It Is

- a packaged review tool
- a small command-line bridge around `poe-review`
- a way to send selected files or text to Poe for external critique

## What It Is Not

- not a live workspace agent
- not remote execution
- not full repo browsing through Poe

## Common Uses

- rebuttal review
- claim checking
- experiment critique
- decision cross-checks
- wording or messaging review before you finalize something

## Quick Start

Install the bridge:

```bash
./scripts/install.sh
```

Create `~/.config/poe-review.env`:

```bash
POE_API_KEY=your_poe_api_key
```

Then run a small smoke test:

```bash
poe-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply examples/test-fixtures/reply.md
```

`POE_API_BASE_URL` is optional. The default Poe API endpoint is already what most users want.

## Commands

- `poe-review`
  normal user-facing command
- `poe-external-review`
  compatibility / implementation wrapper

## Skill Note

If you use Codex skills, this repository is the runtime bridge, not the main skill library.

The corresponding Poe review skill lives in the sibling `codex-skills` repository. In normal use:

- install this repo so `poe-review` is available
- install or sync the `poe-review` skill from your skill repo

## Model Selection

- pass `--model <poe-model-id>` for an exact model
- use `--model auto` if you want local alias routing
- copy `config/model_aliases.example.json` to `config/model_aliases.json` if you want editable aliases

## Read More

- [Installation](docs/installation.md)
- [Architecture](docs/architecture.md)
- [Gemini Packaged Review Example](examples/gemini_packaged_review.md)
