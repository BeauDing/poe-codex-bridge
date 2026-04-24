---
name: poe-codex-bridge
description: Use Poe's API-first packaged review path on selected local materials for external review without live workspace access.
---
# poe-codex-bridge

Use this skill when the task calls for:

- a packaged external review through Poe on selected local files

## When To Use It

- the user wants Poe API review without live workspace access
- a packaged external critique is enough
- live workspace access is not required
- the task is rebuttal review, claim review, experiment critique, or decision cross-check

## Paths

Use:

- `poe-review`

## Core Rule

Do not describe this skill as having live workspace access.
It is a packaged review path, not a workspace agent path.

## Practical Guidance

- prefer `poe-review` as the general entrypoint
- prefer exact model ids or alias routing for packaged review
