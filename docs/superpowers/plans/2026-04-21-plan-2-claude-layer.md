# Plan 2 — Claude Code layer (retrospective)

> **Status:** implemented in the same session as Plan 1. This document is retrospective — it describes the plan as executed, for methodological consistency. Future plans should be written before execution.

**Goal:** Produce the Claude Code operating layer of the starter — slash commands, shared skill, project-level `CLAUDE.md`, full README with Security + Lighthouse sections, and i18n directory dictionary.

**Architecture:** Skill `.claude/skills/starter-setup/SKILL.md` holds shared logic (brand loading, CSP mutation rules, sitemap maintenance, components catalog upkeep, env-var discipline). Ten slash commands under `.claude/commands/` invoke the skill and provide per-task wizards. `CLAUDE.md` at repo root auto-loads the non-negotiable rules into every Claude session.

## Files created

- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/i18n-dirs.json`
- `.claude/skills/starter-setup/SKILL.md`
- `.claude/commands/start-new-site.md`
- `.claude/commands/adopt-existing-site.md`
- `.claude/commands/new-page.md`
- `.claude/commands/new-section.md`
- `.claude/commands/brand-setup.md`
- `.claude/commands/new-blog-article.md`
- `.claude/commands/deploy.md`
- `.claude/commands/audit-brand.md`
- `.claude/commands/setup-integration.md`
- `.claude/commands/setup-staging-auth.md`
- `README.md` (rewritten in full)
- `_template-page.html` (generic page template referenced by `/new-page`)

## Files removed

- `CONTRIBUTING.md` — intent moved into the Usage section of the README, aligned with the "fork freely, not monitored" positioning.

## Verification checklist

- [x] Every slash command `.md` file has YAML frontmatter with `description`.
- [x] Skill `SKILL.md` uses the superpowers frontmatter format (`name`, `description`).
- [x] `CLAUDE.md` covers token rules, tone rules, secrets, staging discipline, clean URLs, image rules, CSP coherence.
- [x] `.claude/settings.json` allow-list is scoped narrowly (no `Bash(rm:*)`, no broad `WebFetch(*)`).
- [x] README includes: install one-liner, brand-first disclaimer, Claude Max recommendation, Security section, Lighthouse workflow, example site, usage / forking positioning, MIT license.
- [x] i18n-dirs.json covers fr/es/de/it/pt as a working dictionary for `/start-new-site` language renames.
