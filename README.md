# PaperBanana Skill for Claude Code

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-2.1.0-orange?style=flat-square" />
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Skill-2B6CB0?style=flat-square" />
  <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-black?style=flat-square" />
</p>

<p align="center">
  <strong>English</strong> | <a href="README_CN.md">中文</a>
</p>

A [Claude Code](https://claude.ai/claude-code) skill that integrates [PaperBanana](https://github.com/llmsresearch/paperbanana) — an agentic framework for generating publication-quality academic diagrams and statistical plots.

## What It Does

Invoke `/paperbanana` in Claude Code to:

- **Generate methodology diagrams** — architecture figures, pipeline overviews, system designs
- **Create statistical plots** — bar charts, line plots, scatter plots from CSV/JSON data
- **Benchmark** — run PaperBananaBench evaluation suite
- **Polish** — style-guide refinement of existing images
- **Evaluate** — compare generated diagrams against human references

Powered by a 5-agent pipeline: Retriever → Planner → Stylist → Visualizer → Critic.

## What's New in v2.1

- **Auto VLM selection** — `--vlm-model auto` (default) automatically picks Flash (fast) or Pro (quality) based on input complexity
- **6 pipeline modes** — `vanilla`, `planner`, `planner_stylist`, `planner_critic`, `full`, `polish`
- **`bench` command** — run PaperBananaBench evaluations directly from Claude Code
- **`polish` command** — style-guide polishing of existing images
- **Robust Critic JSON parsing** — 4-layer fallback: json.loads → json-repair → regex → safe defaults

## Examples

```
/paperbanana Our model uses a 4-layer CNN with batch normalization for image classification

/paperbanana generate method.txt Overview of the proposed framework

/paperbanana plot results.csv Bar chart comparing accuracy across models

/paperbanana bench data/PaperBananaBench/ --task diagram --max-samples 5

/paperbanana polish output.png --task diagram
```

## Sample Output

**Transformer with Sparse Attention:**

![Transformer Architecture](https://github.com/PlutoLei/paperbanana-skill/raw/master/examples/transformer_architecture.png)

**CNN Image Classification:**

![CNN Architecture](https://github.com/PlutoLei/paperbanana-skill/raw/master/examples/cnn_architecture.png)

## Installation

### 1. Install PaperBanana

```bash
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana
pip install -e ".[google]"
```

### 2. Set up API key

Get a Google Gemini API key at https://aistudio.google.com/apikey

Create a `.env` file in the paperbanana directory:

```
GOOGLE_API_KEY=your-api-key-here
```

### 3. Install the skill

**Option A: Install via CLI**

```bash
claude install-skill PlutoLei/paperbanana-skill
```

**Option B: Manual install**

```bash
mkdir -p ~/.claude/skills/paperbanana
cp SKILL.md ~/.claude/skills/paperbanana/
```

### 4. Use it

```
/paperbanana <your description or command>
```

## Commands

| Command | Example | Description |
|---------|---------|-------------|
| `generate` | `/paperbanana <text>` | Generate methodology diagram from description |
| `generate` (file) | `/paperbanana generate file.txt caption` | Generate from text file |
| `plot` | `/paperbanana plot data.csv intent` | Generate statistical plot |
| `bench` | `/paperbanana bench dataset/ --task diagram` | Run PaperBananaBench evaluation |
| `polish` | `/paperbanana polish image.png` | Style-guide polishing |
| `evaluate` | `/paperbanana evaluate gen.png ref.png` | Compare diagrams |

## Pipeline Modes

| Mode | Pipeline | Critic |
|------|----------|--------|
| `vanilla` | Direct generation | No |
| `planner` | Retriever → Planner → Visualizer | No |
| `planner_stylist` | + Stylist | No |
| `planner_critic` | + Critic loop | Yes |
| `full` | Full pipeline (default) | Yes |
| `polish` | Style-guide polishing | No |

## Requirements

- [PaperBanana](https://github.com/llmsresearch/paperbanana) installed
- Google Gemini API key
- Python 3.10+

## License

MIT
