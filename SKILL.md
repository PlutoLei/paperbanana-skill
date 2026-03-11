---
name: paperbanana
description: Generate publication-quality academic diagrams, statistical plots, and presentation slides from text descriptions using PaperBanana multi-agent framework.
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

### `generate` — Methodology Diagrams

```bash
python -m paperbanana.cli generate --input '<file>' --caption '<caption>' --config configs/fast.yaml --optimize --auto --verbose
```

When user provides inline text (no file): write to temp file, use as `--input`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--input` / `-i` | — | Path to methodology text file |
| `--caption` / `-c` | — | Figure caption / communicative intent |
| `--output` / `-o` | auto | Output image path |
| `--vlm-provider` | `gemini` | VLM provider: `gemini`, `anthropic`, `openai`, `bedrock`, `openrouter` |
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
| `--config` | — | Path to config YAML file |

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
python -m paperbanana.cli slide-batch --prompts-dir '<dir>' --resolution 4k --config configs/fast.yaml --auto
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--prompts-dir` | — | Directory containing slide prompt markdown files **[required]** |
| `--output-dir` | auto | Output directory |
| `--image-model` | auto | Image gen model |
| `--style` / `-s` | — | Style preset applied to all slides |
| `--iterations` / `-n` | `3` | Max critic rounds per slide |
| `--resolution` / `-r` | `4k` | Output resolution |

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

Use `--vlm-provider` and `--image-provider` flags to select providers per command.

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

## After Generation

1. Parse output to find image path
2. Use Read tool to display the generated image
3. Report Run ID, iteration count, and Critic feedback
