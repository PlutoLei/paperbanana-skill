---
name: paperbanana-slide-deck
description: Create or revise a complete PaperBanana slide deck, including image slides and native editable PowerPoint text, tables, charts and diagrams. Use for PaperBanana deck requests; preserve the user's selected presentation tool and existing deck mode.
---

# PaperBanana slide deck

Two output modes share content planning and final inspection:

- **image**: per-slide prompts → generated full-slide images → PPTX assembly.
- **editable**: `slide-spec.json` → native PowerPoint objects → rendered previews
  → review → targeted spec edits → rebuild.

## Resolve this bundle

`BUNDLE_DIR` is the absolute directory containing **this file**, `package.json`,
`scripts/` and `references/`. A plugin host may discover the small entrypoint in
`skills/paperbanana-slide-deck/`; that entrypoint points here, two levels above it.
Use the path supplied by the host, not a search of another runtime's directories.

Before building, verify `scripts/build-deck.ts` exists and run
`bun install --frozen-lockfile` in `BUNDLE_DIR` when dependencies are absent.
Only copying the nested discovery file is not a complete installation.
The local editable renderer needs Bun, not an image API or Python backend.

## Select mode and scope

For a plan or read-only review, return the requested analysis without writing a
deck or calling generation. Otherwise reuse the chosen mode:

| Request | Mode |
| --- | --- |
| Edit native text, cells, charts or connectors in PowerPoint | `editable` |
| Generate full-slide artwork or continue an existing image deck | `image` |
| A new deck with no output-mode preference | Explain the difference and resolve that choice before generation |

Record the chosen mode in the task's existing notes or `deck-mode.txt`. Do not
silently fall back from editable to image mode. Inspect an existing deck and
its inputs before changing it; missing `outline.md` alone does not mean it is new.

For a new deck, establish audience, source material, slide count and style.
Reuse approved choices and outline. Read the [outline contract](references/outline-format.md)
and [style guide](references/style-guide.md) as needed. Resolve material missing
choices, then author the outline and prompts/spec. A scoped revision does not
need a new full-deck outline or style-selection interview.

## Editable workflow

Read the [spec contract](references/editable-slide-spec.md) before authoring.

1. Author `slide-spec.json` with native text, shapes, lines, tables and charts.
   Use image assets only where the task needs them; diagrams do not require a
   preliminary image-model call. Preserve research facts and label example data.
   Include sources in speaker notes and the schema's required source fields.
2. Validate and build from any working directory:

   ```bash
   bun "$BUNDLE_DIR/scripts/build-deck.ts" --mode editable "$DECK_DIR"
   ```

3. Render the current spec through the bundled preview helper, which rebuilds
   the PPTX and associates spec, slides and preview files in a manifest:

   ```bash
   python3 "$BUNDLE_DIR/scripts/editable/render-previews.py" --spec "$DECK_DIR/slide-spec.json" --output-dir "$DECK_DIR/rendered"
   ```

   Preview rendering needs LibreOffice and Poppler. If unavailable, deliver the
   built PPTX with its visual inspection explicitly pending; do not invent previews.
4. Inspect every preview for text fit, cropping, object placement and content.
   Automated Critic review is optional when not requested and requires a configured
   PaperBanana Python backend plus authorization for its VLM calls:

   ```bash
   python3 "$BUNDLE_DIR/scripts/editable/review-editable.py" --spec "$DECK_DIR/slide-spec.json" --rendered-dir "$DECK_DIR/rendered" --output "$DECK_DIR/critic-review.json"
   ```

5. Preserve unresolved/unmapped findings. Edit the affected elements in the spec,
   rebuild and rerender before reviewing again. Never use old previews or a previous
   review as evidence for a changed deck. Do not patch the generated PPTX as the
   sole source of a fix while leaving the spec stale.

Invalid specs, missing assets and hash mismatches must fail without an image-mode
fallback. Native OOXML objects prove structure; rendered previews prove visible
layout; actual PowerPoint interaction is needed to claim that application was tested.

## Image workflow

1. Keep the approved style tokens across `prompts/NN-slide-slug.md`: palette,
   type hierarchy, background and recurring visual treatment. Keep required
   labels, quantities and connections explicit.
2. Use the configured PaperBanana backend and preserve explicit/saved provider
   and model choices. Check `slide --help` or `slide-batch --help` for supported
   flags. Credentials stay in the configured environment, outside prompts/logs.

   ```bash
   python -m paperbanana.cli slide-batch --prompts-dir "$DECK_DIR/prompts" --output-dir "$DECK_DIR"
   ```

3. For partial batches, preserve completed pages and resume only missing pages.
   For one-page edits, regenerate only that page with the existing style tokens.
   Do not assume `slide-batch --continue` is supported. If the backend cannot
   target a subset, stage the requested prompt(s) in a separate directory and
   reconcile only those outputs; don't overwrite unrelated slides.
4. Before assembly, compare the intended slide list with actual image filenames.
   Report missing, duplicate or orphaned pages. Do not silently delete files or
   merge a stale orphan; stage the intended images/prompts for assembly when needed.
5. Assemble and inspect the result:

   ```bash
   bun "$BUNDLE_DIR/scripts/build-deck.ts" --mode image "$DECK_DIR"
   ```

Critic failure does not require generating the image again. Preserve it as
`UNREVIEWED`. Do not switch to a direct Gemini script or another provider solely
because the selected route failed. Reuse approved alternatives when present;
otherwise report the limitation and resolve the missing choice.

## Delivery and recovery

Return the deck, inspected previews and the status of each requested output.
List missing pages and review gaps. A model score is not scientific acceptance.
Do not claim native editing when the deck contains full-slide images.

Retry recoverable failures within scope after diagnosing them. Respect the
approved call limits and provider choices; do not pursue an unbounded "until
clean" loop. Further revisions should address concrete findings. Preserve source
specs, prompts and existing user edits throughout.
