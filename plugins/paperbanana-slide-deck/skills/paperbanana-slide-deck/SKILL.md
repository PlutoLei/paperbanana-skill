---
name: paperbanana-slide-deck
description: End-to-end slide deck creation via PaperBanana + Nexus RDIV. Content analysis, interactive style selection, outline/prompt generation, image batch generation, PPTX/PDF merge. Use when user wants to create a full presentation/slide deck from content.
---

# PaperBanana Slide Deck

End-to-end slide deck creation orchestrated via Nexus RDIV workflow.

**Pipeline:** Content -> Style Selection -> Outline -> Prompts -> PaperBanana Image Gen -> PPTX/PDF Merge

## When to Use

- User wants to create a slide deck / presentation from content (paper, notes, topic)
- User says "make slides", "create a presentation", "PPT", "slide deck"
- User has content and wants it turned into visual slides

## Dependencies

| Component | Role | Location |
|-----------|------|----------|
| PaperBanana CLI | Image generation | `python -m paperbanana.cli slide-batch` |
| Baoyu slide-deck assets | Style files + merge scripts | `~/.claude/plugins/cache/baoyu-skills/content-skills/*/skills/baoyu-slide-deck/` |
| Bun | Run merge scripts | `bun` or `npx -y bun` |

## Nexus Integration

This skill runs as a Nexus RDIV task. Initialize via:

```
Route: IMPLEMENTATION
Complexity: MEDIUM
Workflow: RDIV
```

## RDIV Workflow

### Phase R: Research — Content Analysis & Style Selection

**Step R1: Discover baoyu assets**

```bash
# Find latest baoyu-slide-deck cache
BAOYU_DIR=$(ls -td ~/.claude/plugins/cache/baoyu-skills/content-skills/*/skills/baoyu-slide-deck 2>/dev/null | head -1)
```

If found: Glob `${BAOYU_DIR}/references/styles/*.md` to get full style list.
If not found: Use PaperBanana's 23 built-in presets (fallback).

**Step R2: Analyze content**

Read user's input content. Analyze for:
- Topic/discipline (biology, ML, business, etc.)
- Audience (academic, executive, general)
- Tone (formal, educational, energetic)
- Content length -> recommended slide count:

| Content Length | Recommended Slides |
|---------------|-------------------|
| < 1000 words | 5-10 |
| 1000-3000 words | 10-18 |
| 3000-5000 words | 15-25 |
| > 5000 words | 20-30 |

**Step R3: Style recommendation**

Based on content signals, recommend 2-3 styles from the 23 presets:

| Content Signals | Recommended Style |
|----------------|-------------------|
| biology, chemistry, medical | `scientific` |
| machine learning, AI, deep learning | `ml-ai` |
| biotech, genomics, drug discovery | `biotech` |
| neuroscience, brain, cognitive | `neuroscience` |
| ecology, climate, sustainability | `environmental` |
| architecture, system design | `blueprint` |
| business, investor, corporate | `corporate` |
| product launch, keynote | `bold-editorial` |
| Apple/Tesla premium | `tech-keynote` |
| finance, investment, consulting | `financial-elite` |
| tutorial, education, beginner | `sketch-notes` |
| classroom, teaching | `chalkboard` |
| academic research, briefing | `intuition-machine` |
| SaaS, product, dashboard | `notion` |
| executive, minimal | `minimal` |
| entertainment, gaming | `dark-atmospheric` |
| innovation, design showcase | `creative-bold` |
| creative, children | `vector-illustration` |
| historical, heritage | `vintage` |
| lifestyle, wellness, artistic | `watercolor` |
| science communication | `editorial-infographic` |
| storytelling, magical | `fantasy-animation` |
| gaming, retro, developer | `pixel-art` |

**Step R4: Interactive selection**

Use AskUserQuestion for each decision:

**Q1: Style**
```
header: "Style"
question: "Which visual style for this deck?"
options:
  - label: "{recommended} (Recommended)"
    description: "Best match based on content analysis"
  - label: "{alternative_1}"
    description: "[description]"
  - label: "{alternative_2}"
    description: "[description]"
```

**Q2: Audience**
```
header: "Audience"
question: "Who is the primary reader?"
options:
  - label: "General readers"
  - label: "Beginners/learners"
  - label: "Experts/professionals"
  - label: "Executives"
```

**Q3: Slide Count**
```
header: "Slides"
question: "How many slides?"
options:
  - label: "{N} slides (Recommended)"
  - label: "Fewer ({N-3} slides)"
  - label: "More ({N+3} slides)"
```

**Step R5: Save analysis**

Create output directory and save `analysis.md`:
```
slide-deck/{topic-slug}/analysis.md
```

### Phase D: Design — Outline & Prompts

**Step D1: Load style spec**

If baoyu available: `Read ${BAOYU_DIR}/references/styles/{style_name}.md`
If fallback: Use `paperbanana.guidelines.slide_styles.get_style_prompt(style_name)`

**Step D2: Generate outline**

Create `outline.md` with structure:

```markdown
# {Deck Title}

Style: {style_name}
Slides: {N}
Audience: {audience}

## Slide 1: Cover
- Layout: title-hero
- Title: {deck title}
- Subtitle: {subtitle}

## Slide 2: {title}
- Layout: {layout_type}
- Key points:
  - Point 1
  - Point 2

...

## Slide N: Back Cover
- Layout: title-hero
- Content: Key takeaway or CTA
```

Available layouts (from PaperBanana):
- `title-hero`, `quote-callout`, `key-stat`, `split-screen`
- `icon-grid`, `two-columns`, `three-columns`, `image-caption`, `bullet-list`
- `linear-progression`, `binary-comparison`, `comparison-matrix`
- `hierarchical-layers`, `hub-spoke`, `bento-grid`, `funnel`
- `dashboard`, `venn-diagram`, `circular-flow`, `winding-roadmap`

**Step D3: Optional outline review**

Ask user if they want to review the outline before proceeding.

**Step D4: Generate prompts**

For each slide, create `prompts/NN-slide-{slug}.md`:

```markdown
{style_instructions from Step D1}

---

Generate a presentation slide image with the following content:

**Slide Title:** {title}
**Layout:** {layout_type}
**Content:**
{content points}

**Design Requirements:**
- Resolution: 16:9 aspect ratio (1920x1080 or 3840x2160)
- No slide numbers, page numbers, footers, headers, or logos
- All text must be clear, readable, and correctly spelled
- One clear focal point per slide
```

### Phase I: Implement — Generate & Merge

**Step I1: Batch generate images**

```bash
cd <paperbanana_dir>
python -m paperbanana.cli slide-batch \
  --prompts-dir "slide-deck/{topic-slug}/prompts" \
  --output-dir "slide-deck/{topic-slug}" \
  --style {style_name} \
  --resolution 4k \
  --config configs/fast.yaml \
  --iterations 2 --auto
```

**Step I2: Merge to PPTX**

```bash
BAOYU_DIR=$(ls -td ~/.claude/plugins/cache/baoyu-skills/content-skills/*/skills/baoyu-slide-deck 2>/dev/null | head -1)
bun "${BAOYU_DIR}/scripts/merge-to-pptx.ts" "slide-deck/{topic-slug}"
```

**Step I3: Merge to PDF**

```bash
bun "${BAOYU_DIR}/scripts/merge-to-pdf.ts" "slide-deck/{topic-slug}"
```

If baoyu merge scripts unavailable: inform user that PNG images are ready but PPTX/PDF merge requires baoyu-slide-deck plugin.

### Phase V: Verify — Review & Iterate

**Step V1: Display results**

Read and display each generated slide image. Report:
- Total slides generated
- Style used
- Output directory
- PPTX/PDF file paths

**Step V2: User feedback**

Ask user:
```
header: "Review"
question: "How do the slides look?"
options:
  - label: "Looks great, done!"
  - label: "Regenerate specific slides"
    description: "I'll tell you which ones to redo"
  - label: "Change style and redo all"
    description: "Start over with a different style"
```

**Step V3: Selective regeneration**

If user wants to modify specific slides:
1. User identifies slide numbers
2. User provides feedback for each
3. Update the prompt file: `prompts/NN-slide-{slug}.md`
4. Regenerate: `python -m paperbanana.cli slide --input prompts/NN-slide-{slug}.md --style {style_name} --resolution 4k --config configs/fast.yaml --auto`
5. Re-merge PPTX/PDF

## Output Structure

```
slide-deck/{topic-slug}/
  source.md              <- Original content
  analysis.md            <- R phase output
  outline.md             <- D phase output
  prompts/               <- D phase output
    01-slide-cover.md
    02-slide-xxx.md
    ...
  01-slide-cover.png     <- I phase output
  02-slide-xxx.png
  {topic-slug}.pptx      <- I phase output
  {topic-slug}.pdf       <- I phase output
```

## Fallback Behavior

| Component Missing | Fallback |
|-------------------|----------|
| Baoyu styles | Use `slide_styles.py` 23 built-in presets |
| Baoyu merge scripts | Output PNG only, skip PPTX/PDF |
| Bun/npx | Skip PPTX/PDF merge, inform user |

## Quick Reference

```bash
# List available styles
python -m paperbanana.cli slide --list-styles

# Generate single slide with style
python -m paperbanana.cli slide --input prompt.md --style scientific

# Batch generate with style
python -m paperbanana.cli slide-batch --prompts-dir prompts/ --style blueprint --resolution 4k
```
