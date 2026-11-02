# Editable Slide Spec (v1 contract)

`--mode editable` builds a native PowerPoint deck from a single `slide-spec.json` in the deck directory. Every text box, table, chart, shape, and connector is emitted as a real OOXML object — nothing is rasterised. The pipeline is fail-closed: any schema violation, unknown type or theme, out-of-bounds box, duplicate ID, missing `[Sources]` block, missing asset, or asset hash mismatch throws **before** the output path is written. Editable mode never falls back to image mode.

## Coordinate system

Decks use `LAYOUT_WIDE`: a **13.333 × 7.5 inch** canvas (16:9). All `x`, `y`, `w`, `h` values are inches from the top-left corner. Every element must satisfy `x + w ≤ 13.333` and `y + h ≤ 7.5` (children of a `group` are validated against the group box instead — see below).

## Deck header

| Field | Allowed values | Notes |
|-------|----------------|-------|
| `schema_version` | `"1"` | Fixed for this contract |
| `deck.layout` | `"LAYOUT_WIDE"` | Only wide 16:9 is supported |
| `deck.language` | `"en"`, `"zh-CN"` | Deck language metadata |
| `deck.theme` | `"paperbanana-parchment"`, `"paperbanana-clean"` | Any other name throws |

### Themes

| Theme | Background | Ink | Muted | Rule | Accent | Accent 2 | Fonts |
|-------|------------|-----|-------|------|--------|----------|-------|
| `paperbanana-parchment` | `F7F2E6` | `25231F` | `6D6A64` | `C8C3B8` | `2A9D8F` | `4A6FD4` | Charter |
| `paperbanana-clean` | `FFFFFF` | `1F2937` | `64748B` | `CBD5E1` | `0F766E` | `4F46E5` | Aptos Display / Aptos |

## Slides

Each slide requires `id`, `title`, `speaker_notes`, `sources`, and `elements` (all non-empty). Slide and element IDs must match `^[a-z0-9][a-z0-9_-]*$` and be unique across the whole slide, including nested group children.

**`[Sources]` rule:** `speaker_notes` must contain a `[Sources]` block listing where every claim on the slide comes from (mirror the `sources` array). A spec without it fails validation.

## Element fields

Common required fields for every element: `id`, `type`, `x`, `y`, `w`, `h`.

| `type` | Required extras | Optional | Emitted as |
|--------|-----------------|----------|------------|
| `text` | `text`, `font_size` (≥ 16) | `color`, `align`, `valign`, `bold` | Native text box |
| `shape` | — | `shape` (PowerPoint geometry name, e.g. `roundRect`; default `rect`), `fill`, `stroke` | Native autoshape |
| `line` | — | `stroke`, `end_arrow` (`none`/`triangle`/`stealth`/`arrow`); `w` or `h` may be 0 for a straight connector | Native connector, inserted **before** node shapes |
| `table` | `rows` (non-empty array of string rows) | — | Native table |
| `chart` | `series` (non-empty; `{name, labels, values}`), `chart_type` (`bar`/`line`/`scatter`) | — | Native chart part (`ppt/charts/chartN.xml`) |
| `image` | `path`, `sha256` (64 hex), `alt_text` | — | Picture with pinned content hash |
| `group` | `children` (non-empty array of elements) | — | Layout-only container (see below) |

Colors (`color`, `fill`, `stroke`) are 6-digit uppercase hex without `#`.

### Groups

A `group` is a layout-only container: children use **group-relative coordinates** and are validated against the group box (`child.x + child.w ≤ group.w`, `child.y + child.h ≤ group.h`; violations report `outside group bounds`). At render time each child is offset into absolute slide coordinates and emitted as its own native object with its own stable `objectName` ID. PptxGenJS 4.0.1 exposes no native PowerPoint group API, so the container itself is neither emitted nor rasterised — children stay individually editable.

### Asset hash rule

Every `image` element pins its file with `sha256`. The `path` is resolved relative to the directory holding `slide-spec.json`. At build time the file must exist and its SHA-256 must match the pinned value, or the build throws before writing anything. This makes decks reproducible byte-for-byte on the asset side.

### SVG boundary

An SVG (or any vector file rendered to PNG) is only an **image asset**. Embedding one does not make its contents editable in PowerPoint and is not proof of semantic editability. Real editability means `text`, `table`, `chart`, `shape`, and `line` elements — those are the only kinds this renderer treats as editable, and they are never converted to images.

## Commands

```bash
cd plugins/paperbanana-slide-deck

# Validate only
bun scripts/editable/validate-slide-spec.ts <deck-dir>/slide-spec.json

# Build the native PPTX (fail-closed; never falls back to image mode)
bun scripts/build-deck.ts --mode editable <deck-dir> --output <deck-dir>/deck.pptx

# Rebuild and render matching previews (Bun + LibreOffice + Poppler)
python3 scripts/editable/render-previews.py \
  --spec <deck-dir>/slide-spec.json --output-dir <deck-dir>/rendered
# → rebuilt PPTX, per-page PNGs and render-manifest.json in rendered/

# Review previews with PaperBanana Critic (preview-only; never edits the PPTX)
python3 scripts/editable/review-editable.py \
  --spec <deck-dir>/slide-spec.json \
  --rendered-dir <deck-dir>/rendered \
  --output <deck-dir>/critic-review.json
# Add --dry-run to emit per-slide Critic context without importing PaperBanana
```

Render manifest **v2** binds the spec, PPTX, every preview page and every source
image, including images nested inside layout groups. Source-image paths resolve
relative to the spec and must match their declared `sha256`. Rendering checks
those images before and after the build; review checks them before provider
calls and again before recording completion. Changed or missing inputs produce
an `unreviewed` report. Regenerate old v1 manifests with `render-previews.py`;
they cannot establish source-image correspondence.

Rendering stages a complete generation and publishes it as a directory. A
publication failure restores the previous directory. If filesystem errors also
prevent restoration, the script reports a retained backup path for recovery.
The manifest records a local build association, not scientific correctness or
tamper-resistant attestation. Keep `critic-review.json` outside `rendered/` so
review cannot overwrite its inputs. The render directory must not contain the
spec or any source image. Report paths must not alias any input, including
source-image symbolic links or hard links; this protection also applies to
dry runs and error reports, even when the declared image hash is invalid.

The Python environment must provide the maintained PaperBanana backend and a
configured VLM provider. `--vlm-provider` and `--vlm-model` override that backend's
settings. Provider selection is separate from the image provider. The report
uses `reviewed`, `needs-revision` and `unreviewed`; a dry run is context preparation,
not a completed review. The adapter validates the original response before the
backend can normalize it: `critic_suggestions` is required; a score, when
present, must be a finite JSON number from 0 to 10. Strings, booleans, out-of-range
scores and empty unscored feedback are `unreviewed`, not approval.

Critic suggestions come back prefixed `slide-id/element-id: …` (unmatched ones as `slide-id/unmapped: …`). Apply findings by editing `slide-spec.json` and rebuilding — never by touching the PPTX or the preview PNGs.

## Full passing example

This is the repository test fixture (`tests/fixtures/editable/slide-spec.json`) and exercises every non-group element type:

```json
{
  "schema_version": "1",
  "deck": { "layout": "LAYOUT_WIDE", "language": "en", "theme": "paperbanana-parchment" },
  "slides": [{
    "id": "slide-01",
    "title": "Editable conclusion",
    "sources": ["local:examples/slide_deck_workflow.png"],
    "speaker_notes": "[Sources]\n- local:examples/slide_deck_workflow.png",
    "elements": [
      { "id": "title-text", "type": "text", "x": 0.7, "y": 0.6, "w": 5.0, "h": 0.6,
        "text": "Editable conclusion", "font_size": 24 },
      { "id": "status-shape", "type": "shape", "x": 0.7, "y": 1.55, "w": 2.2, "h": 0.7,
        "shape": "roundRect", "fill": "D8EFEA", "stroke": "2A9D8F" },
      { "id": "status-line", "type": "line", "x": 2.9, "y": 1.9, "w": 0.7, "h": 0.01,
        "stroke": "6D6A64", "end_arrow": "triangle" },
      { "id": "native-table", "type": "table", "x": 0.7, "y": 2.65, "w": 4.4, "h": 1.25,
        "rows": [["Native table", "Value"], ["TSTR", "0.6506"]] },
      { "id": "native-chart", "type": "chart", "x": 5.45, "y": 1.55, "w": 3.25, "h": 3.0,
        "chart_type": "bar", "series": [{ "name": "TSTR", "labels": ["A", "B", "C"],
        "values": [0.1749, 0.1514, 0.6506] }] },
      { "id": "asset-image", "type": "image", "x": 9.05, "y": 1.55, "w": 3.55, "h": 3.0,
        "path": "../../../../../examples/slide_deck_workflow.png",
        "sha256": "826d374136ae75b3b28f127c86fbde833ed78b5f9b4e90983458c1e956fc6eb6",
        "alt_text": "PaperBanana slide deck workflow" }
    ]
  }]
}
```

A grouped variant replaces `elements` with:

```json
[{ "id": "group", "type": "group", "x": 1, "y": 1, "w": 4, "h": 2,
   "children": [{ "id": "group-label", "type": "text", "x": 0.2, "y": 0.2, "w": 3, "h": 0.5,
     "text": "Grouped label", "font_size": 20 }] }]
```
