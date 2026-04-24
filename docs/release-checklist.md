# Release Checklist

## Minimum Publish Pass

- confirm no local usernames, machine-specific paths, or private excerpts remain
- confirm `README.md` presents packaged Poe review as the default path
- confirm `LICENSE` matches the intended public license
- confirm `config/poe-review.env.example` has no real credentials
- confirm `config/model_aliases.example.json` contains only safe example aliases
- confirm `scripts/install.sh` still matches the documented quick-start path

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

## Documentation Checks

- verify installation steps match the current file layout
- verify the main claim is packaged review through Poe API
- verify packaged review is still described as packaged-context review

## Optional Before First Public Push

- add a short changelog or release notes
- add GitHub issue templates if the repo will be actively maintained
- decide whether a `CONTRIBUTING.md` file is worth adding
