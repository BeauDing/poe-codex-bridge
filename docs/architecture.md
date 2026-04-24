# Architecture

## Overview

This repository is organized around one explicit path: packaged external review through Poe's API.

### Packaged external review

Flow:

`local files -> build_review_prompt.py -> send_and_summarize.py -> Poe OpenAI-compatible API -> target model`

Properties:

- default product surface
- works with arbitrary Poe model ids or local aliases
- does not expose live workspace state
- best for rebuttal review, claim review, experiment critique, and decision cross-checks

## Capability Comparison

- live workspace access: no
- packaged local file excerpts: yes
- any Poe model id: yes
- easiest installation path: yes
- best fit for skill-style external critique: yes

## Which Path To Use

Use this repository when you want:

- the smallest setup
- any Poe model through the API-first packaged path
- review on selected local text, notes, rebuttals, or evidence packages
- a clear external-review boundary without workspace access

## Why This Design Exists

This repository is a straightforward skill pipeline.
It packages selected inputs, sends them to Poe, and summarizes the response.

## Important Limits

- the repository only supports packaged-context review, not live workspace execution
- the packaged reviewer only sees the files or excerpts you send
- the packaged path is intended for critique and second opinions, not primary drafting

This repository does not currently provide:

- live workspace inspection
- direct repository execution on the remote model side
- an adapter that turns arbitrary Poe models into workspace-style backends

## Security Notes

- never commit `POE_API_KEY`
- redact personal paths, unpublished text, and sensitive content before using the packaged review path
- treat all direct Poe API review inputs as externally transmitted content

## Command Surface

- [`../bin/poe-review`](../bin/poe-review): short default alias for packaged review through Poe API
- [`../bin/poe-external-review`](../bin/poe-external-review): package local files and send them to a Poe model via direct API
