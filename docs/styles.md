# Style libraries

[Home](../README.md) · [中文说明](#中文说明) · [Deck skill](../plugins/paperbanana-slide-deck/skills/paperbanana-slide-deck/SKILL.md)

There are three different style sources, not three competing counts of the same bundle:

| Source | Included here? | How to use it |
| --- | --- | --- |
| [123 structured style references](../plugins/paperbanana-slide-deck/references/styles) | Yes | The deck skill reads palettes, typography and layout guidance from these files |
| Python backend slide presets | In the backend | The released skill documents 23 named presets; check your backend before passing `--style` |
| Optional external skill libraries | No | Discover only when separately installed; availability and overlap vary |

The older “150+” description combined local and optional libraries. It is not a guaranteed installed count. Some references describe related aesthetics with different names; do not count them as independently validated output modes.

Start with a style suited to the content: a restrained scientific treatment for dense diagrams, or consistent typography and palette for a presentation. Use the same source, style and layout rules throughout a deck.

The bundled references were introduced in [v4.1](../CHANGELOG.md#410---2026-03-29), curated from Fooocus/ComfyUI-style presets. Optional sources mentioned by the skill include baoyu-slide-deck, baoyu-infographic and theme-factory; those packages are separate dependencies and retain their own attribution and licenses.

## 中文说明

仓库实际包含 **123 份结构化风格参考**，可在上方目录逐项查看。旧文案中的“23 种”指 Python 后端预设，“150+”则把可选的外部技能库也算了进去，不能当作每次安装都自带的数量。

做科学图时先保证关系和标注清楚，再选配色与字体；做整套幻灯片时固定同一风格来源和排版规则。使用后端的 `--style` 前，确认该版本确实支持相应名称。外部风格库是否可用，以本机实际安装情况为准。
