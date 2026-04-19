# Gemini Packaged Review Example

Run a Gemini-based external review on packaged local materials:

```bash
poe-review \
  --model-alias balanced_alt \
  --mode rebuttal-review \
  --reviewer-comments examples/test-fixtures/review.md \
  --current-reply examples/test-fixtures/reply.md \
  --evidence-notes examples/test-fixtures/evidence.md \
  --summary-file rebuttal.summary.md
```

This path does not expose the live workspace.
It only sends the packaged inputs you select.

Typical response shape:

- summary metadata
- verdict
- top risks
- best next moves
- optional direct edits
