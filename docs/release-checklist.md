# Release Checklist

## Minimum Publish Pass

- confirm no local usernames, machine-specific paths, or private excerpts remain
- confirm `README.md` presents packaged Poe review as the default path
- confirm `LICENSE` matches the intended public license
- confirm `config/poe-review.env.example` has no real credentials
- confirm `config/claude-poe.env.example` has no real credentials
- confirm `config/model_aliases.example.json` contains only safe example aliases

## Core Functional Checks

- run `poe-review --help`
- run one real low-cost packaged review request
- run `python3 scripts/check_model_aliases.py` if alias routing is part of the release

Recommended low-cost smoke test:

```bash
poe-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply examples/test-fixtures/reply.md \
  --language English \
  --max-output-tokens 1200
```

Notes:

- prefer `gemini-3-flash` for routine smoke tests unless you are explicitly validating a different alias or model family
- do not use higher-cost models for routine smoke tests

## Optional Advanced Bridge Checks

Run these only if the Claude workspace bridge is included in the release scope:

- run `claude-poe --wrapper-help`
- run `claude-poe models`
- run `claude-poe-review --wrapper-help`
- run one real low-cost Claude-family request

Recommended low-cost bridge smoke test:

```bash
claude-poe --model claude-haiku-4.5 -p "Reply with exactly: pong"
```

- prefer `claude-haiku-4.5` for the Claude-family smoke test unless a specific compatibility issue requires another model

## Documentation Checks

- verify installation steps match the current file layout
- verify the main claim is packaged review through Poe API
- verify the optional Claude bridge is clearly labeled as advanced
- verify packaged review is still described as packaged-context review
- verify `claude-poe models` is documented as a known-good local list rather than a live Poe catalog

## Optional Before First Public Push

- add a short changelog or release notes
- add GitHub issue templates if the repo will be actively maintained
- decide whether a `CONTRIBUTING.md` file is worth adding
