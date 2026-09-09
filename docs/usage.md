# Commands and troubleshooting

[Home](../README.md) · [中文说明](#中文说明) · [Install](getting-started.md) · [Providers](providers.md)

The skill translates requests into the selected backend's commands. Verify the actual CLI with `python -m paperbanana.cli --help` and `<command> --help`; an upstream/PyPI installation may differ from the maintained fork. The [skill reference](../plugins/paperbanana/skills/paperbanana/SKILL.md) contains the wider command surface.

| Task | Skill request / command |
| --- | --- |
| Methodology figure | Ask paperbanana to draw your method from its description |
| Plot from real data | Ask paperbanana to plot your CSV/JSON and preserve the supplied values |
| One image slide | `slide` in a backend that exposes that command |
| Multiple image slides | `slide-batch`; use `--concurrent` only if the chosen backend exposes it |
| Refine an existing run | `--continue` and `--feedback` where supported |
| Compare with a reference | `evaluate` |
| Configure access | `setup` |
| Inspect environment | `doctor` |

## Local PowerPoint renderer

From `plugins/paperbanana-slide-deck`, after `bun install --frozen-lockfile`:

```bash
bun scripts/build-deck.ts --mode editable ../../examples/editable-demo \
  --output ../../examples/editable-demo/editable-demo.pptx
```

For image mode, use `--mode image` with a directory containing the expected numbered slide images. For editable mode, a validated `slide-spec.json` is required. Image slides remain pictures; native text/table/chart/shape/line elements remain individually editable. [Full object contract](../plugins/paperbanana-slide-deck/references/editable-slide-spec.md).

## When something fails

| Symptom | Next step |
| --- | --- |
| Missing credentials | Check the selected provider's existing environment or use its setup flow; redact credentials from reports |
| Unknown image provider | Use the `_imagen` factory name, such as `google_imagen` or `openai_imagen` |
| Missing CLI command/flag | Inspect that checkout's help; check whether the feature needs the maintained fork or a preview branch |
| Skill cannot find scripts/styles | Install the complete skill/plugin bundle, not just one Markdown file |
| Critic failed or output is `UNREVIEWED` | Keep the image, report the failed review and inspect it manually |
| Request timed out | Preserve the request/output record and check whether the service completed it before resubmitting |
| Editable build rejects the spec | Fix the reported missing field, bounds, source note or asset hash; do not silently switch to image mode |

Retry/fallback behavior belongs to the installed backend and route. Do not stack shell retries or switch provider merely to make a failed command appear successful. [Image 2.5 preview recovery](https://github.com/PlutoLei/paperbanana-skill/blob/codex/image25-adapter/references/image-routing.md#failure-recovery-and-response) has a separate contract.

## 中文说明

先核对当前后端的 `--help`，再使用命令或参数。`slide`、`slide-batch` 和并发能力取决于安装版本；技能文档不能替代实际 CLI 的支持情况。

图像提供商使用带 `_imagen` 后缀的名称。找不到脚本或风格文件时，检查是否只复制了 `SKILL.md`。Critic 失败时保留产出并说明“未评审”，不要据此声称通过。超时则先查原请求状态，避免重复提交。

原生 PPTX 构建可运行上方命令。`editable` 模式要求完整源规范，校验失败后应修正源文件；`image` 模式生成的整页图片不会因此变成可编辑文本或图表。
