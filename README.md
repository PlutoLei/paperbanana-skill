# PaperBanana Skills

<p align="center">
  <a href="https://github.com/PlutoLei/paperbanana-skill/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/PlutoLei/paperbanana-skill?style=flat-square&color=yellow" /></a>
  <img alt="Version" src="https://img.shields.io/badge/version-4.5.0-blue?style=flat-square" />
  <img alt="Agent Skills" src="https://img.shields.io/badge/Agent%20Skills-Standard-2B6CB0?style=flat-square" />
  <img alt="Multi-Runtime" src="https://img.shields.io/badge/Runtime-Multi-success?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="Providers" src="https://img.shields.io/badge/Providers-8-green?style=flat-square" />
  <img alt="GPT Image 2" src="https://img.shields.io/badge/GPT%20Image%202-native-blueviolet?style=flat-square" />
  <img alt="Eval" src="https://img.shields.io/badge/Eval-6--item%20Checklist-orange?style=flat-square" />
  <a href="https://github.com/PlutoLei/paperbanana-skill/blob/master/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-black?style=flat-square" /></a>
</p>

<p align="center">
  <strong>One sentence in, publication-quality academic figure out.</strong><br/>
  Powered by a 5-agent pipeline that plans, styles, generates, and self-critiques your illustrations.
</p>

<p align="center">
  <strong>English</strong> | <a href="README_CN.md">中文</a>
</p>

---

## Gallery

<table>
<tr>
<td align="center"><strong>Biology — Signal Pathway</strong><br/><img src="examples/bio_signaling_pathway.png" width="400"/></td>
<td align="center"><strong>NLP — RAG Pipeline</strong><br/><img src="examples/nlp_rag_pipeline.png" width="400"/></td>
</tr>
<tr>
<td align="center"><strong>Data Engineering — Lakehouse</strong><br/><img src="examples/data_lakehouse.png" width="400"/></td>
<td align="center"><strong>Medical AI — U-Net + Mamba</strong><br/><img src="examples/unet_mamba_segmentation.png" width="400"/></td>
</tr>
<tr>
<td align="center"><strong>Medical Imaging — TextMamba3D</strong><br/><img src="examples/textmamba3d_architecture.png" width="400"/><br/><sub><em>gpt-image-2 · paper-grade info density</em></sub></td>
<td align="center"><strong>Game Theory — Influence Diagram</strong><br/><img src="examples/game_theory_influence_diagram.png" width="400"/><br/><sub><em>Gemini · soft pastel academic aesthetic</em></sub></td>
</tr>
<tr>
<td align="center"><strong>Ablation Study — BraTS 2023</strong><br/><img src="examples/ablation_brats_figure.png" width="400"/><br/><sub><em>gpt-image-2 · 2×2 MRI panels + Dice bar chart</em></sub></td>
<td align="center"><strong>Scientific Slide — scRNA-seq Workflow</strong><br/><img src="examples/slide_scrna_workflow.png" width="400"/><br/><sub><em>paperbanana-slide-deck · single-cell analysis pipeline</em></sub></td>
</tr>
</table>

<p align="center"><em>All figures generated from plain text descriptions — zero manual drawing.</em></p>

### Slide Deck Showcase — "The Flywheel Learning Method"

A real 10-slide lecture deck built with `paperbanana-slide-deck`. Below: 4 selected slides showing **set-wide style consistency** (same warm off-white palette, sketch-notes hand-drawn typography, and gear motif across the whole deck).

<table>
<tr>
<td align="center"><strong>Slide 1 — Cover</strong><br/><img src="examples/slide_flywheel_01_cover.png" width="380"/></td>
<td align="center"><strong>Slide 4 — Flywheel Model</strong><br/><img src="examples/slide_flywheel_04_model.png" width="380"/></td>
</tr>
<tr>
<td align="center"><strong>Slide 7 — AI Tools Do's and Don'ts</strong><br/><img src="examples/slide_flywheel_07_ai_tools.png" width="380"/></td>
<td align="center"><strong>Slide 10 — Let the Flywheel Spin</strong><br/><img src="examples/slide_flywheel_10_summary.png" width="380"/></td>
</tr>
</table>

<p align="center"><em>One command: <code>paperbanana-slide-deck</code> picks a style preset, plans the outline, drafts per-slide prompts, then generates all slides with consistent design tokens.</em></p>

<p align="center"><sub>The same pipeline now routes across <strong>8 providers</strong> — render this deck on <code>gpt-image-2</code> (clean Chinese titles), <code>gemini</code> (fast &amp; cheap), or any of <strong>100+ LiteLLM backends</strong> / local <code>ollama</code> models, with no workflow change.</sub></p>

<details>
<summary><strong>More Examples</strong> (architecture diagrams, traditional aesthetics)</summary>
<br/>
<table>
<tr>
<td align="center"><strong>Transformer Architecture</strong><br/><img src="examples/transformer_architecture.png" width="380"/></td>
<td align="center"><strong>Mamba SSM Architecture</strong><br/><img src="examples/mamba_architecture.png" width="380"/></td>
</tr>
<tr>
<td align="center" colspan="2"><strong>RAG Pipeline</strong><br/><img src="examples/rag_pipeline.png" width="760"/></td>
</tr>
<tr>
<td align="center" colspan="2"><strong>Chinese Calligraphy — 自律 (Self-Discipline)</strong><br/><img src="examples/chinese_calligraphy.png" width="560"/><br/><sub><em>Gemini · bold expressive brushwork + 飞白 on xuan paper</em></sub></td>
</tr>
</table>
</details>

---

## Skills in this Marketplace

| Skill | Scope | Description | Version |
|-------|-------|-------------|---------|
| **paperbanana** | user | Academic diagrams, plots, slides, and quality evaluation | v4.4.0 |
| **paperbanana-slide-deck** | project | Full slide deck orchestration (RDIV workflow) + 150+ style presets + editable PPTX mode | v1.3.0 |

## Feature Matrix

| Capability | Status | Details |
|------------|--------|---------|
| **Editable PPTX mode** | ✅ **v4.5 New** | `build-deck.ts --mode editable` renders native PowerPoint text/table/chart/shape/line objects from `slide-spec.json` — fail-closed, never silently falls back to images |
| **GPT Image 2 native support** | ✅ **v4.3 New** | `gpt-image-2` (2026-04-21) with true 16:9 up to 2048×1152, quality tier (low/medium/high), full RDIV pipeline + Critic |
| **Smart provider routing** | ✅ **v4.3 New** | Auto-pick `openai` vs `gemini` by scenario; explicit `用 GPT`/`用 Gemini`/`两路并行` override always respected |
| Methodology diagrams | ✅ | Text → publication-quality figure in 30s |
| Statistical plots | ✅ | CSV/JSON data → auto-styled academic plot |
| Presentation slides | ✅ | Markdown → 4K slide with 150+ style presets |
| Multi-venue styles | ✅ **New** | `--venue neurips\|icml\|acl\|ieee\|custom` |
| PDF input | ✅ **New** | `--input paper.pdf --pages 3-5` |
| 6-item quality eval | ✅ **New** | Binary checklist: completeness, layout, annotation, color, legibility, hallucination |
| Autoresearch loop | ✅ **New** | Automated prompt self-optimization with keep/revert |
| Error handling | ✅ **New** | Critic UNREVIEWED status, provider fallback chains, retry filtering |
| 8 VLM providers | ✅ | Gemini, Claude, OpenAI, Bedrock, OpenRouter + **LiteLLM** (100+ backends), **Ollama** (local models), **claude_code** (via `claude` CLI) |
| Auto-refine | ✅ | `--auto` loops until Critic is satisfied |
| Run continuation | ✅ | `--continue` with `--feedback` for iterative refinement |
| Dynamic aspect ratio | ✅ | 8 Imagen ratios, Planner auto-recommends |

---

## What's New in v4.5 — Editable PPTX Mode

`paperbanana-slide-deck` v1.3.0 adds an explicit, fail-closed **editable** deck mode alongside the existing image mode. Instead of merging full-slide PNGs, editable mode reads a `slide-spec.json` contract and emits **native PowerPoint objects** — every text box, table, chart, shape, and connector stays editable in PowerPoint.

```bash
cd plugins/paperbanana-slide-deck

# Image mode — the existing PNG-merge workflow, unchanged
bun scripts/build-deck.ts --mode image slide-deck/my-deck

# Editable mode — native objects from slide-deck/my-deck/slide-spec.json
bun scripts/build-deck.ts --mode editable slide-deck/my-deck
```

- **Native element types:** `text`, `shape`, `line`, `table`, `chart`, `image`, `group` (layout-only container; children stay individually editable). None of them is ever converted to an image.
- **Fail-closed contract:** unknown types or themes, out-of-bounds boxes, duplicate IDs, missing `[Sources]` notes, missing assets, or asset SHA-256 mismatches abort the build before any file is written. `--mode` is required; editable **never** silently falls back to image mode.
- **Critic on previews:** `scripts/editable/review-editable.py` renders-then-reviews the final PPTX pages with PaperBanana's Critic and maps every suggestion back to `slide-id/element-id`; fixes are applied by editing `slide-spec.json` and rebuilding — the PPTX itself is never patched.
- **Compatibility:** the legacy image merger (`merge-to-pptx.ts`) keeps its public boundary byte-for-byte — same CLI, same filename pattern, same output naming, same prompt-notes behavior.
- **Editable vs SVG:** embedding an SVG (or any vector render) is still just an image asset — it is *not* proof of semantic editability. Only native `text`/`table`/`chart`/`shape`/`line` objects count as editable.

Authoring contract, coordinate system (13.333×7.5 in), themes, and a full working example: [`plugins/paperbanana-slide-deck/references/editable-slide-spec.md`](plugins/paperbanana-slide-deck/references/editable-slide-spec.md).

---

## What's New in v4.4 — Wave-Parallel Slide Batches

`slide-batch` now generates slides **concurrently**: each slide gets its own pipeline instance (isolated run directory, isolated Critic loop), with a 5s start-up stagger, in-batch delayed retry for transient 503s, and an end-of-batch serial retry pass for stragglers.

**Measured:** 6 slides at `--concurrent 3` in **309s** vs a 768s serial estimate — **0.40x wall-clock (~2.5x speedup)**, zero dropped slides, identical per-slide quality gating.

Also in 4.4:

- **Smarter delivery** — the final image per slide is the **highest-critic-score** iteration rather than simply the last one; `critic_score_threshold=9.0` skips provably-done rounds early (calibrated on 69 historical runs with zero false early-stops).
- **Auto-routing decision table** and the `X_imagen` provider-naming warning are now part of SKILL.md.

> The runtime features (`--concurrent`, argmax delivery, threshold early-stop, slide generation itself) live in the maintained fork **[PlutoLei/paperbanana](https://github.com/PlutoLei/paperbanana)** — see Quick Start. On upstream builds, `slide-batch` runs serially.

---

## What's New in v4.3 — GPT Image 2 First-Class Support

OpenAI released `gpt-image-2` on **2026-04-21**. PaperBanana v4.3 integrates it natively so the full **Retriever → Planner → Stylist → Visualizer → Critic** pipeline runs on gpt-image-2 outputs. You get quality-gated images at up to 2048×1152 without leaving paperbanana.

### Adapter upgrade

| Feature | Before (v4.2) | After (v4.3) |
|---------|---------------|--------------|
| Default OpenAI model | `gpt-image-1.5` | `gpt-image-1.5` — but `gpt-image-2` is now fully wired in too |
| Output sizes | 1024×1024 / 1536×1024 / 1024×1536 (3 sizes) | **Adds** 2048×1152 (true 16:9), 1536×1536, 1792×1024, 1152×2048 |
| `quality=low\|medium\|high` | ❌ rejected | ✅ auto-sent for gpt-image-2 |
| Supported ratios | 3 (`1:1`, `3:2`, `2:3`) | **8** (all paperbanana ratios; no more downgrade) |
| Critic loop | Only on Gemini | ✅ Runs on gpt-image-2 too — catches Chinese typo bugs, missing nodes |

Switching is a two-flag change:

```bash
python -m paperbanana.cli generate \
  --image-provider openai_imagen --image-model gpt-image-2 \
  --aspect-ratio 16:9 \
  --input prompt.txt --caption "..."
```

### Auto routing by scenario

The skill picks the right provider based on your request's signal:

| Scenario | Auto-routes to | Why |
|----------|----------------|-----|
| User says `用 GPT` / `用 Gemini` / `两路并行` | That provider (or both) | Explicit intent always wins |
| `--purpose submission` / "投稿用" | `gpt-image-2` high | Rigor priority |
| Slide deck with **Chinese titles** | `gpt-image-2` | Avoid Gemini's duplicate-character bug (see below) |
| Edit with ≥ 2 reference images | `gpt-image-2` | Avoid Gemini's multi-image hallucination |
| Prompt mentions 山水 / 书法 / 古风 / 水墨 | `gemini` | Gemini dominates traditional East-Asian aesthetics |
| `generate` with architecture / multi-stage / ablation keywords | `gpt-image-2` high | GPT wins on dense multi-module figures |
| Everything else | `gemini` medium (default) | Faster, cheaper, prettier for general work |

Routing is calibrated from a 16-prompt controlled comparison (details: `docs/superpowers/specs/2026-04-23-image-router-design.md` in the companion repo).

### Before / After — routing in action

These pairs come from the same prompt sent to both providers. The routing table exists because each model has specific strengths and specific bugs.

#### 1. Chinese slide titles — GPT wins (Gemini has a duplicate-character bug)

<table>
<tr>
<td align="center" width="50%"><strong>Gemini</strong><br/><img src="examples/routing-comparison/D2_gemini.png" width="440"/><br/><em>Title reads "飞轮模飞轮模型" — the prefix "飞轮模" is duplicated. Not viable for slide decks.</em></td>
<td align="center" width="50%"><strong>gpt-image-2</strong><br/><img src="examples/routing-comparison/D2_openai.png" width="440"/><br/><em>Title renders cleanly: "飞轮模型 — 核心概念". Routing sends Chinese slides here.</em></td>
</tr>
</table>

#### 2. Semantic correctness (diffusion process) — GPT wins

<table>
<tr>
<td align="center" width="50%"><strong>Gemini</strong><br/><img src="examples/routing-comparison/A2_gemini.png" width="440"/><br/><em>Cat images at x_0 through x_4 look identical; only x_T is noise. Semantics and visuals don't match.</em></td>
<td align="center" width="50%"><strong>gpt-image-2</strong><br/><img src="examples/routing-comparison/A2_openai.png" width="440"/><br/><em>Cat actually degrades step-by-step — visually faithful to the diffusion process.</em></td>
</tr>
</table>

#### 3. Traditional Chinese calligraphy — Gemini wins (bolder brushwork)

<table>
<tr>
<td align="center" width="50%"><strong>Gemini</strong><br/><img src="examples/routing-comparison/G2_gemini.png" width="440"/><br/><em>Bold expressive strokes with visible 飞白 and xuan-paper fiber — the prompt asked for "bold" and got it.</em></td>
<td align="center" width="50%"><strong>gpt-image-2</strong><br/><img src="examples/routing-comparison/G2_openai.png" width="440"/><br/><em>Technically correct characters but the stroke feels restrained. The routing sends 书法/山水/古风 prompts to Gemini.</em></td>
</tr>
</table>

### Verdict

You don't need to know any of this — just ask for a figure and paperbanana picks. Or override with `--image-provider openai_imagen|google_imagen` (note the `_imagen` suffix — bare `openai`/`gemini` are rejected; asking the skill for "both" runs the two providers side by side). The Critic loop runs on whatever the pipeline picks, so quality stays gated regardless.

---

## What's New in v4.0

### Eval-First Quality System

A 6-item binary checklist evaluator that measures academic figure quality without human reference images:

| Check | Question | Pass Criteria |
|-------|----------|--------------|
| Completeness | All input concepts represented? | Every key concept has a visual element |
| Layout | Logical flow direction? | Clear L→R, T→B, or radial flow |
| Annotation | All components labeled? | Every visual element has text |
| Color Restraint | ≤3 primary colors? | Academic palette discipline |
| Legibility | Readable at 50% zoom? | Text survives PDF column layout |
| No Hallucination | Zero unlabeled concepts? | Nothing invented beyond input |

**Baseline: 76% → 100%** after prompt optimization. Color restraint was the bottleneck (33% → 100%).

### Autoresearch Self-Optimization

Automated prompt mutation loop inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch):

```
Mutate prompt → Generate figures → Evaluate checklist → Keep or Revert → Repeat
```

- One mutation per round (isolation principle)
- Targets weakest checklist dimension automatically
- Versioned prompt snapshots + JSONL changelog
- Stop condition: 3 consecutive rounds at 90%+ or 20 rounds max

### Multi-Venue Academic Styles

```bash
/paperbanana generate method.txt "Architecture overview" --venue neurips
```

Built-in style guides for NeurIPS, ICML, ACL, IEEE — each with venue-specific color palettes, layout conventions, and typography.

### Robust Error Handling

| Failure Type | Behavior |
|-------------|----------|
| Image API failure | Retry 3× → fallback provider chain → report |
| Critic JSON parse failure | **Never silently approve** — mark UNREVIEWED, retry once |
| Rate limit (429) | Exponential backoff, skip non-transient errors |
| Plot code injection | AST-based import blocklist (os, subprocess, socket blocked) |

---

## Quick Start

```bash
# 1. Install PaperBanana — maintained fork, full feature set
#    (slide / slide-batch, --concurrent wave-parallel batching, gpt-image-2)
git clone https://github.com/PlutoLei/paperbanana.git
cd paperbanana && pip install -e ".[google]"

# 2. Add the marketplace & install skills
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project  # optional

# 3. Generate your first figure
# /paperbanana A 4-layer CNN with batch normalization for image classification
```

> **Note:** This repository contains agent **skill definitions** (SKILL.md files). The full-featured Python package lives at [PlutoLei/paperbanana](https://github.com/PlutoLei/paperbanana), a downstream fork of [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) — upstream works too, but only covers diagrams and plots (no slide generation, no `--concurrent`).

---

## Why PaperBanana?

| Pain Point | Traditional | With PaperBanana |
|------------|------------|------------------|
| Methodology figures | Hours in PowerPoint / TikZ | One sentence, 30 seconds |
| Statistical plots | matplotlib boilerplate | Describe your intent, auto-styled |
| Style consistency | Manual effort per figure | Critic agent enforces palette |
| Quality assurance | Eyeball it | 6-item binary checklist, automated |
| Venue compliance | Read style guide, guess | `--venue neurips` handles it |

---

## Pipeline Architecture

<p align="center">
  <img src="examples/pipeline_architecture.png" width="800" alt="PaperBanana Multi-Agent Pipeline"/>
</p>

The pipeline runs iteratively: the **Critic** evaluates each output against academic quality criteria and either accepts it or sends revision instructions back to the **Planner**. Parse failures are handled safely — never silently approved.

### Slide Deck Orchestrator

<p align="center">
  <img src="examples/slide_deck_workflow.png" width="800" alt="Slide Deck RDIV Workflow"/>
</p>

End-to-end presentation creation: analyze content → select from 23 visual styles → generate outlines → batch-generate 4K slides → merge to PPTX/PDF.

---

## Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `generate` | Methodology diagrams | `/paperbanana A transformer with sparse attention` |
| `plot` | Statistical plots | `/paperbanana plot results.csv Bar chart of accuracy` |
| `slide` | Presentation slides | `/paperbanana slide prompt.md` |
| `slide-batch` | Batch slides | `/paperbanana slide-batch prompts/` |
| `evaluate` | Compare gen vs reference | `/paperbanana evaluate gen.png ref.png` |
| `data` | Manage datasets | `/paperbanana data download` |
| `setup` | Setup wizard | `/paperbanana setup` |
| `doctor` | Health check (optional deps / API keys / reference data) | `/paperbanana doctor` |

<details>
<summary><strong>Command Examples</strong></summary>

```bash
# Generate with venue-specific style
/paperbanana generate method.txt "Overview of the proposed framework" --venue neurips --optimize

# Generate from PDF
/paperbanana generate paper.pdf "Architecture diagram" --pages 3-5

# Auto-refine until Critic is satisfied
/paperbanana generate method.txt "Pipeline overview" --auto

# Continue with feedback
/paperbanana generate --continue --feedback "Make the arrows thicker and add color coding"

# Custom provider and aspect ratio
/paperbanana generate method.txt "Wide pipeline" --vlm-provider anthropic --aspect-ratio 16:9

# Batch generate slides with style
/paperbanana slide-batch prompts/ --resolution 4k --style ml-ai --iterations 3
```

</details>

---

## Supported Providers

| Provider | VLM | Image Generation | Setup |
|----------|-----|-----------------|-------|
| Google Gemini | Flash / Pro | Imagen 3 | `GOOGLE_API_KEY` |
| Anthropic Claude | Claude 4 | — | `ANTHROPIC_API_KEY` |
| OpenAI | GPT-4o | DALL-E 3 | `OPENAI_API_KEY` |
| AWS Bedrock | Claude / Nova | Nova Canvas | AWS credentials |
| OpenRouter | Various | Various | `OPENROUTER_API_KEY` |
| LiteLLM | 100+ backends | via backend | `LITELLM_MODEL` / `LITELLM_API_KEY` |
| Ollama | Local models | — | `OLLAMA_BASE_URL` / `OLLAMA_MODEL` |
| Claude Code | via `claude` CLI | — | Claude Code signed in (no key) |

**Retry policy:** Transient errors (429, 5xx) retry with exponential backoff. Auth errors (401, 403) fail immediately — no wasted retries.

---

## Installation

These are Agent Skills following the [skills.sh standard](https://skills.sh) — they run on any skills-compatible runtime (Claude Code, Codex, Cursor, OpenCode, OpenClaw, Gemini CLI, …). Pick the layer that matches your setup.

### Layer 1: One-line install (any runtime, auto-detect)

```bash
npx skills add PlutoLei/paperbanana-skill        # auto-detects your agent
npx skills add PlutoLei/paperbanana-skill -a codex   # or target a runtime explicitly: codex / cursor / opencode / …
```

### Layer 2: Claude Code plugin marketplace (Claude Code only)

```bash
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project  # optional
```

### Layer 3: Manual install (copy SKILL.md into your runtime's skills directory)

Each runtime resolves skills from its own directory — drop `SKILL.md` into the right one:

| Runtime | Skills directory |
|---------|------------------|
| Claude Code | `~/.claude/skills/<name>/` (user) or `.claude/skills/<name>/` (project) |
| Codex | `~/.codex/skills/<name>/` |
| Cursor | `~/.cursor/skills/<name>/` |
| OpenCode / others | that runtime's skills directory |

```bash
# Example — paperbanana skill, adjust the target dir per the table above
DEST="$HOME/.claude/skills/paperbanana"   # ← change for your runtime
mkdir -p "$DEST"
curl -o "$DEST/SKILL.md" \
  https://raw.githubusercontent.com/PlutoLei/paperbanana-skill/master/plugins/paperbanana/skills/paperbanana/SKILL.md

# paperbanana-slide-deck skill (optional)
DECK_DEST="$HOME/.claude/skills/paperbanana-slide-deck"   # ← change for your runtime
mkdir -p "$DECK_DEST"
curl -o "$DECK_DEST/SKILL.md" \
  https://raw.githubusercontent.com/PlutoLei/paperbanana-skill/master/plugins/paperbanana-slide-deck/skills/paperbanana-slide-deck/SKILL.md
```

**Fallback (no skills loader):** any agent can use these without an installer — just `cat` the `SKILL.md` into context as reference material before your request.

### PaperBanana package setup

```bash
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana
pip install -e ".[google]"          # Gemini (default, free tier available)
# pip install -e ".[all]"           # All providers
python -m paperbanana.cli setup     # Interactive API key configuration
```

---

## Style Presets (23 available)

Use `--style <name>` with `slide` or `slide-batch`.

| Category | Styles |
|----------|--------|
| Academic | `scientific`, `biotech`, `neuroscience`, `ml-ai`, `environmental` |
| Professional | `corporate`, `minimal`, `notion`, `bold-editorial` |
| Creative | `watercolor`, `sketch-notes`, `pixel-art`, `fantasy-animation` |
| Premium | `tech-keynote`, `creative-bold`, `financial-elite` |
| Specialized | `blueprint`, `chalkboard`, `dark-atmospheric`, `vintage`, `editorial-infographic`, `vector-illustration`, `intuition-machine` |

---

## Evaluation Infrastructure

PaperBanana v4.0 includes a complete evaluation system for measuring and improving figure quality:

```
evaluation/
├── checklist.py          # 6-item binary pass/fail evaluator
├── judge.py              # VLM-as-Judge comparative evaluation
├── benchmark.py          # End-to-end benchmark harness
└── prompt_ablation.py    # A/B prompt comparison runner

scripts/
├── run_checklist_baseline.py   # Run checklist on existing outputs
└── autoresearch_loop.py        # Automated prompt optimization
```

Run your own baseline:

```bash
python scripts/run_checklist_baseline.py --output-dir outputs/ --report baseline.json
```

Run autoresearch optimization:

```bash
python scripts/autoresearch_loop.py --test-inputs data/checklist_test_set --max-rounds 10 --target 90
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Run `setup` or check `.env` in paperbanana directory |
| "Image generation failed" | Check provider supports image gen (Claude VLM does not) |
| "Critic parse error" | v4.0 marks output as UNREVIEWED instead of silent approval |
| Output marked UNREVIEWED | Critic couldn't evaluate — review the figure manually |
| Windows Unicode errors | Upgrade PaperBanana (`git pull` in project directory) |
| Slow generation | Use `--venue` to skip Retriever, or reduce `--iterations` |

## Contributing

Contributions welcome! See the [Contributing Guide](CONTRIBUTING.md).

## License

MIT
