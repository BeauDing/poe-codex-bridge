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

## Why The Split Exists

The main path depends on Claude Code semantics and the Poe bridge around Claude Code.
The auxiliary path only packages selected local materials and forwards them to Poe's direct API.

They are both useful, but they do not provide the same agent capability.

## Command Surface

- [`../bin/claude-poe`](../bin/claude-poe): run Claude Code through Poe
- [`../bin/claude-poe-review`](../bin/claude-poe-review): read-only review prompt on the current workspace
- [`../bin/poe-external-review`](../bin/poe-external-review): package local files and send them to a Poe model via direct API

