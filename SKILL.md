---
name: paperbanana
description: Generate and revise academic figures, data plots, or image slides through a configured PaperBanana backend; inspect their automated review status.
argument-hint: "[generate|plot|slide|slide-batch|evaluate|data|setup] [description or file path]"
---

# PaperBanana repository entrypoint

Read the [complete PaperBanana skill](plugins/paperbanana/skills/paperbanana/SKILL.md)
before acting. Its references resolve relative to that skill's directory.

This entrypoint preserves repository-root installs. For a smaller standalone
installation, install `plugins/paperbanana/skills/paperbanana` directly.
Full deck creation uses the separate [deck bundle](plugins/paperbanana-slide-deck/SKILL.md).
