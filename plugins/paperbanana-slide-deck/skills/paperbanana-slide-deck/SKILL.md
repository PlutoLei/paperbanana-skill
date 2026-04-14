---
name: paperbanana-slide-deck
description: Use when user wants to create a full slide deck or presentation using PaperBanana image generation, OR modify/regenerate an existing PaperBanana slide deck. Triggers on "make slides", "create presentation", "PPT", "slide deck", "regenerate slides", "update slides", "paperbanana slides". Also triggers when user has an existing slide-deck directory with outline.md and wants to regenerate images or make changes. This is the PRIMARY slide deck skill — always prefer over baoyu-slide-deck.
---

# PaperBanana Slide Deck

End-to-end slide deck creation and modification. Supports two modes: creating new decks from scratch, and regenerating existing decks after prompt edits.

**Pipeline:** Content → Style Selection → Outline → Prompts → Image Generation → PPTX Merge

## Mode Detection

On invocation, determine the mode by checking the target directory:

| Condition | Mode | Start Phase |
|-----------|------|-------------|
| Target dir missing OR no `outline.md` | **New** | Phase R (full RDIV) |
| Target dir has `outline.md` + `prompts/` | **Modify** | Phase I (generate + merge) |

In Modify mode, the user has already edited prompts or outline externally. Skip directly to Phase I.

## Dependencies

| Component | Role | Location |
|-----------|------|----------|
| `google-genai` SDK | Path B image generation | `pip install google-genai` |
| PaperBanana CLI | Path A image generation | `python -m paperbanana.cli slide-batch` |
| merge-to-pptx.ts | PPTX merge | `skills/paperbanana-slide-deck/scripts/merge-to-pptx.ts` (local) |
| Style libraries | Style presets (4 sources, 150+) | See R1 for discovery paths |
| Bun | Run merge script | `bun` |

## Phase R: Research (New Mode Only)

Skip this phase entirely in Modify mode.

**R1: Discover style libraries** — Scan all four sources and merge into a unified list.

```bash
# Source 0 (PRIMARY): Local extended library (123 styles from Fooocus/ComfyUI, structured)
LOCAL_STYLES="$(find ~/.claude/skills .claude/skills -maxdepth 1 -name 'paperbanana-slide-deck' -type d 2>/dev/null | head -1)/references/styles"

# Source 1: baoyu-slide-deck styles (16 slide-optimized)
BAOYU_SLIDE=$(ls -td ~/.claude/plugins/cache/baoyu-skills/content-skills/*/skills/baoyu-slide-deck/references/styles 2>/dev/null | head -1)

# Source 2: baoyu-infographic styles (20 visual-rich)
BAOYU_INFOG=$(ls -td ~/.claude/plugins/cache/baoyu-skills/content-skills/*/skills/baoyu-infographic/references/styles 2>/dev/null | head -1)

# Source 3: theme-factory themes (10 color/typography presets)
THEME_FACTORY=$(ls -td ~/.claude/plugins/cache/anthropic-agent-skills/document-skills/*/skills/theme-factory/themes 2>/dev/null | head -1)
```

Merge: Glob all four directories for `*.md`, deduplicate by filename (priority: baoyu-slide-deck > local > baoyu-infographic > theme-factory). Present the full unified list to user during R3.

If none found: Use PaperBanana's 23 built-in presets.

**R2: Analyze content** — Topic, audience, tone, recommended slide count.

**R3: Style recommendation** — Recommend 2-3 styles based on content signals. See `references/style-guide.md` for the full style-to-content mapping table.

**R4: Interactive selection** — Use AskUserQuestion for style, audience, and slide count.

**R5: Save analysis** — Create `slide-deck/{topic-slug}/analysis.md`.

## Phase D: Design (New Mode Only)

In Modify mode, the user handles prompt edits directly.

**D1: Load style spec** — Read from baoyu styles or PaperBanana built-ins.

**D2: Generate outline** — Create `outline.md` with slide structure. See `references/outline-format.md`.

**D3: Optional outline review** — Ask user if they want to review before proceeding.

**D4: Generate prompts** — For each slide, create `prompts/NN-slide-{slug}.md`. Each prompt file has the style instructions block, then `---`, then the slide-specific content and design requirements.

## Phase I: Implement (Both Modes)

### Step I1: Image Generation (Dual Path)

**Path A — PaperBanana CLI (preferred, has critic quality review):**

```bash
cd <project_root>
python -m paperbanana.cli slide-batch \
  --prompts-dir "slide-deck/{topic-slug}/prompts" \
  --output-dir "slide-deck/{topic-slug}" \
  --resolution 4k \
  --iterations 2
```

**Auto-degrade trigger:** Switch to Path B if **any** slide (not just the first) hits one of these. Don't keep retrying Path A:
- `RetryError` / `ResourceExhausted` / HTTP 429 (rate-limited)
- `ServerError` (5xx) or non-429 `ClientError` (4xx)
- Critic takes longer than 3 minutes on any single slide
- User reports "一直 429" / persistent rate limits → degrade immediately, skip further Path A retries

**Distinguish two 429 sources**:

| Source | Symptom | Response |
|--------|---------|----------|
| Critic 429 (VLM rate limit) | Error inside critic loop, Path A specific | Auto-degrade to Path B (no critic → bypasses the issue) |
| Image-gen 429 (`gemini-3-pro-image-preview`) | Same error in Path B | Exponential backoff: `time.sleep(30 * 2**retry)` up to 5 min, then surface to user |

**Partial-batch recovery**: If some slides were already generated before 429 hit, preserve existing PNGs and resume from the next missing slide (cross-reference `prompts/*.md` with existing `NN-slide-*.png`).

> **Note (upstream sync pending):** Upstream `paperbanana` CLI (≥ #129) has native `batch_checkpoint.json` for Path A `slide-batch` — resume is automatic there. The skip logic above is for the Path B fallback code, which doesn't yet use the upstream checkpoint format.

**Path B — Direct Gemini API (fallback, no critic, stable):**

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64, os, time

# Read API key from paperbanana/.env
client = genai.Client(api_key=GOOGLE_API_KEY)

config = types.GenerateContentConfig(
    response_modalities=['IMAGE'],
    image_config=types.ImageConfig(
        aspect_ratio='16:9',
        image_size='4K',
    ),
)

MAX_RETRIES = 5   # after which surface to user
BASE_SLEEP = 30   # seconds

for prompt_file in sorted(os.listdir(prompts_dir)):
    name = prompt_file.replace('.md', '')
    out_path = os.path.join(output_dir, f'{name}.png')

    # Partial-batch resume: skip slides already generated
    if os.path.exists(out_path):
        continue

    with open(os.path.join(prompts_dir, prompt_file), 'r', encoding='utf-8') as f:
        prompt_text = f.read()

    # Exponential backoff on 429 / transient errors
    for retry in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model='gemini-3-pro-image-preview',
                contents=prompt_text,
                config=config,
            )
            break
        except Exception as e:
            msg = str(e).lower()
            if '429' in msg or 'resource' in msg or 'rate' in msg:
                wait = min(BASE_SLEEP * (2 ** retry), 300)  # cap at 5 min
                time.sleep(wait)
                continue
            raise  # non-429 error → surface immediately
    else:
        raise RuntimeError(f'{name}: 429 after {MAX_RETRIES} retries, surface to user')

    for part in response.candidates[0].content.parts:
        inline = getattr(part, 'inline_data', None)
        if inline and getattr(inline, 'data', None):
            data = inline.data
            img_bytes = base64.b64decode(data) if isinstance(data, str) else data
            img = Image.open(BytesIO(img_bytes))
            img.save(out_path, 'PNG')
            break

    time.sleep(BASE_SLEEP)  # baseline cooldown between slides
```

The API key is in `<project_root>/paperbanana/.env` as `GOOGLE_API_KEY`. Read it with dotenv or manually.

### Step I2: Smart Cleanup (Pre-Merge)

**Run AFTER I1 generation, not before.** I1 is partial-batch-aware and skips already-generated slides; Cleanup's job is only to remove PNGs whose prompt was deleted/renamed since the last run. Running Cleanup before I1 would delete valid WIP slides from a resumed batch.

Sequencing: `I1 (generate + resume) → I2 (cleanup orphans) → I3 (merge)`.

1. Scan `prompts/*.md` → build expected PNG set (e.g. `01-slide-hook.md` → `01-slide-hook.png`)
2. Scan target directory for `*.png` files matching pattern `NN-slide-*.png`
3. Delete slide PNGs NOT in expected set (orphans from renamed/deleted prompts)
4. Preserve non-slide PNGs (e.g. `logo.png`, `background.png`) and all expected-set PNGs

### Step I3: Merge to PPTX

```bash
# Locate skill directory dynamically (works on any platform)
SKILL_DIR="$(find ~/.claude/skills .claude/skills -maxdepth 1 -name 'paperbanana-slide-deck' -type d 2>/dev/null | head -1)"
bun "${SKILL_DIR}/scripts/merge-to-pptx.ts" "slide-deck/{topic-slug}"
```

If merge script unavailable: inform user that PNG images are ready but PPTX merge requires bun and the local merge-to-pptx.ts script.

## Phase V: Verify (Both Modes)

**V1: Display results** — Read and display each generated slide image. Report total slides, output directory, PPTX file path.

**V2: User feedback** — Ask:
- "Looks great, done!"
- "Regenerate — I'll tell you what to fix in the prompts"

**V3: Regeneration** — If user wants changes:
1. User edits the specific prompt files
2. Regenerate ALL slides (not just changed ones — ensures visual consistency)
3. Smart cleanup + re-merge PPTX
4. Return to V1

## Fallback Behavior

| Situation | Fallback |
|-----------|----------|
| All style libraries missing | Use PaperBanana built-in presets |
| Local merge script missing | Output PNG only, skip PPTX |
| Bun/npx missing | Skip PPTX merge, inform user |
| **Critic 429 / RetryError** | **Auto-degrade to Path B (no critic)** |
| **Image-gen 429 in Path B** | **Exponential backoff up to 5 min, then surface** |
| **Partial batch already generated** | **Resume from next missing slide, preserve existing PNGs** |

## Output Structure

```
slide-deck/{topic-slug}/
  analysis.md            ← R phase (New mode only)
  outline.md             ← D phase
  prompts/               ← D phase
    01-slide-hook.md
    02-slide-cover.md
    ...
  01-slide-hook.png      ← I phase
  02-slide-cover.png
  ...
  {topic-slug}.pptx      ← I phase
```

## Quick Reference

```bash
# Path A: PaperBanana CLI batch
python -m paperbanana.cli slide-batch --prompts-dir prompts/ --resolution 4k --iterations 2

# Path A: single slide (supports --vlm-model)
python -m paperbanana.cli slide --input prompt.md --resolution 4k

# List available styles
python -m paperbanana.cli slide --list-styles
```
