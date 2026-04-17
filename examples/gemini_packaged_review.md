# Gemini Packaged Review Example

Run a Gemini-based external review on packaged local materials:

```bash
poe-external-review \
  --model-alias balanced_alt \
  --mode rebuttal-review \
  --reviewer-comments review.md \
  --current-reply reply.md \
  --evidence-notes evidence.md \
  --summary-file rebuttal.summary.md
```

This path does not expose the live workspace.
It only sends the packaged inputs you select.

