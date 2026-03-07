# PaperBanana — Claude Code 学术插图技能集

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-3.1.0-orange?style=flat-square" />
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Skills-2B6CB0?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="Providers" src="https://img.shields.io/badge/Providers-5-green?style=flat-square" />
  <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-black?style=flat-square" />
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>中文</strong>
</p>

## 本仓库包含的技能

| 技能 | 作用域 | 描述 | 版本 |
|------|--------|------|------|
| **paperbanana** | 用户级 | 学术插图、统计图表、演示幻灯片生成 | v3.1.0 |
| **paperbanana-slide-deck** | 项目级 | 完整 PPT 编排器（RDIV 工作流） | v1.0.0 |

## 效果展示

### 学术插图生成

<table>
<tr>
<td align="center"><strong>Transformer 架构图</strong><br/><img src="examples/transformer_architecture.png" width="400"/></td>
<td align="center"><strong>CNN 分类网络</strong><br/><img src="examples/cnn_architecture.png" width="400"/></td>
</tr>
<tr>
<td align="center" colspan="2"><strong>RAG 流水线</strong><br/><img src="examples/rag_pipeline.png" width="800"/></td>
</tr>
</table>

> 以上图片均由 PaperBanana 根据纯文本描述自动生成，无需手动绘图。

## 快速上手

```bash
# 1. 安装 PaperBanana
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana && pip install -e ".[google]"

# 2. 添加技能市场并安装
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project  # 可选

# 3. 生成你的第一张图
# /paperbanana 一个 4 层 CNN 加 batch normalization 的图像分类网络
```

一句话输入，出版级插图输出。底层由五智能体流水线驱动——自动规划、配色、生成、自我评审，全程无需人工干预。

> **注意：** 本仓库包含 Claude Code **技能定义**（SKILL.md 文件）。底层 Python 包位于 [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana)——需同时安装技能和 Python 包。

## 为什么选择 PaperBanana？

| 痛点 | 传统做法 | PaperBanana |
|------|---------|-------------|
| 绘制方法论示意图 | PowerPoint / TikZ 手绘数小时 | 一句话描述，30 秒出图 |
| 制作统计图表 | matplotlib 模板代码 + 反复调样式 | 描述意图，自动排版配色 |
| 保持风格一致 | 逐图手动调整 | Critic 智能体统一执行风格规范 |
| 制作演示幻灯片 | 从零设计每一页 | Markdown 提示词 → 精美幻灯片 |

## v3.1 新特性

- **5 大 VLM/图像生成服务商** — Gemini、Claude、OpenAI、Bedrock、OpenRouter 任选
- **输入优化** — `--optimize` 自动扩充上下文、锐化标题，提升生成质量
- **自动精修** — `--auto` 让 Critic 循环评审直到满意为止
- **断点续跑** — `--continue` + `--feedback` 在上次输出基础上迭代改进
- **动态宽高比** — 支持 8 种 Imagen 比例，Planner 自动推荐最优构图
- **幻灯片生成** — `slide` 和 `slide-batch` 命令，Critic 循环打磨演示页面
- **引导式配置** — `setup` 命令交互式完成 API 密钥设置
- **数据集管理** — `data` 命令一键下载/查看/清理参考数据集
- **范例检索增强** — `--exemplar-retrieval` 在规划前引入相似案例
- **PPT 编排器** — `paperbanana-slide-deck` 技能，端到端 RDIV 工作流（内容→风格→大纲→批量生成→PPTX）
- **插件市场** — 支持现代 `claude plugin` 安装方式

## 流水线架构

<p align="center">
  <img src="examples/pipeline_architecture.png" width="800" alt="PaperBanana 多智能体流水线"/>
</p>

流水线以迭代方式运行：评审器对每次生成结果进行评估，合格即输出，不合格则附带修改意见回传给规划器重新生成。

### PPT 编排器（paperbanana-slide-deck）

<p align="center">
  <img src="examples/slide_deck_workflow.png" width="800" alt="Slide Deck RDIV 工作流"/>
</p>

PPT 编排器通过 RDIV 四阶段流程完成端到端演示文稿制作：内容分析、23 种视觉风格选择、大纲与提示词生成、4K 批量图片生成、PPTX/PDF 合并输出。

## 命令速查

| 命令 | 用途 | 示例 |
|------|------|------|
| `generate` | 方法论示意图 | `/paperbanana 稀疏注意力 Transformer 架构` |
| `plot` | 统计图表 | `/paperbanana plot results.csv 各模型准确率对比柱状图` |
| `slide` | 演示幻灯片 | `/paperbanana slide prompt.md` |
| `slide-batch` | 批量幻灯片 | `/paperbanana slide-batch prompts/` |
| `evaluate` | 对比评估 | `/paperbanana evaluate gen.png ref.png` |
| `data` | 数据集管理 | `/paperbanana data download` |
| `setup` | 引导式配置 | `/paperbanana setup` |

### 带优化的生成

```bash
/paperbanana generate method.txt "所提出框架的总体架构" --optimize --auto
```

### 从 CSV 生成统计图

```bash
/paperbanana plot results.csv "四种模型 F1 分数对比柱状图" --optimize
```

### 生成演示幻灯片

```bash
/paperbanana slide presentation/slide_03.md --resolution 4k --iterations 5
```

### 在上次结果基础上继续迭代

```bash
/paperbanana generate --continue --feedback "箭头加粗，增加颜色编码"
```

<details>
<summary><strong>更多示例</strong></summary>

```bash
# 指定服务商
/paperbanana generate method.txt "流水线概览" --vlm-provider anthropic --image-provider google_imagen

# 试运行（不调用 API）
/paperbanana generate method.txt "架构图" --dry-run

# 自定义宽高比
/paperbanana generate method.txt "宽幅流水线图" --aspect-ratio 16:9

# 批量生成全部幻灯片
/paperbanana slide-batch prompts/ --resolution 2k --iterations 3

# 详细输出的对比评估
/paperbanana evaluate gen.png ref.png --context paper.txt --caption "Figure 1" --verbose
```

</details>

## 服务商支持

| 服务商 | VLM | 图像生成 | 配置方式 |
|--------|-----|---------|---------|
| Google Gemini | Flash / Pro | Imagen 3 | `.env` 中设置 `GOOGLE_API_KEY` |
| Anthropic Claude | Claude 4 | 不适用（仅 VLM） | `.env` 中设置 `ANTHROPIC_API_KEY` |
| OpenAI | GPT-4o | DALL-E 3 | `.env` 中设置 `OPENAI_API_KEY` |
| AWS Bedrock | Claude / Nova | Nova Canvas | 配置 AWS 凭证 |
| OpenRouter | 多种模型 | 多种模型 | `.env` 中设置 `OPENROUTER_API_KEY` |

通过 `--vlm-provider` 和 `--image-provider` 按命令选择服务商。

## 安装

### 方式 A：插件市场安装（推荐）

```bash
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project  # 可选
```

### 方式 B：手动安装

```bash
# paperbanana 技能（用户级）
mkdir -p ~/.claude/skills/paperbanana
curl -o ~/.claude/skills/paperbanana/SKILL.md \
  https://raw.githubusercontent.com/PlutoLei/paperbanana-skill/master/plugins/paperbanana/skills/paperbanana/SKILL.md

# paperbanana-slide-deck 技能（项目级，可选）
mkdir -p .claude/skills/paperbanana-slide-deck
curl -o .claude/skills/paperbanana-slide-deck/SKILL.md \
  https://raw.githubusercontent.com/PlutoLei/paperbanana-skill/master/plugins/paperbanana-slide-deck/skills/paperbanana-slide-deck/SKILL.md
```

### PaperBanana 环境配置

```bash
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana
pip install -e ".[google]"          # Gemini（默认）
# pip install -e ".[anthropic]"     # + Claude
# pip install -e ".[openai]"        # + OpenAI / DALL-E
# pip install -e ".[bedrock]"       # + AWS Bedrock
# pip install -e ".[all]"           # 全部服务商
```

运行引导式配置：

```bash
python -m paperbanana.cli setup
```

或手动在 paperbanana 目录下创建 `.env` 文件：

```
GOOGLE_API_KEY=你的密钥
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| "API key not found" | 确认 `.env` 文件位于 paperbanana 项目目录下 |
| "Image generation failed" | 确认所选服务商支持图像生成（Claude VLM 仅支持视觉理解，不支持图像生成） |
| "Critic JSON parse error" | 升级到最新版 PaperBanana，4 层 fallback 已修复此问题 |
| Windows 中文乱码 | 升级 PaperBanana（`git pull`），已修复 Unicode 兼容性 |

## 许可证

MIT
