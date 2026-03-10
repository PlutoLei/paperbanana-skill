# Contributing to PaperBanana Skills

Thank you for your interest in contributing! This guide covers how to report issues, suggest features, and submit changes.

## Reporting Bugs

1. Check [existing issues](https://github.com/PlutoLei/paperbanana-skill/issues) to avoid duplicates
2. Open a new issue using the **Bug Report** template
3. Include: steps to reproduce, expected vs actual behavior, and your environment

## Suggesting Features

Open an issue using the **Feature Request** template. Describe the problem you're trying to solve and your proposed solution.

## Submitting Changes

### Setup

```bash
# Fork and clone the repository
git clone https://github.com/<your-username>/paperbanana-skill.git
cd paperbanana-skill

# Create a feature branch
git checkout -b feat/your-feature
```

### Making Changes

- **Skill definitions** live in `plugins/<skill-name>/skills/<skill-name>/SKILL.md`
- **Top-level SKILL.md** is the legacy single-skill definition
- **Examples** go in `examples/` (keep images under 1MB each)

### Skill Development Guidelines

When modifying or creating SKILL.md files:

- Keep the file under 500 lines (split into `references/` subdirectory if needed)
- Include a clear `name`, `description`, and trigger conditions
- Document all commands with examples
- Test the skill locally with `claude` before submitting

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new diagram style support
fix: correct aspect ratio calculation
docs: update installation instructions
```

### Pull Request Process

1. Ensure your branch is up to date with `master`
2. Fill out the PR template completely
3. Link any related issues
4. Wait for review — maintainers will respond within a few days

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold these standards.

## Questions?

Open a [discussion](https://github.com/PlutoLei/paperbanana-skill/issues) or reach out to the maintainers.
