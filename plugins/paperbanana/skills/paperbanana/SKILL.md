---
name: paperbanana
description: Use when user needs academic diagrams, methodology figures, statistical plots, or presentation slides from text descriptions or data files. Also use for evaluating generated figures against references.
argument-hint: [generate|plot|slide|slide-batch|evaluate|data|setup] [description or file path]
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# PaperBanana - Academic Illustration Generator

Multi-agent pipeline (Retriever → Planner → Stylist → Visualizer → Critic) for publication-quality academic diagrams, statistical plots, and presentation slides.

**API key:** Set provider keys in PaperBanana project's `.env` file.
**Timeout:** 300000 (5 min) for all generation commands.

---

## Commands

All commands run from project root: `cd <paperbanana_dir> && python -m paperbanana.cli <cmd>`

### Command Selection Decision Tree

Route user requests to the right subcommand **before** looking up parameters:

| User intent | Signal words | Subcommand |
|-------------|--------------|------------|
| 方法论/架构/流程图 from text or PDF | "method figure", "架构图", "流程图", "methodology", "pipeline diagram", "论文配图" | `generate` |
| Statistical plot from data file | "plot", "curve", "bar chart", "scatter", "heatmap", has CSV/JSON | `plot` |
| Single presentation slide | "slide", "一张幻灯片", "封面图", single prompt file | `slide` |
| Batch slide generation | "all slides", "批量生成", "N 张幻灯片", `prompts/` directory | `slide-batch` |
| Compare generated vs human reference | "evaluate", "对比", "与参考图对比" | `evaluate` |
| Manage reference dataset | "download dataset", "清缓存" | `data` |
| First-time provider config | "setup", "配置 API key" | `setup` |

**Ambiguous input**: If user provides just a description with no subcommand signal, default to `generate` (see Argument Parsing table for details).

**Out-of-scope**: Pure code generation (matplotlib/seaborn script) is NOT paperbanana's job — those go to `matplotlib` / `scientific-visualization` skills. Paperbanana is for AI-driven image generation + critique loops.

> **Note (upstream sync pending):** Upstream `paperbanana` CLI also adds subcommands (`plot-batch` #123, `sweep` #118) not yet reflected in this table. See the [llmsresearch/paperbanana CHANGELOG](https://github.com/llmsresearch/paperbanana) for the authoritative CLI surface.

### `generate` — Methodology Diagrams

```bash
python -m paperbanana.cli generate --input '<file>' --caption '<caption>' --optimize --verbose
```

When user provides inline text (no file): write to temp file, use as `--input`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--input` / `-i` | — | Path to methodology text file or PDF (`.pdf` requires `pip install 'paperbanana'`) |
| `--caption` / `-c` | — | Figure caption / communicative intent |
| `--output` / `-o` | auto | Output image path |
| `--vlm-provider` | `gemini` | VLM provider: `gemini`, `anthropic`, `openai`, `bedrock`, `openrouter`, `ollama`, `claude_code`, `litellm` |
| `--vlm-model` | auto | VLM model name |
| `--image-provider` | auto | Image gen provider: `google_imagen`, `openai`, `bedrock`, `openrouter` |
| `--image-model` | auto | Image gen model name |
| `--iterations` / `-n` | `3` | Max critic rounds |
| `--auto` | off | Loop until critic is satisfied (safety cap via `--max-iterations`) |
| `--max-iterations` | `30` | Safety cap for `--auto` mode |
| `--optimize` | off | Preprocess inputs (parallel enrichment + caption sharpening) |
| `--continue` | off | Continue from the latest run |
| `--continue-run` | — | Continue from a specific run ID |
| `--feedback` | — | User feedback for the critic when continuing a run |
| `--aspect-ratio` / `-ar` | auto | Target aspect ratio: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `9:16`, `16:9`, `21:9` |
| `--format` / `-f` | `png` | Output format: `png`, `jpeg`, `webp` |
| `--dry-run` | off | Validate inputs without making API calls |
| `--exemplar-retrieval` | off | Enable external exemplar retrieval before planning |
| `--seed` | — | Random seed for reproducible generation |
| `--verbose` / `-v` | off | Show detailed agent progress and timing |
| `--auto-download-data` | off | Auto-download expanded reference set (~257MB) on first run |
| `--venue` | — | Academic venue style: `neurips`, `icml`, `acl`, `ieee`, `custom` |
| `--pages` | — | Page range for PDF input (e.g., `3-5`) |
| `--config` | — | Path to config YAML file |

> **Venue styles:** `--venue neurips` applies NeurIPS-specific methodology and plot style guides from `data/guidelines/`. Each venue has distinct color palettes, layout conventions, and typography expectations.

> **PDF input:** `--input paper.pdf --pages 3-5` extracts text from the specified pages as source context.

> **Exemplar advanced flags:** `--exemplar-retrieval` enables retrieval; see `generate --help` for additional config flags (`--exemplar-endpoint`, `--exemplar-mode`, `--exemplar-top-k`, `--exemplar-timeout`, `--exemplar-retries`).

### `plot` — Statistical Plots

```bash
python -m paperbanana.cli plot --data '<data.csv>' --intent '<intent>' --optimize --verbose
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--data` / `-d` | — | Path to data file (CSV or JSON) **[required]** |
| `--intent` | — | Communicative intent for the plot **[required]** |
| `--output` / `-o` | auto | Output image path |
| `--vlm-provider` | `gemini` | VLM provider |
| `--iterations` / `-n` | `3` | Refinement iterations |
| `--format` / `-f` | `png` | Output format |
| `--aspect-ratio` / `-ar` | auto | Target aspect ratio |
| `--optimize` | off | Enrich context and sharpen caption |
| `--auto` | off | Loop until critic satisfied |
| `--verbose` / `-v` | off | Detailed progress |

### `slide` — Presentation Slides

```bash
python -m paperbanana.cli slide --input '<prompt.md>' --resolution 4k
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--input` / `-i` | — | Path to slide prompt markdown file **[required]** |
| `--caption` / `-c` | auto | Slide intent description |
| `--output` / `-o` | auto | Output image path |
| `--image-model` | auto | Image gen model |
| `--vlm-model` | auto | VLM model name |
| `--iterations` / `-n` | `3` | Max critic rounds |
| `--style` / `-s` | — | Style preset name (see table below) |
| `--list-styles` | off | List all available style presets and exit |
| `--resolution` / `-r` | `4k` | Output resolution: `1k`, `2k`, `4k` |
| `--config` | — | Path to config YAML file |

### `slide-batch` — Batch Slide Generation

```bash
python -m paperbanana.cli slide-batch --prompts-dir '<dir>' --resolution 4k
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--prompts-dir` | — | Directory containing slide prompt markdown files **[required]** |
| `--output-dir` | auto | Output directory |
| `--image-model` | auto | Image gen model |
| `--style` / `-s` | — | Style preset applied to all slides |
| `--iterations` / `-n` | `3` | Max critic rounds per slide |
| `--resolution` / `-r` | `4k` | Output resolution |
| `--concurrent` / `-c` | `2` (settings.batch_concurrent) | Slides generated concurrently; 3 is the sweet spot, never exceed 4. Requires a paperbanana build ≥ 2026-08-03 (maintainer's fork) |

### Wave-Parallel Batch Generation (speed default for ≥2 slides)

With a concurrency-enabled paperbanana build, batch generation runs slides in parallel with identical per-slide quality — every slide keeps its full Critic loop, its own pipeline instance, and its own run directory:

```bash
python -m paperbanana.cli slide-batch --prompts-dir '<dir>' --output-dir '<out>' --resolution 4k --concurrent 3
```

Measured (2026-08-03): 6 slides at `--concurrent 3` in 309s vs 768s serial estimate (0.40x, ~2.5x speedup). Built-in resilience: 5s start-up stagger (same-second bursts to the image API fail or hang server-side long before per-minute quotas are near), in-batch delayed retry for transient 503s (recovery overlaps with other slides), and an end-of-batch serial retry pass for stragglers. Delivery quality is protected twice over: the final image per slide is the **highest-critic-score** iteration (not simply the last), and `critic_score_threshold=9.0` skips provably-done rounds early — calibrated on 69 historical runs with zero false early-stops.

If the installed paperbanana lacks `--concurrent`, fall back to serial `slide-batch` — do NOT spawn more than 3 parallel `slide` processes yourself, as there is no cross-process rate-limit coordination.

### Style Presets (23 available)

Use `--style <name>` with `slide` or `slide-batch`. Use `--list-styles` to see all.

| Style | Source | Best For |
|-------|--------|----------|
| `blueprint` | baoyu | Architecture, system design, technical |
| `chalkboard` | baoyu | Classroom, teaching, education |
| `corporate` | baoyu | Business, investor, quarterly reports |
| `minimal` | baoyu | Executive briefings, clean/simple |
| `sketch-notes` | baoyu | Tutorials, guides, beginner content |
| `watercolor` | baoyu | Lifestyle, wellness, artistic |
| `dark-atmospheric` | baoyu | Entertainment, gaming, cinematic |
| `notion` | baoyu | SaaS, product, dashboards |
| `bold-editorial` | baoyu | Product launches, keynotes, marketing |
| `editorial-infographic` | baoyu | Science communication, explainers |
| `fantasy-animation` | baoyu | Storytelling, magical, children |
| `intuition-machine` | baoyu | Academic research, bilingual |
| `pixel-art` | baoyu | Gaming, retro, developer culture |
| `scientific` | baoyu | Biology, chemistry, medical |
| `vector-illustration` | baoyu | Creative, children, flat design |
| `vintage` | baoyu | Historical, heritage, expedition |
| `tech-keynote` | elite-ppt | Apple/Tesla premium minimalism |
| `creative-bold` | elite-ppt | Google/Airbnb energetic innovation |
| `financial-elite` | elite-ppt | Goldman Sachs/McKinsey sophistication |
| `biotech` | sci-slides | Life sciences, genomics |
| `neuroscience` | sci-slides | Brain research, cognitive science |
| `ml-ai` | sci-slides | Machine learning, deep learning |
| `environmental` | sci-slides | Ecology, climate, sustainability |

### `evaluate` — Comparative Evaluation

```bash
python -m paperbanana.cli evaluate --generated '<gen.png>' --reference '<ref.png>' \
  --context '<text_file>' --caption '<caption>'
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--generated` / `-g` | — | Path to generated image **[required]** |
| `--reference` / `-r` | — | Path to human reference image **[required]** |
| `--context` | — | Path to source context text file **[required]** |
| `--caption` / `-c` | — | Figure caption **[required]** |
| `--vlm-provider` | `gemini` | VLM provider for evaluation |
| `--verbose` / `-v` | off | Detailed progress |

### `data` — Manage Reference Datasets

```bash
python -m paperbanana.cli data download   # Download expanded reference set (~257MB)
python -m paperbanana.cli data info       # Show cached dataset info
python -m paperbanana.cli data clear      # Remove cached dataset
```

### `ablate-retrieval` — Retrieval Ablation (Advanced)

Research utility for running baseline vs retrieval ablation (k sweep). See `ablate-retrieval --help` for details.

### `setup` — Interactive Setup Wizard

```bash
python -m paperbanana.cli setup
```

Guides through API key configuration and provider selection. No flags needed.

---

## Provider Selection

| Provider | VLM | Image Gen | Setup |
|----------|-----|-----------|-------|
| Google Gemini | Flash / Pro | Imagen 3 | `GOOGLE_API_KEY` |
| Anthropic Claude | Claude 4 | — | `ANTHROPIC_API_KEY` |
| OpenAI | GPT-4o | DALL-E 3 | `OPENAI_API_KEY` |
| AWS Bedrock | Claude / Nova | Nova Canvas | AWS credentials |
| OpenRouter | Various | Various | `OPENROUTER_API_KEY` |
| LiteLLM | 100+ backends | via backend | `LITELLM_MODEL` / `LITELLM_API_KEY` |
| Ollama | Local models | — | `OLLAMA_BASE_URL` / `OLLAMA_MODEL` |
| Claude Code | via `claude` CLI | — | Claude Code signed in (no key) |

Use `--vlm-provider` and `--image-provider` flags to select providers per command.

> **⚠️ Provider naming asymmetry (common trap)**: VLM providers use short names (`gemini` / `openai` / `anthropic` / `bedrock` / `openrouter`), but **image providers require the `_imagen` suffix**: `google_imagen` (not `gemini`), `openai_imagen` (not `openai`), `bedrock_imagen`, `openrouter_imagen`. The error `ValueError: Unknown image provider: openai. Available: google_imagen, openrouter_imagen, openai_imagen, bedrock_imagen` means you hit this. Every `--image-provider` example in this document uses the `X_imagen` form.

### Auto-routing decision table

When the user doesn't specify an image model, pick `--image-provider` by the first matching rule (top priority wins). Calibrated from a controlled 16-prompt two-provider comparison (2026-04) plus slide-deck production use:

| # | Condition | Flag to pass | Why |
|---|-----------|--------------|-----|
| 1 | User explicitly names a provider ("use GPT" / "use Gemini" / "nano banana") | That provider | Explicit override beats all auto-rules |
| 1 | User asks for a side-by-side ("both providers", "对比一下") | Run once with each, show both | Dual comparison |
| 2 | Submission-ready venue figures ("投稿用", journal/conference figure) | `--image-provider openai_imagen --image-model gpt-image-2` | Rigor and text fidelity priority |
| 3 | `slide` / `slide-batch` AND the prompt contains CJK text | `--image-provider openai_imagen --image-model gpt-image-2` | Avoids a documented Gemini duplicate-character bug on CJK slide titles |
| 3 | ≥2 reference images for editing/composition | `--image-provider openai_imagen --image-model gpt-image-2` | Avoids Gemini multi-image hallucination (invented text fields) |
| 4 | Traditional East-Asian aesthetics (水墨 / 书法 / 古风 / ukiyo-e etc.) | `--image-provider google_imagen` | Gemini dominates this space (3-0 sweep in comparison test) |
| 4 | `generate` with dense multi-module figures (architecture / ablation / encoder-decoder) | `--image-provider openai_imagen --image-model gpt-image-2` | GPT wins on structural preservation |
| 5 | Everything else | `--image-provider google_imagen` (default) | Better aesthetics on ordinary tasks, ~2x faster, cheaper |

**Never second-guess an explicit user choice.** If the user says which provider to use, use it — even when the auto-rules would pick differently.

## Argument Parsing

| Input Pattern | Action |
|---------------|--------|
| `generate <file.txt> <caption>` | Generate with file + caption |
| `generate <text>` | Write to temp file, auto-caption, generate |
| `plot <data.csv> <intent>` | Plot mode |
| `slide <prompt.md>` | Generate presentation slide |
| `slide-batch <dir>` | Batch generate slides |
| `evaluate <gen.png> <ref.png>` | Comparative evaluation |
| Just a description (no subcommand) | Default to `generate` |

## Error Handling

Two types of API failure can occur during generation. Handle them differently:

### Type 1: Image Generation API Failure (Visualizer)

The image provider (Gemini Imagen, DALL-E, Nova Canvas) fails to return an image.

| Error | Cause | Action |
|-------|-------|--------|
| `429` / `ResourceExhausted` | Rate limit | Wait 30s, retry up to 3 times |
| `500` / `503` / `ServerError` | Provider outage | Switch to fallback provider (see chain below) |
| `400` / `InvalidArgument` | Bad prompt (too long, policy violation) | Shorten/rephrase prompt, retry once |
| `401` / `403` | Invalid API key | Stop and ask user to run `setup` |
| Timeout (>60s no response) | Network or provider hang | Retry once, then switch provider |

**Fallback chain:** `google_imagen` → `openai` → `bedrock` → `openrouter`. Use the next provider in chain that has a valid API key in `.env`. If all fail, stop and report the error.

### Type 2: VLM Critic API Failure

The VLM provider (Gemini Flash, Claude, GPT-4o) fails during quality evaluation.

| Error | Cause | Action |
|-------|-------|--------|
| `429` / Rate limit | Too many requests | Wait 15s, retry up to 3 times |
| JSON parse failure | VLM returned malformed response | **Do NOT treat as "approved"**. Retry once with stricter prompt. If still fails, mark output as `UNREVIEWED` |
| `500` / `503` | Provider outage | Switch VLM provider (see chain below) |
| Timeout (>30s) | Network hang | Retry once, then skip Critic and mark as `UNREVIEWED` |

**VLM fallback chain:** `gemini` → `anthropic` → `openai` → `openrouter`.

**Critical rule:** A Critic failure must NEVER silently approve an image. If Critic cannot evaluate, the output status must be `UNREVIEWED`, not `APPROVED`. Report this clearly to the user.

### Recovery with `--continue`

Use `--continue` to resume after any failure:

| Scenario | Command |
|----------|---------|
| Pipeline crashed mid-generation | `--continue` (resumes latest run) |
| Want to iterate on a specific run | `--continue-run <run_id>` |
| Want to provide feedback for next iteration | `--continue --feedback "make the arrows thicker"` |

The run directory preserves all intermediate state (plans, images, critic feedback). `--continue` picks up from the last successful step.

### Batch Mode (`slide-batch`) Resilience

When generating multiple slides, a single slide failure should NOT kill the batch:
1. Log the failure for the specific slide
2. Continue generating remaining slides
3. At the end, report which slides succeeded and which failed
4. User can re-run with `--continue` to retry only failed slides

---

## 🔴 User Confirmation Checkpoints

Paperbanana is CLI-first, but three user-facing actions are expensive or irreversible. **🛑 STOP and ask for explicit confirmation** before running any row below — do not proceed on assumed consent.

| 🔴 Trigger | 🛑 STOP — Confirm before proceeding |
|------------|--------------------------------------|
| `--auto` with `--max-iterations > 5` | **🛑 STOP.** Show: cap, est. API cost (≈ iterations × $0.04), est. wall time (≈ iterations × 30s). Ask: "Proceed with up to N iterations?" Do not kick off until user says yes. |
| `--auto-download-data` on first run | **🛑 STOP.** Announce: "reference dataset will be downloaded to cache (~257MB full_bench, or lightweight curated set in upstream ≥ #112)". Ask: "Continue?" Do not download until confirmed. |
| `setup` wizard | **🛑 STOP.** Before writing to `.env`, show the exact keys and preview of values (redact secrets after 4 chars). Ask: "Save to .env?" Do not write until confirmed. |

**✅ No checkpoint needed:** normal `generate` / `plot` / `slide` (no `--auto`, within iteration cap 3) — these are short, cheap, and the Critic loop is self-bounded. Run them directly.

---

## ⛔ Anti-Patterns — Red-Line Blacklist

Hard "do NOT" rules. Each maps to a failure mode already encoded above — this section consolidates them into one scannable list.

| ⛔ Anti-pattern | Why it's wrong | Do this instead |
|-----------------|----------------|-----------------|
| Treating a Critic API failure as "approved" | Ships an unreviewed image as if it passed QA | Mark `UNREVIEWED`, never `APPROVED`; report to user |
| Proceeding past a 🔴 checkpoint without confirmation | Burns API budget / overwrites `.env` on assumed consent | 🛑 STOP at every checkpoint row; wait for explicit yes |
| Writing matplotlib/seaborn scripts | That's `scientific-visualization`'s job, not paperbanana | Route code-gen away; paperbanana = AI image gen + critique loop |
| Killing the whole `slide-batch` on one slide failure | Loses N−1 good slides over 1 bad one | Log the failure, continue, report survivors, retry via `--continue` |
| Full regeneration after a mid-run crash | Throws away plans/images/critic state, wastes API spend | Resume with `--continue` / `--continue-run <id>` |
| Routing every "make a figure" to `generate` | `plot` (data files) and `slide` (presentation) have dedicated paths | Run the Command Selection Decision Tree first |
| Inventing CLI flags not in the parameter tables | Upstream CLI surface drifts (see #115/#118/#123 note) | Verify with `<cmd> --help`; don't fabricate flags |

---

## After Generation

1. Parse output to find image path
2. Use Read tool to display the generated image
3. Report Run ID, iteration count, and Critic feedback
4. If any outputs are marked `UNREVIEWED`, warn the user explicitly
5. **If user expresses dissatisfaction OR status is UNREVIEWED**, proactively suggest:
   `python -m paperbanana.cli <cmd> --continue --feedback "<specific fix>"` — preserves run state, avoids full regeneration
