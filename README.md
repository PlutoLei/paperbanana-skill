# PaperBanana Skills for Claude Code

<p align="center">
  <a href="https://github.com/PlutoLei/paperbanana-skill/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/PlutoLei/paperbanana-skill?style=flat-square&color=yellow" /></a>
  <img alt="Version" src="https://img.shields.io/badge/version-4.0.0-blue?style=flat-square" />
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Skills-2B6CB0?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="Providers" src="https://img.shields.io/badge/Providers-5-green?style=flat-square" />
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
</table>

<p align="center"><em>All figures generated from plain text descriptions — zero manual drawing.</em></p>

<details>
<summary><strong>More Examples</strong> (architecture diagrams, slides)</summary>
<br/>
<table>
<tr>
<td align="center"><strong>Transformer Architecture</strong><br/><img src="examples/transformer_architecture.png" width="380"/></td>
<td align="center"><strong>Mamba SSM Architecture</strong><br/><img src="examples/mamba_architecture.png" width="380"/></td>
</tr>
<tr>
<td align="center" colspan="2"><strong>RAG Pipeline</strong><br/><img src="examples/rag_pipeline.png" width="760"/></td>
</tr>
</table>
</details>

---

## Skills in this Marketplace

| Skill | Scope | Description | Version |
|-------|-------|-------------|---------|
| **paperbanana** | user | Academic diagrams, plots, slides, and quality evaluation | v4.0.0 |
| **paperbanana-slide-deck** | project | Full slide deck orchestration (RDIV workflow) | v1.0.0 |

## Feature Matrix

| Capability | Status | Details |
|------------|--------|---------|
| Methodology diagrams | ✅ | Text → publication-quality figure in 30s |
| Statistical plots | ✅ | CSV/JSON data → auto-styled academic plot |
| Presentation slides | ✅ | Markdown → 4K slide with 23 style presets |
| Multi-venue styles | ✅ **New** | `--venue neurips\|icml\|acl\|ieee\|custom` |
| PDF input | ✅ **New** | `--input paper.pdf --pages 3-5` |
| 6-item quality eval | ✅ **New** | Binary checklist: completeness, layout, annotation, color, legibility, hallucination |
| Autoresearch loop | ✅ **New** | Automated prompt self-optimization with keep/revert |
| Error handling | ✅ **New** | Critic UNREVIEWED status, provider fallback chains, retry filtering |
| 5 VLM providers | ✅ | Gemini, Claude, OpenAI, Bedrock, OpenRouter |
| Auto-refine | ✅ | `--auto` loops until Critic is satisfied |
| Run continuation | ✅ | `--continue` with `--feedback` for iterative refinement |
| Dynamic aspect ratio | ✅ | 8 Imagen ratios, Planner auto-recommends |

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
# 1. Install PaperBanana
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana && pip install -e ".[google]"

# 2. Add the marketplace & install skills
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project  # optional

# 3. Generate your first figure
# /paperbanana A 4-layer CNN with batch normalization for image classification
```

> **Note:** This repository contains Claude Code **skill definitions** (SKILL.md files). The underlying Python package lives at [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana).

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

**Retry policy:** Transient errors (429, 5xx) retry with exponential backoff. Auth errors (401, 403) fail immediately — no wasted retries.

---

## Installation

### Option A: Plugin marketplace (recommended)

```bash
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project  # optional
```

### Option B: Manual install

```bash
# paperbanana skill (user-level)
mkdir -p ~/.claude/skills/paperbanana
curl -o ~/.claude/skills/paperbanana/SKILL.md \
  https://raw.githubusercontent.com/PlutoLei/paperbanana-skill/master/plugins/paperbanana/skills/paperbanana/SKILL.md

# paperbanana-slide-deck skill (project-level, optional)
mkdir -p .claude/skills/paperbanana-slide-deck
curl -o .claude/skills/paperbanana-slide-deck/SKILL.md \
  https://raw.githubusercontent.com/PlutoLei/paperbanana-skill/master/plugins/paperbanana-slide-deck/skills/paperbanana-slide-deck/SKILL.md
```

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
