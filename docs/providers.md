# Runtimes, providers and routing

[Home](../README.md) · [中文说明](#中文说明) · [Installation](getting-started.md)

## Separate the three roles

| Role | Examples | Responsibility |
| --- | --- | --- |
| Agent runtime | Claude Code, Codex | Reads the skills, interprets the task and calls available tools |
| Image provider | Gemini through `google_imagen`, OpenAI through `openai_imagen` | Produces images through the configured backend |
| Planning / review VLM | Configured Gemini, Anthropic, OpenAI or another supported VLM integration | Plans content or reviews images; it may not generate images |

The Python backend also contains Bedrock/OpenRouter image integrations and additional VLM integrations, including LiteLLM and Ollama. Availability depends on the installed backend and account configuration. A count of VLM backends is not a count of image generators; an Ollama or Claude VLM entry alone does not make it an image backend.

For CLI image-provider flags, use the factory names `google_imagen`, `openai_imagen`, `bedrock_imagen` or `openrouter_imagen`. Short VLM names such as `gemini` and `openai` belong to `--vlm-provider`. Consult the selected command's `--help` before copying flags between versions.

## Keep existing Gemini and Vertex workflows

An explicit provider choice remains part of the task. Keep saved model/provider choices and their API-key or Vertex configuration; do not reinterpret a Gemini request as an OpenAI request because Codex is the host.

The released skills use the configured Python pipeline or their documented provider integrations. Existing Vertex users need a backend that already supports Vertex authentication; this repository's documentation does not migrate that configuration. Pick currently available model IDs from your deployed backend rather than copying old model names from a screenshot.

## Image 2.5 preview

The Image 2.5 adapter is a separate feature branch, **not part of the v4.5 release**:

- [Skill branch and routing guide](https://github.com/PlutoLei/paperbanana-skill/blob/codex/image25-adapter/references/image-routing.md)
- [Optional Python backend branch](https://github.com/PlutoLei/paperbanana/tree/codex/image25-adapter)
- [Live integration smoke report, 2026-09-09](https://github.com/PlutoLei/paperbanana-skill/blob/codex/image25-adapter/docs/image25-live-smoke.md)

On that branch, new Codex image requests with no chosen/existing backend can use the available native image tool. Exact API model selection, quality, dimensions, transparency or mask controls use the explicit API backend. Existing Gemini selections are resolved before native fallback. Editable PPTX rendering remains local.

The native Codex tool does not expose an exact image-model selector in the verified schema. Its output cannot be labeled Flare/Sunburst merely because the tool succeeded. The API branch explicitly supports the requested Image 2.5 models; requested model and reported model are separate fields.

Keep the skill and core feature versions aligned when evaluating the preview. Use its own guide rather than assuming the default installation commands select it. Merging or installing a preview is a separate change from reading these docs.

## 中文说明

Claude Code 和 Codex 是承载技能的运行环境；Gemini、OpenAI 等提供具体模型能力。生图模型与规划、评审所用的 VLM 可以不同，因此“支持某个 VLM”不能直接写成“可以用它生图”。

已有 Gemini 或 Vertex 任务继续使用原后端、模型和认证配置。尤其不要因为任务运行在 Codex 中，就把它改送 OpenAI。Vertex 是否可用取决于已安装后端的支持情况；文档整理不迁移认证，也不替旧版本补装适配。

CLI 的图像提供商名称带 `_imagen` 后缀，例如 `google_imagen`、`openai_imagen`；VLM 的名称则是 `gemini`、`openai` 等。具体命令仍以当前后端的帮助信息为准。

Image 2.5 与 Codex 原生路由属于上方链接中的预览分支，目前不包含在 v4.5 正式版。该分支允许未绑定后端的新 Codex 请求使用原生工具；需要精确模型、尺寸、质量或遮罩控制时，使用 API 后端。原生工具未报告模型名称时，不能自行标注为 Flare 或 Sunburst。
