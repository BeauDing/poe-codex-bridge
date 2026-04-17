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

## Documentation Checks

- verify installation steps match the current file layout
- verify the main claim is still `Claude Code via Poe`
- verify non-Claude review is still described as packaged-context review

## Optional Before First Public Push

- add a short changelog or release notes
- add GitHub issue templates if the repo will be actively maintained
- decide whether a `CONTRIBUTING.md` file is worth adding

