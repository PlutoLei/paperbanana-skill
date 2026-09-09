# Image route validation — 2026-09-09

Scope: skill/router changes, optional-backend integration, packaging and existing PPTX modes.
No native image generation or paid API evaluation was executed for this engineering check.

| Check | Observed result |
| --- | --- |
| `node --test plugins/paperbanana/tests/*.test.mjs` | 14 passed |
| `bun test tests/*.test.ts` in slide-deck plugin | 6 passed |
| `python3 -m unittest discover -s tests -p 'test_*.py'` in slide-deck plugin | 1 passed |
| Root/packaged skill, routing guide copies and plugin versions | Checked by packaging tests |
| SKILL frontmatter, manifest JSON and whitespace | Passed |

The route tests cover native arguments, local/conversation references, missing/mixed inputs,
exact-model/strict-control selection, unavailable native tools and Gemini-bound requests.
Existing Gemini routes are resolved before native fallback. The PPTX tests verify actual OOXML
objects for editable decks and a full-slide image plus notes for the legacy image mode.

The matching backend change is on `PlutoLei/paperbanana:codex/image25-adapter`; its validation
record documents 171 passing targeted tests plus 3 optional MCP skips, and a separate compatibility
copy with the user's pending Gemini/Vertex source patch: 173 passing plus the same 3 skips.
Those pending Gemini changes were not committed by this work.

This evidence does not establish model access, native model identity, real image quality, API
latency, billing cost or scientific acceptance. The 24-case evaluation is a prepared protocol;
editing assets and a paid execution budget still need to be supplied for a real evaluation.
