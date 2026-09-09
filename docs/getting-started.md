# Installation and first output

[Home](../README.md) · [中文说明](#中文说明) · [Providers](providers.md) · [Local PPTX demo](../examples/editable-demo/README.md)

## Install for your runtime

For Codex, install from the repository with the skills installer:

```bash
npx skills add PlutoLei/paperbanana-skill -a codex
```

For Claude Code, add the marketplace and choose the plugins you need:

```bash
claude plugin marketplace add PlutoLei/paperbanana-skill
claude plugin install paperbanana@paperbanana-skills
claude plugin install paperbanana-slide-deck@paperbanana-skills --scope project
```

The deck plugin is optional. Reload skills in your runtime after installation. Installing a skill does not configure API access or install its Python backend. Check which skills the installer selected; runtime discovery and plugin installation are different mechanisms.

## Python backend

Use the maintained fork for the pipeline and image-slide features described here. Run this in a directory where you want a new checkout; existing users can keep their configured environment.

```bash
git clone https://github.com/PlutoLei/paperbanana.git
cd paperbanana
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[google]'
python -m paperbanana.cli --help
python -m paperbanana.cli setup
```

On Windows, activate `.venv\Scripts\Activate.ps1` in PowerShell instead. Configure credentials through your own environment/setup process; never include them in prompts or issues. Gemini users can keep their existing Google configuration. Vertex users should retain their Vertex-capable backend and authentication settings; installing this skill does not add Vertex support to an older backend.

For OpenAI image generation, install the backend's OpenAI extra with `python -m pip install -e '.[openai]'`, configure your OpenAI access, and retain a suitable VLM provider for pipeline planning/review. See [provider roles](providers.md). Check the chosen checkout's `--help`; features can differ between the maintained fork, upstream and PyPI versions.

The standalone editable PPTX renderer uses Bun and the dependencies in this repository. It can run without the Python backend or image credentials. [Build the included example](../examples/editable-demo/README.md).

## First figure

Once the backend is configured, ask your agent to use `paperbanana` and describe the figure. For example:

> Use paperbanana with Gemini to draw a four-layer CNN with batch normalization. Label the input, convolution blocks and classifier. Use a white background and a restrained palette. Return the image and its review status.

The agent should identify the configured backend and preserve an explicit provider choice. The generated image and the Critic result are separate outputs: inspect the actual figure even when automated review succeeds. [More recipes](prompts.md).

## Manual installation

Copy the complete skill bundle, including referenced files and scripts. Downloading only a `SKILL.md` can leave the deck skill without its renderer or styles. Use fresh destination directories or reconcile an existing installation before copying; nested copies and stale files can shadow an update. For an existing repository checkout, a Codex example is:

```bash
# Run from the paperbanana-skill repository root.
SKILLS_DEST="$HOME/.codex/skills"
mkdir -p "$SKILLS_DEST"
cp -R plugins/paperbanana/skills/paperbanana "$SKILLS_DEST/paperbanana"
cp -R plugins/paperbanana-slide-deck "$SKILLS_DEST/paperbanana-slide-deck"
cp plugins/paperbanana-slide-deck/skills/paperbanana-slide-deck/SKILL.md \
  "$SKILLS_DEST/paperbanana-slide-deck/SKILL.md"
```

Other runtimes use their own skill directory. This example does not install a Claude plugin or migrate another runtime's settings.

## 中文说明

先选择运行环境，再配置任务真正需要的后端。Codex 可使用上面的 `npx skills add ... -a codex`；Claude Code 则使用插件市场命令。只做插图时安装 `paperbanana` 即可，需要整套演示编排再加装 `paperbanana-slide-deck`。

安装完成后刷新技能列表，并核对实际安装了哪些技能。技能安装器、Claude 插件市场与 Python 包是三个独立环节。

### Python 后端

插图和图片式幻灯片流水线使用[维护版 Python 仓库](https://github.com/PlutoLei/paperbanana)。首次使用可按本页上半部分创建虚拟环境、安装所选提供商的依赖并运行 `setup`。已有环境可继续使用，不必为了改版重新克隆或迁移配置。

使用 Gemini 时保留现有 Google 认证方式；使用 Vertex 时，继续使用已支持 Vertex 的后端版本和配置。技能安装本身不会给旧后端补上 Vertex 接口。OpenAI 生图需要对应依赖和访问配置，流水线的规划、评审还需要可用的 VLM。

只构建原生可编辑 PPTX 时，可以直接运行仓库内的 [Bun 示例](../examples/editable-demo/README.md#中文说明)，无需 Python 生图后端或图片 API 密钥。

### 第一个任务

> 用 paperbanana 和 Gemini 画一个带批量归一化的四层 CNN。标清输入、卷积模块和分类器，使用白底和克制配色，返回图片及评审状态。

手动安装时应复制完整目录，保留技能引用的脚本与风格文件。覆盖旧安装前先核对目录层级，避免把新文件嵌套进旧技能目录。[更多命令与排障](usage.md#中文说明)。
