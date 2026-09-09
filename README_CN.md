# PaperBanana Skills

**让你的智能体生成学术插图，编排幻灯片，交付可编辑的 PowerPoint。**

[![最新版本](https://img.shields.io/github/v/release/PlutoLei/paperbanana-skill?style=flat-square)](https://github.com/PlutoLei/paperbanana-skill/releases)
[![持续集成](https://github.com/PlutoLei/paperbanana-skill/actions/workflows/validate.yml/badge.svg?branch=master)](https://github.com/PlutoLei/paperbanana-skill/actions/workflows/validate.yml)
[![MIT 许可证](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

[English](README.md) · **中文**

[快速开始](#快速开始) · [精选案例](#精选案例) · [文档导航](#文档导航)

把方法描述变成插图，让整套演示保持一致风格，或生成能继续修改的 PowerPoint 对象。在 Claude Code 或 Codex 中使用技能，按任务选择所需的生图后端。

[![TextMamba3D 学术架构图：影像与文本双分支、特征融合及分割解码器](examples/previews/textmamba3d_architecture.webp)](examples/textmamba3d_architecture.png)

*历史案例，原 README 记录使用 GPT Image 2。点击查看原图。[更多案例与来源说明](docs/gallery.md)。*

## 快速开始

### 1. 安装技能

**Codex**：通过技能安装器安装。

```bash
npx skills add PlutoLei/paperbanana-skill -a codex
```

**Claude Code**：通过插件市场安装。

```bash
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
```

需要整套演示编排时，再安装 `paperbanana-slide-deck@paperbanana-skills`，并指定 `--scope project`。[完整安装步骤与手动安装 →](docs/getting-started.md#中文说明)

### 2. 选择你要的产出

| 你的任务 | 从这里开始 |
| --- | --- |
| 生成插图或图片式幻灯片 | 配置 [Python 后端](docs/getting-started.md#python-后端)，选择生图与评审所用的提供商 |
| 生成可编辑的 PowerPoint | 运行[本地 PPTX 示例](examples/editable-demo/README.md#中文说明)；渲染需要 Bun，不调用生图 API |
| 继续使用 Gemini / Vertex | 沿用已有后端和认证配置，参见[提供商说明](docs/providers.md#中文说明) |

### 3. 直接描述任务

向智能体发送：

> 用 paperbanana 和 Gemini 画一个带批量归一化的四层 CNN，标清输入、卷积模块和分类器，返回图片及其评审状态。

在 Claude Code 中也可以用 `/paperbanana` 调用。已有提供商偏好时，请在请求中直接说明。[更多起步提示词 →](docs/prompts.md)

**预览功能：** Codex 原生生图路由与 Image 2.5 精确控制位于 [`codex/image25-adapter`](https://github.com/PlutoLei/paperbanana-skill/tree/codex/image25-adapter)，尚未进入当前 v4.5 正式版。[预览分支与真实调用记录](docs/providers.md#image-25-preview)单独说明了它们的使用条件。

## 精选案例

<table>
<tr>
<td width="50%" valign="top"><strong>学术插图</strong><br/><a href="examples/game_theory_influence_diagram.png"><img src="examples/previews/game_theory_influence_diagram.webp" width="400" alt="博弈论影响图，以柔和配色区分决策节点与依赖关系"/></a><br/>Gemini · <a href="docs/prompts.md#scientific-figure">起步提示词</a></td>
<td width="50%" valign="top"><strong>科研演示</strong><br/><a href="examples/slide_scrna_workflow.png"><img src="examples/previews/slide_scrna_workflow.webp" width="400" alt="展示单细胞 RNA 测序分析流程的科研幻灯片"/></a><br/>图片式幻灯片 · <a href="docs/prompts.md#research-slide">起步提示词</a></td>
</tr>
<tr>
<td width="50%" valign="top"><strong>成套幻灯片</strong><br/><a href="examples/slide_flywheel_04_model.png"><img src="examples/previews/slide_flywheel_04_model.webp" width="400" alt="飞轮学习法的核心模型，沿用整套演示的暖纸色与手绘笔记风格"/></a><br/><a href="docs/gallery.md#slide-deck">查看整组</a> · <a href="docs/prompts.md#consistent-deck">起步提示词</a></td>
<td width="50%" valign="top"><strong>可编辑 PowerPoint</strong><br/><a href="examples/editable-demo/editable-demo.pptx"><img src="examples/previews/editable-demo.webp" width="400" alt="由原生 PowerPoint 文本、形状、连接线、表格与演示图表构成的幻灯片"/></a><br/><a href="examples/editable-demo/editable-demo.pptx">下载 PPTX</a> · <a href="examples/editable-demo/slide-spec.json">查看源文件</a></td>
</tr>
</table>

前三项是保留的历史产出；PPTX 是可在本地重建的演示示例，数值仅用于展示编辑能力。起步提示词是新编写的任务模板，并非历史生成时的原始输入。[完整图库与来源说明 →](docs/gallery.md)

## 工作方式

- **`paperbanana`** 负责理解插图、图表和幻灯片需求，调用已配置的 Python 流水线完成检索、规划、风格设计、生图和 Critic 评审。
- **`paperbanana-slide-deck`** 负责整套演示的内容与风格编排。开始时明确选择图片模式或原生可编辑 PPTX 模式。
- **[Python 后端](https://github.com/PlutoLei/paperbanana)** 提供模型接入与生成、评审流程；本地可编辑 PPTX 渲染器则直接包含在技能仓库中。

运行环境、生图提供商、评审提供商各有分工。接入了某个 VLM，并不代表它也能生成图片。[提供商、运行环境与路由 →](docs/providers.md#中文说明)

## 验证与限制

CI 检查技能文件、插件清单和 PPTX 渲染器。[可编辑示例](examples/editable-demo/README.md#中文说明)同时提供源文件和实际生成的原生对象。用于论文前，仍须核对标签、箭头、数值和科学表述；Critic 的自动评分不能替代科学审查。

生成结果可能出现文字或结构错误，评审失败时应明确标记为**未评审**。历史对比和最近的冒烟测试不代表通用模型排名，也不能承诺固定耗时或费用。[证据与质量检查 →](docs/evaluation.md#中文说明)

## 文档导航

| 文档 | 用途 |
| --- | --- |
| [安装与上手](docs/getting-started.md#中文说明) | 安装技能、配置后端、生成首个结果 |
| [完整图库](docs/gallery.md) · [起步提示词](docs/prompts.md) | 查看原图、了解来源、改写自己的任务 |
| [提供商说明](docs/providers.md#中文说明) | Claude Code / Codex、Gemini / Vertex、OpenAI 与预览功能 |
| [风格库](docs/styles.md#中文说明) | 随仓库提供的风格、可选来源与后端预设 |
| [可编辑 PPTX](examples/editable-demo/README.md#中文说明) · [对象规范](plugins/paperbanana-slide-deck/references/editable-slide-spec.md) | 构建和修改原生 PowerPoint 对象 |
| [命令与排障](docs/usage.md#中文说明) | 常用命令、故障恢复与评审状态 |
| [评测说明](docs/evaluation.md#中文说明) | 证据、质量检查及局限 |
| [更新日志](CHANGELOG.md) · [正式版本](https://github.com/PlutoLei/paperbanana-skill/releases) | 查询版本变化 |

当前正式版组件：技能市场 **4.5.0**、`paperbanana` 插件 **4.4.0**、`paperbanana-slide-deck` 插件 **1.3.0**。三者分别维护版本号。

## 贡献与致谢

参与前请阅读[贡献指南](CONTRIBUTING.md)和[行为准则](CODE_OF_CONDUCT.md)。报告问题时，请附运行环境、提供商与模型名称，以及可复现步骤。

本项目基于 [PaperBanana](https://github.com/llmsresearch/paperbanana)，附加集成由[维护版 Python 后端](https://github.com/PlutoLei/paperbanana)提供。风格来源见[风格库说明](docs/styles.md)。

[MIT 许可证](LICENSE) · 维护者：[雷宇轩 / Lei Yuxuan](https://github.com/PlutoLei)。
