---
name: paperbanana
description: Generate publication-quality academic diagrams and statistical plots from text descriptions using the PaperBanana multi-agent framework. Use when the user wants to create methodology diagrams, architecture figures, or statistical plots for academic papers.
argument-hint: [generate|plot|bench|polish|evaluate] [description or file path]
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# PaperBanana - Academic Illustration Generator

Multi-agent pipeline (Retriever → Planner → Stylist → Visualizer → Critic) for publication-quality academic diagrams.

**API key:** Set `GOOGLE_API_KEY` in your PaperBanana project's `.env` file.
**Timeout:** 300000 (5 min) for all generation commands.

---

## Commands

All commands run from project root: `cd <paperbanana_dir> && python -m paperbanana.cli <cmd>`

### `generate` — Methodology Diagrams

```bash
python -m paperbanana.cli generate --input '<file>' --caption '<caption>' --mode full
```

When user provides inline text (no file): write to temp file, use as `--input`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--mode` / `-m` | `full` | Pipeline mode (see below) |
| `--iterations` / `-n` | `3` | Max critic rounds |
| `--vlm-model` | `auto` | `auto` = auto Flash/Pro selection; or specify model name |
| `--output` / `-o` | auto | Output path |

### Pipeline Modes

| Mode | Pipeline | Critic |
|------|----------|--------|
| `vanilla` | Direct generation | No |
| `planner` | Retriever → Planner → Visualizer | No |
| `planner_stylist` | + Stylist | No |
| `planner_critic` | + Critic loop | Yes |
| `full` | Full pipeline (default) | Yes |
| `polish` | Style-guide polishing of existing image | No |

### `plot` — Statistical Plots

```bash
python -m paperbanana.cli plot --data '<data.csv>' --intent '<intent>'
```

### `bench` — PaperBananaBench Evaluation

```bash
python -m paperbanana.cli bench --dataset '<bench_path>' --task diagram --max-samples 5
```

### `polish` — Style Guide Polishing

```bash
python -m paperbanana.cli polish --image '<image_path>' --task diagram
```

### `evaluate` — Comparative Evaluation

```bash
python -m paperbanana.cli evaluate --generated '<gen.png>' --reference '<ref.png>' \
  --context '<text_file>' --caption '<caption>'
```

---

## Argument Parsing

| Input Pattern | Action |
|---------------|--------|
| `generate <file.txt> <caption>` | Generate with file + caption |
| `generate <text>` | Write to temp file, auto-caption, generate |
| `plot <data.csv> <intent>` | Plot mode |
| `bench <dataset_path>` | Bench evaluation |
| `polish <image_path>` | Style-guide polishing |
| `evaluate <gen.png> <ref.png>` | Comparative evaluation |
| Just a description (no subcommand) | Default to `generate` |

## After Generation

1. Parse output to find image path
2. Use Read tool to display the generated image
3. Report Run ID, iteration count, and Critic feedback
