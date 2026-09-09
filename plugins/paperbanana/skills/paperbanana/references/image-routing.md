# Codex image routing and optional backend

Verified against the public OpenAI documentation and the native tool schema on 2026-09-09.
This is a capability contract; it is not a measurement of either model's quality.

## Choose the route

| Request | Route | Python core required? |
| --- | --- | --- |
| New Codex request with no existing/chosen backend: ordinary generation, composition or editing | Available native image tool | No |
| Native text, tables, charts and shapes in an editable PPTX | Slide-deck renderer | No |
| Exact Sunburst/Flare model, quality, pixel size, output format, transparent-background control or mask file | Explicit Image API via `paperbanana image` | Yes |
| Retrieval, planning, styling and Critic loop | Existing PaperBanana pipeline | Yes |
| Preview review using the Python Critic | Optional `review-editable.py` integration | Yes, for a real Critic call |

Preserve explicit **and existing** Gemini routes, including their default-selection rules and
API-key/Vertex configuration. Resolve a saved task's provider before considering native fallback;
pass `provider: "google_imagen"` into the helper for a Gemini-bound request even when native is
available. A Gemini model request uses the existing Gemini integration, never the OpenAI-only
`image` command. This update does not migrate Gemini work or change its retries/Polish behavior.

Honor an explicit provider choice. If native is explicitly requested together with unsupported
strict controls, explain the incompatibility before changing routes. Lack of a native tool does
not imply API credentials or spending authority. Do not install the core or read credential files
for native generation or an editable PPTX build.

The core repository is an optional backend, not a second skill collection. Keep API encoding,
validation, retry behavior and provenance there; do not embed a duplicate API client in this skill.
Gemini retains its existing backend path. Other hosts use their available provider integration; this document does not assert that they
have Codex's native tool.

## Native call contract

Inspect the tool schema exposed in the current session. The verified `image_gen.imagegen` schema
accepts `prompt`, `referenced_image_paths` and `num_last_images_to_include`. It has no `model`,
`quality`, `size`, `mask` or `background` field. A prompt can express a preference, but cannot prove
an exact model or pixel-level control. Do not claim that native output used Image 2.5.

- Brand-new image: pass `prompt`; omit both reference fields.
- Edit using local images: inspect them with `view_image`, then supply all absolute paths in
  `referenced_image_paths`.
- If at least one target has no local path, use the smallest `num_last_images_to_include` (1–5)
  that covers all target images. Never send both reference fields. If neither mechanism covers
  every target, ask the user to attach the missing images again.
- Call the host's image tool, wait using its supported asynchronous mechanism, and return its
  native image result (in Codex code mode: `generatedImage(result)`). Inspect the output before
  claiming that the requested edit succeeded.
- Report the model as unreported when the result does not expose it. Tool success is generation
  evidence; it does not mean a Critic or human accepted the output.

A deterministic, offline routing helper ships at `scripts/route-image.mjs` beside the packaged
PaperBanana skill. In the source repository it is at
`plugins/paperbanana/skills/paperbanana/scripts/route-image.mjs`. It only emits a decision:

```json
{"prompt":"A three-stage research workflow","mode":"generate","native_available":true}
```

Run `node <path-to-route-image.mjs> request.json`. `native_available` must reflect the current
session. Structured strict controls mean an API route; do not convert a loose visual preference
into a strict control unnecessarily. The helper does not submit requests or inspect file content.
The slide-deck plugin can follow this same decision table without installing the helper.

## Explicit Image API route

Requires a core build containing the `image` subcommand; this feature is developed on
[`PlutoLei/paperbanana`, `codex/image25-adapter`](https://github.com/PlutoLei/paperbanana/tree/codex/image25-adapter).
Check `python -m paperbanana.cli image --help` in the chosen core checkout before using examples.
Do not assume a PyPI or upstream installation already contains these fork additions.

```bash
# Offline contract validation: no credentials, no API client, no generation.
python -m paperbanana.cli image --input prompt.md --output candidate.png \
  --model gpt-image-2.5-flare --quality high --size 1536x864 --dry-run

# Reference and mask validation; remove --dry-run only for authorized live execution.
python -m paperbanana.cli image --input edit.md --output edited.png \
  --model gpt-image-2.5-sunburst --quality xhigh --size 1536x864 \
  --reference original.png --mask mask.png --dry-run
```

Repeat `--reference` for multiple inputs. A mask requires a reference, matching dimensions and an
alpha channel; transparent mask pixels specify the editable region. Inputs are encoded as PNG.
`.png`, `.jpg`/`.jpeg` or `.webp` chooses the output format. Transparent output requires PNG/WebP.
For reproducible comparisons use dated model IDs ending in `-2026-09-08`; this pins a requested
model, not a deterministic output. A configured model name does not prove account access.

Quality accepts `low`, `medium`, `high`, `xhigh`, `max`, `auto` for Image 2.5; older GPT Image models
reject the added tiers. Custom dimensions must be multiples of 16, aspect ratio between 1:3 and
3:1, each edge at most 3840, and 655360–8294400 total pixels. Outputs above 2560×1440 are
experimental in the official guide. Explicit size overrides configured size, then aspect ratio,
then dimensions. Project defaults remain unchanged; use opt-in `configs/image25-*.yaml` profiles.

Sunburst's editing emphasis and Flare's speed emphasis are official product positioning. Do not
promote either as the measured best route until the local evaluation has been run and reviewed.

## Failure, recovery and response

The OpenAI provider is the only image-request retry owner. SDK retries are disabled; bounded
429/5xx retries use backoff (at most three attempts by default). Quota, moderation, authentication,
permission and invalid requests terminate. Timeouts/connections may have reached the service:
record `result_unknown`, preserve artifacts and inspect before explicitly resubmitting. Never
stack shell retries around the whole pipeline or silently switch model/provider.

For the updated OpenAI `slide-batch` path, reuse requires a matching request fingerprint, output hash and
image decode. Re-run with the same prompts and settings; changed or corrupt outputs are rebuilt.
A running/ambiguous matching attempt is skipped until an explicitly chosen `--retry-unknown`.
Use a new output directory after changing pipeline code, prompt templates or reference-library
contents. Only one process should own a batch directory. A valid filename alone is not a resume receipt.

Critic failure leaves the output `UNREVIEWED`. Preserve candidates and explain the review failure;
skipping review cannot turn them into approved output. Generation sidecars describe the image
request, not the final Critic verdict. Manual visual inspection and automated Critic review must
be attributed separately.

The final response should include the artifact/preview, route, requested and reported model (or
unknown), measured elapsed time if available, changed/failed batch items and actual review status.
Cost without billing evidence is unknown, not zero. `image` saves `<output-stem>.image.json` with
safe request metadata; it does not persist credentials or prompts. Do not expose raw SDK errors
or credential values in responses.

## Evaluation and optimization

The core ships `evaluations/image25/cases.json`: 24 planned cases in six categories, each with two
tuning and two holdout cases. Its offline summarizer excludes mocks and keeps missing costs,
latencies and reviews missing. Freeze editing references/masks and their hashes before live runs.
Tune on the tuning split, then freeze the selected profile before opening holdout results.
Do not infer measured quality, latency, cost or release acceptance from unit tests.

Sources: [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst),
[Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare),
[Image API guide](https://developers.openai.com/api/docs/guides/image-generation),
[Codex image generation](https://learn.chatgpt.com/docs/image-generation).
