# Release Checklist

## Minimum Publish Pass

- confirm no local usernames, machine-specific paths, or private excerpts remain
- confirm `README.md` still describes the capability split correctly
- confirm `LICENSE` matches the intended public license
- confirm `config/claude-poe.env.example` has no real credentials
- confirm `config/model_aliases.example.json` contains only safe example aliases

## Functional Checks

- run `claude-poe --wrapper-help`
- run `claude-poe models`
- run `claude-poe-review --wrapper-help`
- run one real low-cost Claude-family request
- run one real low-cost packaged non-Claude request

Recommended low-cost smoke tests:

```bash
claude-poe --model claude-haiku-4.5 -p "Reply with exactly: pong"
```

```bash
poe-external-review \
  --model gemini-3-flash \
  --mode decision-cross-check \
  --current-reply reply.md \
  --language English \
  --max-output-tokens 1200
```

Notes:

- prefer `claude-haiku-4.5` for the Claude-family smoke test unless a specific compatibility issue requires another model
- prefer `gemini-3-flash` for the packaged non-Claude smoke test unless you are explicitly validating a different alias or model family
- do not use higher-cost models for routine smoke tests

## Documentation Checks

- verify installation steps match the current file layout
- verify the main claim is still `Claude Code via Poe`
- verify non-Claude review is still described as packaged-context review
- verify `claude-poe models` is documented as a known-good local list rather than a live Poe catalog

## Optional Before First Public Push

- add a short changelog or release notes
- add GitHub issue templates if the repo will be actively maintained
- decide whether a `CONTRIBUTING.md` file is worth adding
