# PaperBanana Skill for Claude Code

A [Claude Code](https://claude.ai/claude-code) skill that integrates [PaperBanana](https://github.com/llmsresearch/paperbanana) — an agentic framework for generating publication-quality academic diagrams and statistical plots.

## What It Does

Invoke `/paperbanana` in Claude Code to generate:

- **Methodology diagrams** — architecture figures, pipeline overviews, system designs
- **Statistical plots** — bar charts, line plots, scatter plots from CSV/JSON data
- **Diagram evaluation** — compare generated diagrams against human references

Powered by a 5-agent pipeline: Retriever, Planner, Stylist, Visualizer, Critic.

## Examples

```
/paperbanana Our model uses a 4-layer CNN with batch normalization for image classification

/paperbanana generate method.txt Overview of the proposed framework

/paperbanana plot results.csv Bar chart comparing accuracy across models
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

Get a free Google Gemini API key at https://makersuite.google.com/app/apikey

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

Copy `SKILL.md` to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/paperbanana
cp SKILL.md ~/.claude/skills/paperbanana/
```

### 4. Use it

Start a Claude Code session and type:

```
/paperbanana <your description or command>
```

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| Generate | `/paperbanana <text>` | Generate methodology diagram from description |
| Generate (file) | `/paperbanana generate file.txt caption` | Generate from text file |
| Plot | `/paperbanana plot data.csv intent` | Generate statistical plot |
| Evaluate | `/paperbanana evaluate gen.png ref.png` | Compare diagrams |

## Requirements

- [PaperBanana](https://github.com/llmsresearch/paperbanana) installed
- Google Gemini API key (free tier)
- Python 3.10+

## License

MIT
