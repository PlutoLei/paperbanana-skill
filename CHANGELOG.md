# Changelog

## [4.4.0] - 2026-08-03

### Added
- **Wave-parallel batch generation** — new `slide-batch --concurrent N` section in SKILL.md: per-slide pipeline isolation, 5s start-up stagger (same-second image-API bursts fail or hang server-side long before per-minute quotas), in-batch delayed retry for transient 503s, end-of-batch serial retry pass. Measured: 6 slides at `--concurrent 3` in 309s vs 768s serial estimate (0.40x, ~2.5x speedup) with zero dropped slides.
- **Auto-routing decision table** — provider selection rules in SKILL.md: explicit user override > venue-rigor > CJK-slide / multi-reference hard rules (documented Gemini bugs) > East-Asian aesthetics > Gemini default.
- **Provider naming warning** — `--image-provider` requires the `X_imagen` suffix (`google_imagen`, not `gemini`); documented the trap with its exact error signature.

### Changed
- **Delivery-quality notes** — the final image per slide is now the highest-critic-score iteration rather than simply the last one, and `critic_score_threshold=9.0` skips provably-done rounds early (calibrated on 69 historical runs, zero false early-stops).

### Notes
- The `--concurrent` flag, argmax delivery, and threshold early-stop require a paperbanana build ≥ 2026-08-03 (maintainer's fork). On older builds, `slide-batch` remains serial; SKILL.md documents the fallback and warns against uncoordinated multi-process spawning.

## [4.3.0] - 2026-04-23

### Added
- **GPT Image 2 native support** — `gpt-image-2` (released 2026-04-21) is now a first-class model in the OpenAI image provider. Detection is prefix-based (`model.startswith("gpt-image-2")`).
- **Expanded output sizes** — gpt-image-2 unlocks `2048x1152` (true 16:9), `1536x1536` (large square), `1792x1024`, and `1152x2048` alongside the legacy sizes that gpt-image-1.5 / gpt-image-1 / DALL-E 3 already use.
- **Quality tier parameter** — `quality=low|medium|high` is sent automatically for gpt-image-2 (omitted for legacy models since those reject it).
- **Full aspect-ratio coverage for gpt-image-2** — `supported_ratios` now reports 8 ratios (all of paperbanana's Imagen set) when the active model is gpt-image-2. Legacy models still advertise only `1:1`, `3:2`, `2:3`.
- **Smart provider routing table** in both SKILL.md files — decides `openai` vs `gemini` per scenario, with hard rules to avoid two documented Gemini bugs (duplicate-character Chinese titles on slides; hallucinated content on multi-reference composition). Explicit user intent (`用 GPT` / `用 Gemini` / `两路并行`) always overrides the auto-rules.
- **Before/after comparison gallery** in README — three prompt pairs showing Gemini's Chinese-text bug, GPT's semantic fidelity on diffusion diagrams, and Gemini's strength on traditional calligraphy. Backs up the routing table with evidence from a controlled 16-prompt test.

### Changed
- **paperbanana SKILL.md** — Replaced the static "Provider Selection" table with a full "Provider Selection & Routing" section: provider capability matrix + decision table + explicit-override rule + standalone `image-router` CLI pointer for ad-hoc quick-image needs.
- **paperbanana-slide-deck SKILL.md** — New Phase P (Provider Picking) runs before Phase R/D/I and records the choice in `provider.txt`. Phase I1 now branches on `provider.txt` to pass the correct `--image-provider` / `--image-model` flags to `slide-batch`; both providers benefit from the Path A Critic loop.
- **Critic loop coverage** — OpenAI branch previously bypassed the critic (going through the raw adapter). Both branches now go through the full RDIV pipeline so quality gating applies regardless of provider.

### Fixed
- **Legacy models unaffected** — gpt-image-1 / gpt-image-1.5 / DALL-E 3 retain their original 1024/1536 sizing and receive no `quality=` parameter. 17 new TDD tests verify the legacy path stays intact.

### Notes
- Routing calibrated from `image-model-comparison/results/2026-04-22_gemini-only/summary.html` (LLM-as-judge + user-corrected aesthetic judgments over 16 prompts × 2 providers).
- Local paperbanana fork commit: `c82928a` on branch `feat/gpt-image-2-support` (`tests/test_providers/test_openai_imagen.py` — 17 new tests, all green).
- Standalone `image-router` CLI lives at `image-model-comparison/src/cli.py` for ad-hoc image generation without the Critic overhead.

## [4.2.0] - 2026-04-14

### Changed
- **paperbanana SKILL.md** — Added Command Selection Decision Tree (subcommand routing table with ambiguous-input fallback and out-of-scope clause).
- **paperbanana SKILL.md** — Added User Confirmation Checkpoints section (explicit guards for `--auto`, `--auto-download-data`, `setup`).
- **paperbanana SKILL.md** — After Generation now proactively suggests `--continue --feedback` on UNREVIEWED or user dissatisfaction.
- **paperbanana-slide-deck SKILL.md** — Auto-degrade trigger now fires on any slide (not just first), with four explicit conditions including user-reported rate-limit persistence.
- **paperbanana-slide-deck SKILL.md** — Distinguish Critic-429 vs Image-gen-429 with separate response strategies.
- **paperbanana-slide-deck SKILL.md** — I2 Smart Cleanup now documents sequencing (I1 → I2 → I3) to prevent deletion of in-progress batch PNGs.

### Fixed
- **paperbanana-slide-deck Path B code** — Added `try/except` with exponential backoff (`sleep(30 * 2**retry)` capped at 5 min, `MAX_RETRIES=5`) and partial-batch skip (resume from first missing PNG instead of regenerating all).
- **paperbanana-slide-deck Fallback table** — Expanded from 1 to 3 rows covering Critic-429, Image-gen-429, and partial-batch scenarios.

### Notes
- Improvements derived from `darwin-skill` evaluation loop (8-dimension rubric + sub-agent verification).
- Composite scores: paperbanana 71.4 → 83.7 (+12.3); paperbanana-slide-deck 82.0 → 86.5 (+4.5).
- **Upstream awareness**: `llmsresearch/paperbanana` merged 8 PRs on 2026-04-07 not yet incorporated into this skill doc. Three touch points are marked with upstream Notes in SKILL.md: `--auto-download-data` dataset size (upstream #112 curated), Path B partial-batch vs upstream `batch_checkpoint.json` (#129), and new subcommands `plot-batch`/`sweep` + `claude_code` provider (#123/#118/#115). A future skill release will document these.
- Manifest version alignment: `marketplace.json` metadata.version was still at `4.0.0` despite the 4.1.0 CHANGELOG entry — bumped directly to `4.2.0` to reconcile.

## [4.1.0] - 2026-03-29

### Added
- **123 structured style presets** — Curated from Fooocus SDXL (277 styles), enriched with color palettes, typography, visual elements, and style rules. Located in `plugins/paperbanana-slide-deck/references/styles/`.
- **Multi-source style discovery** — Slide deck skill now scans 4 sources: built-in library (123), baoyu-slide-deck (16), baoyu-infographic (20), and theme-factory (10). Total 150+ styles with automatic deduplication.
- **10 style categories** — Art Movement, Classic & Design, Craft & Technique, Commercial, Photography, Futuristic, Papercraft, Atmospheric, Core Digital, Versatile.

### Changed
- **paperbanana-slide-deck** upgraded to v1.1.0 — R1 step now discovers styles from 4 sources instead of 1.
- Feature Matrix updated: 23 presets → 150+ presets.

## [4.0.0] - 2026-03-28

### Added
- **6-item binary quality checklist** — Automated evaluation for completeness, layout, annotation, color restraint, legibility, and hallucination detection. VLM-based absolute assessment without reference images.
- **Autoresearch self-optimization loop** — Karpathy-style prompt mutation with keep/revert, versioned snapshots, and JSONL changelog. Targets weakest checklist dimension automatically.
- **Multi-venue academic styles** — `--venue neurips|icml|acl|ieee|custom` with built-in style guides per venue.
- **PDF input support** — `--input paper.pdf --pages 3-5` extracts methodology text directly from papers.
- **Error handling documentation** — SKILL.md now specifies API failure classification, provider fallback chains, UNREVIEWED status for Critic failures, and batch resilience.
- **Progress streaming** — Pipeline progress callbacks for CLI and MCP (merged from upstream).
- **Prompt A/B comparison harness** — Side-by-side evaluation of prompt variants (merged from upstream).
- **New gallery images** — Bio signaling pathway, NLP RAG pipeline, data lakehouse, U-Net+Mamba segmentation.

### Fixed
- **Critic silent approval bug** — Malformed VLM responses no longer silently pass quality gate; output marked UNREVIEWED instead.
- **Plot code security** — AST-based import blocklist prevents os, subprocess, socket in VLM-generated code.
- **Provider retry filtering** — Auth errors (4xx) no longer trigger futile retries; only transient errors (429, 5xx) retry.
- **Color restraint** — Planner, Stylist, and Critic prompts enforce ≤3 primary color rule (baseline 33% → 100%).

### Changed
- **Upstream sync** — Merged 41 commits from llmsresearch/paperbanana (progress callbacks, PDF input, venue styles, Studio UI, benchmark harness).
- Version badge updated to v4.0.0 with new Eval badge.
- README redesigned with ABC hybrid layout (academic + feature matrix + visual gallery).

## [3.2.1] - 2026-03-11

### Changed
- **Performance optimization** — Default CLI commands now use `--config configs/fast.yaml --auto` for faster generation
  - Planner+Stylist merged (skip one VLM call, ~15s saved)
  - Critic score threshold early exit (score >= 8.0 skips remaining iterations)
  - Slide generation: ~50% faster (high first-pass quality, 1 iteration typical)
  - Diagram generation: ~30% faster (2 iterations vs 3 with score-based early exit)

## [3.2.0] - 2026-03-11

### Added
- **Community health files** — CODE_OF_CONDUCT.md, CONTRIBUTING.md, issue/PR templates
- **CI workflow** — GitHub Actions validation for SKILL.md, plugin manifests, and image sizes
- **Dynamic badges** — GitHub Stars counter and clickable License badge

### Changed
- **Optimized example images** — Total size reduced from 34.6 MB to 3.72 MB (89% reduction)
- Updated version badges to v3.2.0 in both README.md and README_CN.md
- Added Contributing section to both READMEs

## [3.1.0] - 2026-03-07

### Added
- **Plugin marketplace structure** — Supports `claude plugin marketplace add` for modern installation
- **paperbanana-slide-deck skill** (v1.0.0) — End-to-end slide deck creation via RDIV workflow
  - Content analysis and style recommendation (23 presets)
  - Interactive style/audience/slide count selection
  - Outline and prompt generation with 20 layout types
  - Batch image generation via PaperBanana CLI
  - PPTX/PDF merge via baoyu-slide-deck scripts
  - Selective regeneration and iterative refinement
- MIT LICENSE file

### Changed
- Updated paperbanana skill SKILL.md to v3.1.0 (added `ablate-retrieval` and `data` commands)
- Restructured repository as plugin marketplace with two plugins

## [3.0.0] - 2026-02-27

### Added
- 5 VLM/Image providers (Gemini, Claude, OpenAI, Bedrock, OpenRouter)
- Input optimization (`--optimize`)
- Auto-refine mode (`--auto`)
- Run continuation (`--continue` + `--feedback`)
- Dynamic aspect ratio (8 Imagen ratios)
- Slide generation (`slide` and `slide-batch` commands)
- Setup wizard (`setup` command)
- Dataset manager (`data` command)
- Exemplar retrieval (`--exemplar-retrieval`)
