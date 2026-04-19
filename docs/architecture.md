# Architecture

## Overview

This repository is organized around one primary path and one optional advanced path.

### 1. Primary path: packaged external review

Flow:

`local files -> build_review_prompt.py -> send_and_summarize.py -> Poe OpenAI-compatible API -> target model`

Properties:

- default product surface
- works with arbitrary Poe model ids or local aliases
- does not use Claude Code runtime
- does not expose live workspace state
- best for rebuttal review, claim review, experiment critique, and decision cross-checks

### 2. Optional advanced path: Claude workspace bridge

Flow:

`Claude Code -> claude-poe -> poe-code wrap claude -> Poe -> Claude-family model`

Properties:

- uses the Claude Code runtime directly
- can inspect the current working directory live
- best for repository inspection and read-only workspace review
- limited to Claude-family models in the current supported path

## Capability Comparison

### Primary packaged external review

- Claude Code runtime: no
- live workspace access: no
- packaged local file excerpts: yes
- any Poe model id: yes
- easiest installation path: yes
- best fit for skill-style external critique: yes

### Optional Claude workspace bridge

- Claude Code runtime: yes
- live workspace access: yes
- packaged local file excerpts: optional only
- any Poe model id: no
- easiest installation path: no
- best fit for direct repository inspection: yes

## Which Path To Use

Use the primary packaged external review path when you want:

- the smallest setup
- any Poe model through the API-first packaged path
- review on selected local text, notes, rebuttals, or evidence packages
- a clear external-review boundary without workspace access

Use the optional Claude workspace bridge when you want:

- live inspection of the current repository
- a Claude Code style review pass
- a read-only reviewer that can inspect actual uncommitted local state

## Why This Split Exists

The primary path is a straightforward skill pipeline.
It packages selected inputs, sends them to Poe, and summarizes the response.

The optional advanced path depends on Claude Code semantics and local bridge tooling.
It is more capable for workspace inspection, but it is also more complex to install and reason about.

## Important Limits

- the primary path is packaged-context review, not live workspace execution
- the packaged reviewer only sees the files or excerpts you send
- the packaged path is intended for critique and second opinions, not primary drafting
- the optional workspace bridge is Claude-family only
- this repository does not claim arbitrary Poe models can act as drop-in Claude Code backends
- the optional bridge assumes `claude` and `poe-code` are already installed

This repository does not currently provide:

- full Claude Code parity through the packaged API path
- an adapter that translates arbitrary Poe models into a stable Claude Code backend

## Security Notes

- never commit `POE_API_KEY`
- redact personal paths, unpublished text, and sensitive content before using the packaged review path
- treat all direct Poe API review inputs as externally transmitted content

## Command Surface

- [`../bin/poe-review`](../bin/poe-review): short default alias for packaged review through Poe API
- [`../bin/poe-external-review`](../bin/poe-external-review): package local files and send them to a Poe model via direct API
- [`../bin/claude-poe`](../bin/claude-poe): optional advanced bridge for Claude Code through Poe
- [`../bin/claude-poe-review`](../bin/claude-poe-review): optional read-only workspace review wrapper
