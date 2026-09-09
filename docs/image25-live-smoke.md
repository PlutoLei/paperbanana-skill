# Live integration smoke test — 2026-09-09

Real service calls succeeded through the OpenAI adapter, the native Codex tool and the existing
Gemini/Vertex configuration. This was a bounded functional smoke test with prompt refinement,
not the planned 24-case × 4-profile benchmark. Request success and visual acceptance are separate.
No default model or provider was changed.

## Source and environment

- Core source: [`50d0709`](https://github.com/PlutoLei/paperbanana/commit/50d0709b4f8d24acebd5257cb2b7055fd201984c).
- Skill/router source: [`a708e9b`](https://github.com/PlutoLei/paperbanana-skill/commit/a708e9b80ead5aa456a447a4227b6e369cc2eb07).
- Python 3.11; OpenAI SDK 2.30.0; Google Gen AI SDK 1.73.1.
- OpenAI requests used `api.openai.com` with existing credentials. Native model identity was not exposed.
- Gemini image generation used the owner's existing checkout/configuration, including pending
  Gemini/Vertex changes. Critic used a private compatibility copy combining those changes with
  the feature source. The original checkout's tracked diff, status and new Google auth file
  digests remained unchanged. The pending Google changes are not part of this feature branch.
- Earlier offline compatibility coverage: 173 passed, 3 optional MCP skips; see
  [offline validation](image25-validation.md).

## Calls and observations

All eight OpenAI image requests completed on the first attempt and produced 1536×864 PNG files.
Times below are individual provider observations, not a speed benchmark. OpenAI image responses
did not report a model name; the table records the requested model. Local sidecars retain request
IDs, requested controls, output hashes and elapsed time. Generation-side `UNREVIEWED` metadata
is distinct from the subsequent visual/OCR/Critic checks described here.

| Case | Requested model | Quality | Seconds | Observation |
| --- | --- | --- | ---: | --- |
| Bilingual RAG slide | gpt-image-2.5-flare | high | 19.61 | Visual and OCR check passed |
| Bilingual RAG slide | gpt-image-2.5-sunburst | high | 25.02 | Readable labels; title split over two lines and slash omitted |
| Masked title edit, initial | gpt-image-2.5-sunburst | xhigh | 33.11 | Unrequested black title background |
| Masked title edit, refined | gpt-image-2.5-sunburst | xhigh | 33.06 | White background/title corrected; outside-mask pixels not identical |
| Transparent microscope | gpt-image-2.5-flare | high | 20.98 | Alpha output and composition verified |
| Transparent microscope, refined | gpt-image-2.5-flare | xhigh | 19.20 | Alpha output and composition verified |
| Two-reference edit, initial | gpt-image-2.5-flare-2026-09-08 | high | 19.27 | OCR found traditional Chinese variants; font also changed |
| Two-reference edit, refined | gpt-image-2.5-flare-2026-09-08 | high | 23.78 | Explicit simplified Chinese strings preserved; visual/OCR check passed |

Native generation and a reference-image title edit both returned usable 1672×941 images. The
edit's 1536×864 source dimensions were not retained. Native elapsed time and model identity were
not reported, so these calls do not verify native Image 2.5 selection or exact size control.

Gemini returned a valid 1376×768 image using `google_imagen`, `gemini-3-pro-image` and Vertex.
The successful repeat took 51.88 seconds. The first call returned an SDK image but the test
harness incorrectly invoked PIL's `load()` on it and failed to save the result. The repeat used
the project's existing `save_image` conversion. This was a harness correction; no Gemini
provider implementation, route, authentication or default was changed.

The strict Critic path reviewed the first Flare slide via `gemini-3.1-flash-lite` on Vertex in
7.41 seconds. It returned 10/10 with no suggestions. This is one automated opinion about one
artifact, not human/scientific acceptance or a score for all outputs.

## Lessons retained in the adapter guide

1. The account's model list did not include Image 2.5, while requests to both aliases and the
   dated Flare model succeeded. Do not reject a model solely because it is absent from that list.
2. Masked editing needed explicit white background, dark-blue font and preservation constraints.
   After refinement, about 6.37% of outside-mask pixels still had a maximum RGB channel difference
   above 8/255 (mean absolute RGB difference 1.65/255). The result was visually checked, not pixel-exact.
3. Multiple-reference prompts needed a declared source for layout, text and font, plus the exact
   simplified Chinese strings. OCR and visual checks caught and confirmed the correction.
4. Both transparent images had alpha values from 0 to 254. About 80.62% and 78.48% of pixels,
   respectively, were fully transparent; neither had alpha-255 pixels. Alpha-aware composition
   showed usable transparency. An initial halo concern from the raw preview was withdrawn after
   checking the composed output. This does not establish binary alpha or fully opaque regions.
5. Preserve initial failures alongside successful refinements. Better prompts on these samples
   do not establish a general quality improvement or a model ranking.

Original outputs, prompts, mask/reference hashes, request sidecars, OCR records and composed
previews were retained in the operator's local test report. Images and account request IDs are
not included in this public summary. Billing cost remains unknown without billing evidence.
The full holdout evaluation, quality pass rates and price/performance comparisons remain unrun.
