# Changelog

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
