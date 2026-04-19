# HANDOFF

Use this file as the short handoff layer for ongoing work in this repository.

Keep it brief. Update it at milestones, before `/clear`, or before stopping a long session.

## Status
- `complete`

## Last Updated
- `2026-04-19 HKT`

## Applies To
- `poe-codex-bridge` product positioning, default command/config naming, and optional advanced Claude workspace bridge layout.

## Goal
- Keep this repository API-first.
- Keep packaged Poe review as the default product surface.
- Keep the Claude workspace bridge available only as an optional advanced path.

## Current State
- Repository location:
  - `/hdd/dingbo/github/poe-codex-bridge`
- GitHub remote:
  - `https://github.com/BeauDing/poe-codex-bridge.git`
- Public default command:
  - `poe-review`
- Underlying explicit packaged-review command:
  - `poe-external-review`
- Preferred runtime config:
  - `~/.config/poe-review.env`
- Legacy-compatible runtime config fallback:
  - `~/.config/claude-poe.env`
- Optional advanced Claude bridge entrypoints remain in:
  - `bin/claude-poe`
  - `bin/claude-poe-review`
- The advanced Claude bridge implementation now lives under:
  - `extras/claude-workspace-bridge/`

## Confirmed Facts
- `README.md`, `docs/installation.md`, and `docs/architecture.md` now treat packaged review as the default path.
- `docs/advanced-workspace-bridge.md` is the canonical place for Claude workspace bridge setup and limits.
- `bin/claude-poe` and `bin/claude-poe-review` are compatibility entrypoints that delegate to `extras/claude-workspace-bridge/`.
- `scripts/runtime_env.py` and `scripts/runtime_env.sh` now prefer `poe-review.env` and still accept legacy `claude-poe.env`.
- The sibling `codex-skills` repository has been updated so the local `poe-external-review` skill matches this API-first positioning.

## Verification
- `python3 -m unittest tests/test_runtime_env.py`
- `python3 -m unittest tests/test_packaged_review_helpers.py`
- `python3 -m unittest tests/test_cli_wrappers.py`
- `bin/poe-review --help`

## Key Files
- `README.md`
- `HANDOFF.md`
- `bin/poe-review`
- `bin/poe-external-review`
- `docs/installation.md`
- `docs/architecture.md`
- `docs/advanced-workspace-bridge.md`
- `scripts/runtime_env.py`
- `scripts/runtime_env.sh`
- `extras/claude-workspace-bridge/`

## Avoid
- Do not present the Claude workspace bridge as the default product path.
- Do not describe packaged Poe review as live workspace access.
- Do not remove legacy `claude-poe.env` compatibility unless all dependent local tooling has been migrated.
