# Deck outline

Reuse an existing outline when it covers the requested work. For a new deck,
record only decisions needed to write prompts or an editable spec:

```markdown
# Topic
Audience: intended readers
Mode: image or editable
Style: palette, typography hierarchy, background, recurring visual treatment

## 01 — Slide title
Purpose: what the audience should learn
Content: source-backed statements and required labels
Visual: diagram, table, chart or illustration; native objects if editable
Sources: supplied/public sources; mark synthetic examples

## 02 — Slide title
...
```

Respect the requested slide count. Keep source figures and quantitative claims
traceable. For image mode, map each slide to `prompts/NN-slide-slug.md` and its
expected image filename. For editable mode, map it to a stable slide ID in
`slide-spec.json`. This mapping bounds partial revisions and avoids mixing old
pages with new prompts.
