# Limitations

## Main Path Limitations

- The stable path is Claude-family only.
- This repository does not claim arbitrary Poe models can act as drop-in Claude Code backends.
- The wrappers assume `claude` and `poe-code` are already installed.

## Auxiliary Path Limitations

- Non-Claude review is packaged-context review, not live workspace execution.
- The reviewer only sees the files or excerpts you send.
- It is intended for critique and second opinions, not primary drafting.

## Security Notes

- Never commit `POE_API_KEY`.
- Redact personal paths, unpublished text, and sensitive content before using the packaged review path.
- Treat all direct Poe API review inputs as externally transmitted content.

