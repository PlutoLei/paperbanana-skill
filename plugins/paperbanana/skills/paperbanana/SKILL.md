---
name: paperbanana
description: Generate and revise academic figures, data plots, or image slides through a configured PaperBanana backend; inspect their automated review status. Use for PaperBanana requests and academic image generation, not general presentation editing or code-only plotting.
argument-hint: "[generate|plot|slide|slide-batch|evaluate|data|setup] [description or file path]"
---

# PaperBanana

Translate a research brief into an image-generation task, then inspect both the
output and its review. For a complete deck or native editable PowerPoint, use
the separately installed `paperbanana-slide-deck` skill when available.

## Establish the task

1. Identify the requested output, input material, destination and existing run.
   For a review or plan-only request, return findings without creating files or
   calling generation tools. Reuse the user's approved choices.
2. Preserve explicit and saved image-provider/model choices, including Gemini or
   Vertex configuration. The agent host does not select the image provider.
   If no choice exists, use the configured backend; ask only if an actual choice
   is missing. Historical examples do not establish a current model ranking.
3. Locate the user-selected Python backend/environment. Check the relevant
   command's `--help` before using version-dependent flags. Do not scan another
   agent's private directories or read credentials into the conversation.
4. Separate native PowerPoint editing from raster image generation. A screenshot
   or embedded SVG is not a native editable text box, table or chart.

## Choose the command

| Intent | Command | Required material |
| --- | --- | --- |
| Method, architecture or workflow figure | `generate` | Source text/PDF and communicative intent |
| Statistical plot | `plot` | Actual CSV/JSON data and plot intent |
| One image slide | `slide` | Slide prompt |
| Several image slides | `slide-batch` | Prompt directory |
| Compare an image with a reference | `evaluate` | Both images, source context and caption |
| Dataset information/download/removal | `data` | Requested operation; removal needs its own scope |
| Provider setup | `setup` | A configuration request; use the host's credential workflow |

See [command examples](references/commands.md) for invocation patterns. Use the
selected checkout's help as the CLI authority. Code-only plotting requests can
use the host's plotting tools without an image-model call.

Image-provider flags use factory names such as `google_imagen`, `openai_imagen`,
`bedrock_imagen` and `openrouter_imagen`. VLM flags use names such as `gemini`,
`openai` and `anthropic`. Verify names against the installed version.

## Generate or revise

- Keep supplied labels, arrows, quantities and scientific meaning traceable to
  the input. Mark invented example data as illustrative. Do not repair missing
  research facts by making them up. For mixed-language figures, carry an explicit
  list of required labels into the prompt and check them in the returned image.
- Write inline input into a task-owned text file when execution is authorized.
  Pass file paths as quoted arguments; do not interpolate user prose into shell
  commands. Keep the original input and references intact.
- Use the authorized provider and iteration limits. Do not add paid optimization,
  a provider comparison, a large dataset download or an unbounded retry loop to
  a request that did not authorize it. Reuse existing authorization within scope.
- For edits, identify the exact prior run/image and reference files first. Use
  that command's supported continuation/edit mechanism. If the backend lacks
  reference editing, explain the limitation before substituting regeneration.
- For a single changed slide, regenerate that slide and reassemble the deck;
  preserve unrelated pages and source prompts. A failed batch does not authorize
  discarding successful pages or regenerating the entire deck.

## Recover without changing the task

| Observed result | Next action |
| --- | --- |
| Rate limit or temporary service error | Use the backend's bounded retry policy within the approved limit; report exhausted attempts |
| Authentication/configuration error | Stop that call and report the required setup; do not print keys or try another account |
| Timeout with uncertain generation outcome | Inspect the run and existing output before retrying, to avoid duplicate work/charges |
| Requested provider unavailable | Keep the selection; present a concrete alternative only if a new choice is needed |
| Critic timeout, malformed output or unavailable review | Preserve the image and mark it `UNREVIEWED`; never treat missing feedback as acceptance |
| Partial batch | List successful/missing pages and resume only the missing or requested pages using supported commands |

Do not switch providers merely because a fallback credential exists. A retry or
fallback must preserve the user's routing and spending choices. Continuation
flags are command-specific: `generate --continue-run` is not evidence that
`slide-batch --continue` exists.

## Inspect and deliver

Open the actual output when the host has an image viewer. Check requested labels,
connections, numbers, cropping and legibility. If it cannot be inspected, say so.
Report the artifact, run identifier when available, provider/model only as
actually known, and review state separately. A successful API call, a Critic
score and scientific acceptance are different claims.

When revisions are needed, identify the concrete defect and revise the affected
input/run within scope. Do not repeatedly rerun generation without a new
diagnosis. Keep failures and unreviewed pages visible in the final report.
