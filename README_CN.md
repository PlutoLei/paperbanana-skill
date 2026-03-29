# PaperBanana — Claude Code 学术插图技能集

<p align="center">
  <a href="https://github.com/PlutoLei/paperbanana-skill/stargazers"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/PlutoLei/paperbanana-skill?style=flat-square&color=yellow" /></a>
  <img alt="Version" src="https://img.shields.io/badge/version-4.1.0-blue?style=flat-square" />
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Skills-2B6CB0?style=flat-square" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="Providers" src="https://img.shields.io/badge/Providers-5-green?style=flat-square" />
  <img alt="Eval" src="https://img.shields.io/badge/Eval-6%E9%A1%B9%E8%B4%A8%E9%87%8F%E6%A3%80%E6%9F%A5-orange?style=flat-square" />
  <a href="https://github.com/PlutoLei/paperbanana-skill/blob/master/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-black?style=flat-square" /></a>
</p>

<p align="center">
  <strong>一句话输入，论文级学术插图输出。</strong><br/>
  5 智能体流水线自动规划、美化、生成、自我审查你的学术图表。
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>中文</strong>
</p>

---

## 效果展示

<table>
<tr>
<td align="center"><strong>生物 — 信号通路</strong><br/><img src="examples/bio_signaling_pathway.png" width="400"/></td>
<td align="center"><strong>NLP — RAG 管线</strong><br/><img src="examples/nlp_rag_pipeline.png" width="400"/></td>
</tr>
<tr>
<td align="center"><strong>数据工程 — 湖仓架构</strong><br/><img src="examples/data_lakehouse.png" width="400"/></td>
<td align="center"><strong>医学 AI — U-Net + Mamba</strong><br/><img src="examples/unet_mamba_segmentation.png" width="400"/></td>
</tr>
</table>

<p align="center"><em>所有图均由纯文本描述生成，零人工绘制。</em></p>

<details>
<summary><strong>更多示例</strong>（架构图、幻灯片）</summary>
<br/>
<table>
<tr>
<td align="center"><strong>Transformer 架构</strong><br/><img src="examples/transformer_architecture.png" width="380"/></td>
<td align="center"><strong>Mamba 状态空间模型</strong><br/><img src="examples/mamba_architecture.png" width="380"/></td>
</tr>
<tr>
<td align="center" colspan="2"><strong>RAG 管线</strong><br/><img src="examples/rag_pipeline.png" width="760"/></td>
</tr>
</table>
</details>

---

## 技能清单

| 技能 | 作用域 | 描述 | 版本 |
|------|--------|------|------|
| **paperbanana** | 用户级 | 学术插图、统计图表、幻灯片生成与质量评估 | v4.0.0 |
| **paperbanana-slide-deck** | 项目级 | 完整 PPT 编排器（RDIV 工作流）+ 150+ 风格预设 | v1.1.0 |

## 功能矩阵

| 功能 | 状态 | 说明 |
|------|------|------|
| 方法论插图 | ✅ | 文本 → 论文级插图，30 秒 |
| 统计图表 | ✅ | CSV/JSON → 自动美化学术图表 |
| 演示幻灯片 | ✅ | Markdown → 4K 幻灯片，150+ 种风格 |
| 多会议风格 | ✅ **新** | `--venue neurips\|icml\|acl\|ieee\|custom` |
| PDF 输入 | ✅ **新** | `--input paper.pdf --pages 3-5` |
| 6 项质量评估 | ✅ **新** | 完整性、布局、标注、配色、可读性、幻觉 |
| 自研优化循环 | ✅ **新** | Autoresearch 自动 prompt 变异 + 保留/回滚 |
| 错误处理 | ✅ **新** | Critic UNREVIEWED 状态 + provider fallback + 重试过滤 |
| 5 大 VLM 提供商 | ✅ | Gemini、Claude、OpenAI、Bedrock、OpenRouter |
| 自动精炼 | ✅ | `--auto` 循环直到 Critic 满意 |
| 运行恢复 | ✅ | `--continue` + `--feedback` 迭代式精炼 |

---

## v4.0 新增功能

### 评估优先的质量体系

6 项二值检查清单，无需参考图即可量化学术插图质量：

| 检查项 | 问题 | 通过标准 |
|--------|------|---------|
| 完整性 | 所有输入概念都有体现？ | 每个关键概念对应一个视觉元素 |
| 布局 | 逻辑流向清晰？ | 明确的 L→R / T→B / 放射状布局 |
| 标注 | 所有组件都有标签？ | 每个视觉元素有文字说明 |
| 配色克制 | ≤3 种主色？ | 学术级配色纪律 |
| 可读性 | 50% 缩放仍可读？ | 文字在论文双栏排版下依然清晰 |
| 无幻觉 | 零未提及概念？ | 图中不出现输入文本外的内容 |

**基线：76% → 100%**，配色克制从 33% 提升至 100%。

### Autoresearch 自优化循环

```
变异 prompt → 生成图片 → 检查清单评估 → 保留或回滚 → 重复
```

### 多会议学术风格

```bash
/paperbanana generate method.txt "架构概览" --venue neurips
```

内置 NeurIPS、ICML、ACL、IEEE 风格指南。

---

## 快速开始

```bash
# 1. 安装 PaperBanana
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana && pip install -e ".[google]"

# 2. 添加技能市场并安装
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills

# 3. 生成第一张图
# /paperbanana 一个带有批量归一化的 4 层 CNN 图像分类架构
```

> **提示：** 本仓库是 Claude Code 的**技能定义文件**（SKILL.md）。Python 核心包在 [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana)，两者都需安装。

---

## 提供商支持

| 提供商 | VLM | 图像生成 | 配置 |
|--------|-----|---------|------|
| Google Gemini | Flash / Pro | Imagen 3 | `GOOGLE_API_KEY` |
| Anthropic Claude | Claude 4 | — | `ANTHROPIC_API_KEY` |
| OpenAI | GPT-4o | DALL-E 3 | `OPENAI_API_KEY` |
| AWS Bedrock | Claude / Nova | Nova Canvas | AWS 凭证 |
| OpenRouter | 多种模型 | 多种模型 | `OPENROUTER_API_KEY` |

---

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| "API key not found" | 运行 `setup` 或检查 paperbanana 目录下的 `.env` |
| 生成失败 | 确认提供商支持图像生成（Claude VLM 不支持） |
| 输出标记为 UNREVIEWED | Critic 无法评估 — 请人工审查该图 |
| Windows 编码错误 | 升级 PaperBanana（`git pull`） |

## 贡献

欢迎贡献！详见 [贡献指南](CONTRIBUTING.md)。

## 许可证

MIT
