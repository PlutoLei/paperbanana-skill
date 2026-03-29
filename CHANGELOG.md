# Changelog

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
