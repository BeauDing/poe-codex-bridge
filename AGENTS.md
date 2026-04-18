# Repository Agent Rules

Read `README.md` at session start, when repository context is unclear, or when the task touches scope, capability claims, CLI behavior, installation, or release-facing documentation. Do not reread it for every small follow-up if the relevant context is already established.

When updating this repository:

- if `HANDOFF.md` exists, read it first after `/clear` or at the start of a fresh continuation, and use it only when its scope clearly matches the current task
- use `HANDOFF.md` as short-term task continuity, not as a replacement for `README.md` or this file
- update `HANDOFF.md` only at explicit handoff points such as immediately before `/clear`, before stopping a long session, or when the user explicitly asks for a handoff summary
- keep the core product boundary clear: the workspace commands are the main path; the packaged review command is an auxiliary path
- do not describe the non-Claude path as having full Claude Code parity, live workspace access, or drop-in backend equivalence
- treat `bin/claude-poe`, `bin/claude-poe-review`, and `bin/poe-external-review` as the supported public CLI surface
- treat `scripts/*.py` as implementation helpers unless the task explicitly needs lower-level control
- keep runtime env loading consistent across wrappers and Python helpers; prefer shared logic over duplicated env parsing
- keep `README.md`, `docs/`, examples, and wrapper behavior aligned when capability wording or CLI behavior changes
- never commit real `POE_API_KEY`, personal paths, or unsanitized review materials
- prefer lightweight local verification for wrapper behavior and env loading before claiming a change is complete
- when verifying tests, prefer the repository's current standard library test path unless the test runner setup is intentionally changed

Use this repository primarily for:

- Claude Code via Poe for Claude-family workspace access
- read-only workspace review through Poe-backed Claude Code
- packaged external review on selected local materials through Poe API
- documenting the capability split and release-safe usage

Do not use this repository as the place for:

- claiming arbitrary Poe models are full Claude Code backends
- storing secrets or raw sensitive review payloads
- turning packaged review tooling into a general live-agent parity claim
