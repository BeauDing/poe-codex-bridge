# Architecture

## Overview

This repository intentionally exposes two different execution paths.

### 1. Claude-family workspace path

Flow:

`Claude Code -> claude-poe -> poe-code wrap claude -> Poe -> Claude-family model`

Properties:

- uses the Claude Code runtime directly
- sees the current working directory live
- best for repository inspection and code review
- limited to Claude-family models in the current supported path

### 2. Packaged external review path

Flow:

`local files -> build_review_prompt.py -> send_and_summarize.py -> Poe OpenAI-compatible API -> target model`

Properties:

- does not use Claude Code runtime
- does not have live workspace access
- works well for Gemini or other non-Claude second opinions
- best for rebuttal review, claim review, experiment critique, and wording checks

## Capability Comparison

### Claude-family workspace path

- Claude Code runtime: yes
- local workspace access: yes
- live repo inspection: yes
- tool use through Claude Code: yes
- best for code review and repository analysis: yes
- best for Gemini or other non-Claude models: no

### Packaged external review path

- Claude Code runtime: no
- local workspace access: no
- live repo inspection: no
- tool use through Claude Code: no
- packaged local file excerpts: yes
- best for cross-family second opinion: yes

## Which Path To Use

Use the Claude-family workspace path when the user wants:

- live inspection of the current repository
- a Claude Code style review pass
- a read-only reviewer that can look at actual uncommitted local state

Use the packaged external review path when the user wants:

- Gemini or another non-Claude model
- a second opinion on selected text, rebuttal, experiment notes, or wording
- structured external review on packaged local artifacts

## Why The Split Exists

The main path depends on Claude Code semantics and the Poe bridge around Claude Code.
The auxiliary path only packages selected local materials and forwards them to Poe's direct API.

They are both useful, but they do not provide the same agent capability.

## Important Limits

- the stable workspace path is Claude-family only
- this repository does not claim arbitrary Poe models can act as drop-in Claude Code backends
- non-Claude review is packaged-context review, not live workspace execution
- the packaged reviewer only sees the files or excerpts you send
- the packaged path is intended for critique and second opinions, not primary drafting
- the wrappers assume `claude` and `poe-code` are already installed

This repository does not currently provide:

- full Claude Code parity for non-Claude models
- an Anthropic-compatible adapter that translates arbitrary Poe models into a stable Claude Code backend

## Security Notes

- never commit `POE_API_KEY`
- redact personal paths, unpublished text, and sensitive content before using the packaged review path
- treat all direct Poe API review inputs as externally transmitted content

## Command Surface

- [`../bin/claude-poe`](../bin/claude-poe): run Claude Code through Poe
- [`../bin/claude-poe-review`](../bin/claude-poe-review): read-only review prompt on the current workspace
- [`../bin/poe-external-review`](../bin/poe-external-review): package local files and send them to a Poe model via direct API
