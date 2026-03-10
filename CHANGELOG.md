# Changelog

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
