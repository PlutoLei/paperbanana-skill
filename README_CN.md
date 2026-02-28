# PaperBanana — Claude Code 学术插图技能

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-2.1.0-orange?style=flat-square" />
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Skill-2B6CB0?style=flat-square" />
  <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-black?style=flat-square" />
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>中文</strong>
</p>

面向 [Claude Code](https://claude.ai/claude-code) 的学术插图生成技能，集成 [PaperBanana](https://github.com/llmsresearch/paperbanana) 多智能体框架，一句话生成出版级方法图、架构图和统计图。

## 功能一览

在 Claude Code 中输入 `/paperbanana` 即可：

- **生成方法图** — 架构图、流程图、系统设计图
- **创建统计图** — 柱状图、折线图、散点图（支持 CSV/JSON）
- **基准测试** — 运行 PaperBananaBench 评估套件
- **风格润色** — 对已有图片进行学术风格精修
- **对比评估** — 将生成图与人工参考图对比打分

五智能体流水线驱动：检索器 → 规划器 → 风格师 → 可视化器 → 评审器。

## v2.1 新特性

- **自动 VLM 选择** — `--vlm-model auto`（默认），根据输入复杂度自动选 Flash（快速）或 Pro（高质量）
- **6 种流水线模式** — `vanilla`、`planner`、`planner_stylist`、`planner_critic`、`full`、`polish`
- **`bench` 命令** — 直接在 Claude Code 中运行 PaperBananaBench 评估
- **`polish` 命令** — 对已有图片进行风格指南润色
- **Critic JSON 鲁棒解析** — 四层 fallback：json.loads → json-repair → regex → 安全默认值

## 使用示例

```
/paperbanana 我们的模型使用 4 层 CNN 加 batch normalization 进行图像分类

/paperbanana generate method.txt 所提出框架的总体架构

/paperbanana plot results.csv 各模型准确率对比柱状图

/paperbanana bench data/PaperBananaBench/ --task diagram --max-samples 5

/paperbanana polish output.png --task diagram
```

## 示例产出

**稀疏注意力 Transformer：**

![Transformer Architecture](https://github.com/PlutoLei/paperbanana-skill/raw/master/examples/transformer_architecture.png)

**CNN 图像分类：**

![CNN Architecture](https://github.com/PlutoLei/paperbanana-skill/raw/master/examples/cnn_architecture.png)

## 安装

### 1. 安装 PaperBanana

```bash
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana
pip install -e ".[google]"
```

### 2. 配置 API 密钥

前往 https://aistudio.google.com/apikey 获取 Google Gemini API 密钥。

在 paperbanana 目录下创建 `.env` 文件：

```
GOOGLE_API_KEY=你的密钥
```

### 3. 安装技能

**方式 A：CLI 安装**

```bash
claude install-skill PlutoLei/paperbanana-skill
```

**方式 B：手动安装**

```bash
mkdir -p ~/.claude/skills/paperbanana
cp SKILL.md ~/.claude/skills/paperbanana/
```

### 4. 开始使用

```
/paperbanana <描述或命令>
```

## 命令速查

| 命令 | 示例 | 说明 |
|------|------|------|
| `generate` | `/paperbanana <文字描述>` | 根据描述生成方法图 |
| `generate`（文件） | `/paperbanana generate file.txt 标题` | 从文本文件生成 |
| `plot` | `/paperbanana plot data.csv 意图` | 生成统计图表 |
| `bench` | `/paperbanana bench dataset/ --task diagram` | 运行 PaperBananaBench |
| `polish` | `/paperbanana polish image.png` | 风格润色 |
| `evaluate` | `/paperbanana evaluate gen.png ref.png` | 对比评估 |

## 流水线模式

| 模式 | 流水线 | 评审器 |
|------|--------|--------|
| `vanilla` | 直接生成 | 无 |
| `planner` | 检索器 → 规划器 → 可视化器 | 无 |
| `planner_stylist` | + 风格师 | 无 |
| `planner_critic` | + 评审循环 | 有 |
| `full` | 全流水线（默认） | 有 |
| `polish` | 风格润色 | 无 |

## 环境要求

- 已安装 [PaperBanana](https://github.com/llmsresearch/paperbanana)
- Google Gemini API 密钥
- Python 3.10+

## 许可证

MIT
