---
name: paperbanana
description: Generate publication-quality academic diagrams and statistical plots from text descriptions using the PaperBanana multi-agent framework. Use when the user wants to create methodology diagrams, architecture figures, or statistical plots for academic papers.
argument-hint: [generate|plot|evaluate] [description or file path]
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# PaperBanana - Academic Illustration Generator

Generate publication-quality academic diagrams using a multi-agent AI pipeline (Retriever, Planner, Stylist, Visualizer, Critic).

## Prerequisites

1. **PaperBanana** must be installed: `pip install -e ".[google]"` from the [paperbanana repo](https://github.com/llmsresearch/paperbanana)
2. **Google Gemini API key** must be configured in the project's `.env` file:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```
   Get a free key at: https://makersuite.google.com/app/apikey

## Environment Detection

Before running commands, detect the PaperBanana installation:

1. Try running `python -m paperbanana.cli --help` to check if paperbanana is available in the current Python environment
2. If not found, search for common locations:
   - Check if a `paperbanana` directory exists in the current workspace
   - Look for virtual environments (`.venv`, `venv`, conda envs) that may have it installed
3. Set the working directory to where PaperBanana is installed (contains `paperbanana/` package and `.env`)

**Command pattern:**

```bash
cd <paperbanana_project_dir> && python -m paperbanana.cli <command> <args>
```

On Windows with conda, you may need:
```
powershell -Command "Set-Location '<paperbanana_dir>'; & '<python_path>' -m paperbanana.cli <command> <args> 2>&1"
```

Set timeout to 300000 (5 minutes) for generate/plot commands since they call external APIs.

## Usage Modes

### Mode 1: `generate` - Methodology Diagrams

Generate a methodology/architecture diagram from text.

**When user provides a file path:**

```bash
python -m paperbanana.cli generate --input '<file_path>' --caption '<caption>' --iterations 2
```

**When user provides inline text (no file):**

1. Write the user's methodology text to a temporary file (e.g., `temp_input.txt`) in the PaperBanana project directory
2. Run the generate command with that temp file as `--input`
3. Clean up the temp file after completion

**Parameter guidelines:**
- `--caption`: Extract or craft a concise figure caption from the user's description. Should describe what the diagram communicates (e.g., "Overview of the proposed encoder-decoder architecture").
- `--iterations`: Default to 2 for balanced quality/speed. Use 1 for quick drafts, 3 for highest quality.
- `--vlm-model`: Default is `gemini-3-flash-preview`. For complex diagrams, suggest `gemini-3-pro-preview`.
- `--output`: Optional output path. If not specified, saves to `outputs/<run_id>/final_output.png`.

### Mode 2: `plot` - Statistical Plots

Generate statistical plots from CSV or JSON data.

```bash
python -m paperbanana.cli plot --data '<data_file>' --intent '<intent>' --iterations 2
```

- `--data`: Path to CSV or JSON file
- `--intent`: What the plot should communicate (e.g., "Bar chart comparing model accuracy across datasets")

### Mode 3: `evaluate` - Diagram Evaluation

Compare a generated diagram against a human reference.

```bash
python -m paperbanana.cli evaluate --generated '<gen_path>' --reference '<ref_path>' --context '<text_path>' --caption '<caption>'
```

## Argument Parsing

Parse `$ARGUMENTS` as follows:

| Input Pattern | Action |
|---------------|--------|
| `generate <file.txt> <caption>` | Use file as --input, text as --caption |
| `generate <description text>` | Write text to temp file, auto-generate caption |
| `plot <data.csv> <intent>` | Use file as --data, text as --intent |
| `evaluate <gen.png> <ref.png>` | Use as --generated and --reference |
| Just a description (no subcommand) | Default to `generate` mode |

If the user provides only a description without specifying a mode, default to `generate`.

## After Generation

1. Parse the output to find the image path (look for "Output saved to:" in stdout)
2. Use the Read tool to display the generated image to the user
3. Report the Run ID, iteration count, and any Critic feedback
4. If the Critic suggested revisions, inform the user they can re-run with more iterations

## Examples

**User**: `/paperbanana generate method.txt Overview of sparse attention transformer`

Action: Run generate with the provided file and caption.

**User**: `/paperbanana Our model consists of an encoder that processes input features through 3 convolutional layers, followed by a decoder with skip connections`

Action: Write text to temp file, generate caption "Overview of the proposed encoder-decoder architecture with skip connections", run generate.

**User**: `/paperbanana plot results.csv Bar chart comparing accuracy of ResNet vs VGG vs EfficientNet`

Action: Run plot with the CSV file and the intent description.
