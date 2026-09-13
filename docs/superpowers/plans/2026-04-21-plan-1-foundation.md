# Plan 1 — Foundation & Static Skeleton

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a deployable static site skeleton for `claude-site-starter` — directory structure, design tokens, placeholder HTML pages, modular CSS, hardened `.htaccess`, staging protection, and GitHub Actions SFTP workflows. At the end of this plan, pushing to `staging` deploys a password-protected staging site, and pushing to `main` deploys a production site.

**Architecture:** Pure HTML + CSS + JS vanilla. No build step. Opinionated directory layout. Security hardened by default (`.htaccess` with HSTS, strict CSP, anti-clickjacking headers, clean URLs, cache, compression). Staging protected by `.htpasswd` with `noindex` enforcement. Deploy via `lftp` over SFTP triggered by GitHub Actions on push to `staging` or `main`.

**Tech Stack:** HTML5, CSS3 (no preprocessor), vanilla JS, Apache `.htaccess`, `lftp`, GitHub Actions, `htpasswd` (from `httpd-tools` / `apache2-utils`).

**Reference spec:** `docs/superpowers/specs/2026-04-21-claude-site-starter-design.md`

**Working directory:** `/Users/ADMIN/claude-projets/jessem/claude-site-starter/`

---

## File Structure (Plan 1 scope)

Files **created** in Plan 1:

- Root: `.gitignore`, `.env.example`, `LICENSE`, `README.md` (minimal, full version in Plan 2), `CONTRIBUTING.md`, `SETUP.md` (skeleton), `.htaccess`, `.htaccess-staging`, `index.html`, `404.html`, `robots.txt`, `robots-staging.txt`, `sitemap.xml`, `site.webmanifest`, `logo-principal.svg`
- `.github/workflows/deploy-staging.yml`, `.github/workflows/deploy-production.yml`
- `assets/css/tokens.css`, `assets/css/main.css`, `assets/css/home.css`, `assets/css/blog.css`, `assets/css/projects.css`, `assets/css/legal.css`, `assets/css/404.css`, `assets/css/cookie-consent.css`
- `assets/js/shared.js`, `assets/js/cookie-consent.js`
- `assets/fonts/README.md`, `assets/photos/README.md`, `assets/icons/README.md`, `assets/illustrations-blog/README.md`
- `about/index.html`, `projects/index.html`, `projects/_template-project.html`, `blog/index.html`, `blog/_template-article.html`
- `legal/privacy/index.html`, `legal/terms/index.html`, `legal/cookies/index.html`
- `api/_env.php`, `api/webhook.php.example`
- `docs/README.md`, `docs/brand/brand.md`, `docs/brand/tone-of-voice.md`, `docs/brand/illustration-prompt.md`, `docs/brand/toolbelt.md`, `docs/components.md`, `docs/inspirations/README.md`, `docs/content/README.md`, `docs/drafts/README.md`
- `scripts/htpasswd-gen.sh`, `scripts/optimize-image.sh`

Files **already present** from Plan 0 (spec writing):
- `docs/superpowers/specs/2026-04-21-claude-site-starter-design.md`
- `docs/superpowers/plans/2026-04-21-plan-1-foundation.md` (this file)

**Not in scope for Plan 1:**
- `.claude/` (commands and skills — Plan 2)
- `api/brevo.php.example` (module — Plan 4)
- `scripts/generate-image.py`, `scripts/generate-podcast.py`, `scripts/sitemap-update.py` (Plan 3)
- Full `README.md` (Plan 2 once commands exist)

---

## Phase 1 — Repository bootstrap (Tasks 1-3)

### Task 1: Initialize git repository

**Files:** none to create in this step, but working directory needs init.

- [ ] **Step 1: Initialize git**

```bash
cd /Users/ADMIN/claude-projets/jessem/claude-site-starter
git init -b main
```

Expected: `Initialized empty Git repository in .../claude-site-starter/.git/`

- [ ] **Step 2: Verify**

```bash
git status
```

Expected: `On branch main / No commits yet / Untracked files: docs/`

### Task 2: Create `.gitignore`

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Write `.gitignore`**

```
# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Env
.env
.env.local
.env.*.local

# Node (optional tooling)
node_modules/

# Internal docs not deployed (except public PDFs)
docs/
!docs/*.pdf
!docs/superpowers/
!docs/superpowers/**
!docs/brand/
!docs/brand/**
!docs/components.md
!docs/README.md

# Superpowers ephemeral brainstorm state
.superpowers/

# Staging artifacts generated locally
.htpasswd
```

Note: `docs/` is git-ignored by default for deployment purposes, but `docs/superpowers/` (specs, plans) and `docs/brand/` (source of truth) are whitelisted so they remain in git. Only things like `docs/inspirations/`, `docs/content/`, `docs/drafts/`, `docs/migration/` stay out of git unless the user adds them explicitly.

- [ ] **Step 2: Verify**

```bash
cat .gitignore | head -20
```

Expected: content matches.

### Task 3: Create `.env.example`

**Files:**
- Create: `.env.example`

- [ ] **Step 1: Write `.env.example`**

```
# ===============================================
# SITE
# ===============================================
SITE_URL=https://example.com
STAGING_URL=https://staging.example.com

# ===============================================
# GEMINI (illustrations + podcast) — required if
# modules "illustrations" or "podcast" are enabled
# Plan 3 uses these.
# ===============================================
GEMINI_API_KEY=

# ===============================================
# BREVO (CRM / forms) — required if module "brevo"
# is enabled. Plan 4 uses these.
# ===============================================
BREVO_API_KEY=
BREVO_LIST_DEFAULT=

# ===============================================
# CAL.COM (booking) — public values, no secret
# ===============================================
CAL_USERNAME=
CAL_EVENT_SLUG=15min

# ===============================================
# ANALYTICS — public values, no secret
# ===============================================
GA4_MEASUREMENT_ID=
PLAUSIBLE_DOMAIN=
UMAMI_WEBSITE_ID=

# ===============================================
# STAGING BASIC AUTH — generated by
# scripts/htpasswd-gen.sh. Stored also in your
# password manager. Never commit the generated
# .htpasswd file.
# ===============================================
STAGING_HTPASSWD_USER=
STAGING_HTPASSWD_PASS=

# ===============================================
# SFTP — set via GitHub Actions secrets, NOT in
# this file. Listed for reference only:
#   OVH_HOST
#   OVH_USERNAME
#   OVH_PASSWORD
#   OVH_PROD_DIR
#   OVH_STAGING_DIR
# ===============================================
```

- [ ] **Step 2: Verify**

```bash
wc -l .env.example
```

Expected: ~45 lines.

---

## Phase 2 — Documentation scaffolding (Tasks 4-10)

### Task 4: Create `LICENSE`

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: Write MIT license**

```
MIT License

Copyright (c) 2026 Jessy Martin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Task 5: Create minimal `README.md`

Full README comes in Plan 2 once commands are defined. Plan 1 ships a stub that already carries the brand-first disclaimer and points to `SETUP.md`.

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write stub `README.md`**

````markdown
# claude-site-starter

An opinionated, CMS-free, Claude Code-native starter for marketing websites.

> **Status:** early bootstrap. Full documentation and slash commands land in subsequent plans. See `SETUP.md` for the current manual setup path and `docs/superpowers/specs/` for the design.

## Philosophy

- **Static-first.** HTML + CSS + JS vanilla. No framework, no bundler, no build.
- **Brand-first.** This starter does not produce a beautiful site on its own. A qualitative result requires a defined brand universe: typography, colors, logo, photos, copy, editorial voice. Invest time there first.
- **Claude Code-native.** Slash commands, skills, and conventions designed for a human + Claude pair.
- **Deploy via SFTP.** Any shared PHP 8+ host works.

## Requirements

- SFTP host with PHP 8+
- GitHub account
- Claude Code installed (Claude Max plan recommended for sustained use)
- Optional API keys: Gemini (illustrations + podcast), Brevo, Cal.com

## Example

A site built with this methodology: https://jessem.fr

## License

MIT — see `LICENSE`.
````

### Task 6: Create `CONTRIBUTING.md` stub

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Write stub**

```markdown
# Contributing

Thanks for considering a contribution.

## Adding a module

A module is a self-contained folder under `modules/<name>/` with:
- `README.md` — purpose, options, dependencies
- Templates (HTML / CSS / JS / PHP `*.example` if needed)
- `install.md` — step-by-step of what the setup wizard does when activating the module

## Testing changes

Before opening a PR, run the module through `/start-new-site` on a fresh directory and confirm it installs, deploys to a staging URL, and passes `/audit-brand`.

## Commit style

Short imperative subject (`add`, `fix`, `refactor`), reference the module or phase in the body when relevant.
```

### Task 7: Create `SETUP.md` skeleton

**Files:**
- Create: `SETUP.md`

- [ ] **Step 1: Write skeleton**

```markdown
# Manual setup (fallback without Claude Code)

This document mirrors what the `/start-new-site` slash command does, for users who prefer to configure manually or want to understand the moving parts.

## Prerequisites

- Git + GitHub CLI (`gh`) logged in.
- Node not required. Python 3 required for scripts in Plan 3.
- SFTP credentials for your host.
- Apache with `mod_rewrite`, `mod_headers`, `mod_deflate`, `mod_expires`, `mod_mime` enabled (standard on any shared PHP host).

## Step 1 — Clone

    gh repo create <your-site> --template <this-repo> --public --clone
    cd <your-site>

## Step 2 — Brand

Fill `docs/brand/brand.md` and `docs/brand/tone-of-voice.md`. Replace CSS tokens in `assets/css/tokens.css` with your palette and fonts.

## Step 3 — SFTP secrets

Set GitHub Actions secrets:

    gh secret set OVH_HOST --body "sftp.host.example"
    gh secret set OVH_USERNAME --body "..."
    gh secret set OVH_PASSWORD --body "..."
    gh secret set OVH_PROD_DIR --body "/www/"
    gh secret set OVH_STAGING_DIR --body "/staging/"

## Step 4 — Staging auth

    bash scripts/htpasswd-gen.sh

Follow the prompts. Save credentials in your password manager.

## Step 5 — First deploy

    git checkout -b staging
    git push -u origin staging

Watch the workflow: `gh run watch`.

## Step 6 — Production

When staging is validated:

    git checkout main
    git merge staging
    git push origin main

## Step 7 — Server-side `.env`

SSH or SFTP into your host and create a `.env` at the site root with the same keys as `.env.example`, filled in. This is used by PHP endpoints (Plan 4).

More details in the design spec: `docs/superpowers/specs/2026-04-21-claude-site-starter-design.md`.
```

### Task 8: Create `docs/README.md` and brand doc templates

**Files:**
- Create: `docs/README.md`
- Create: `docs/brand/brand.md`
- Create: `docs/brand/tone-of-voice.md`
- Create: `docs/brand/illustration-prompt.md`
- Create: `docs/brand/toolbelt.md`
- Create: `docs/components.md`
- Create: `docs/inspirations/README.md`
- Create: `docs/content/README.md`
- Create: `docs/drafts/README.md`

- [ ] **Step 1: Write `docs/README.md`**

```markdown
# docs/

Internal documentation. Not deployed to production (GitHub Actions workflow strips this folder before SFTP upload, except `docs/**/*.pdf` which are whitelisted).

## Structure

- `brand/` — source of truth for the brand. Claude reads `brand.md` at the start of every working session.
- `components.md` — catalog of reusable HTML/CSS components. Auto-updated by `/new-page` and `/new-section`.
- `inspirations/` — moodboard images (gitignored by default).
- `content/` — raw texts, briefs, transcripts (gitignored).
- `drafts/` — draft ideas (gitignored).
- `superpowers/specs/` — design documents per feature. Kept in git.
- `superpowers/plans/` — implementation plans per feature. Kept in git.
- `migration/` — dump of a CMS site being migrated (gitignored, created by `/adopt-existing-site` in CMS scenario).
```

- [ ] **Step 2: Write `docs/brand/brand.md` template**

```markdown
# Brand

> Source of truth. Claude reads this at the start of every session. Keep it short, decisive, and up to date.

## Identity

- **Name:** <Your brand name>
- **Tagline:** <one line>
- **Positioning:** <one sentence — who you serve and what you do>

## Palette

| Token | Hex | Role |
|---|---|---|
| `--midnight` | `#0D1B2A` | Background primary |
| `--off-white` | `#FAFAFA` | Text on dark |
| `--accent` | `#F9DC5C` | Accent / highlights / CTAs |
| `--soft-blue` | `#7C98B3` | Secondary text |
| `--deep-blue` | `#1B4965` | Alt background |

Keep the palette small (5-7 tokens). Every hex in the site should map to a token. No ad-hoc colors.

## Typography

- **Display:** <font name> — used for emphasized script/italic words, never for body.
- **Body:** <font name> — sans-serif, weights 300-800.

Where to get them:
- Display: local WOFF2 in `assets/fonts/` (preload in `<head>`).
- Body: Google Fonts (preconnect + preload).

## Logo

- Full logo: `logo-principal.svg`
- Minimum size: 40px.
- Clear space: equivalent to the height of the "o" around the mark.

## Photography

- Style: <describe — e.g., natural light, warm tones, documentary>.
- Sources: <e.g., own shoots + curated Unsplash>.
- Retouch: <policies>.

## Iconography

- Style: <outline / filled / duotone / custom>.
- Library: <e.g., Lucide 1.8, pinned>.

## Do / Don't

- **Do:** <brand-consistent visual move>.
- **Don't:** <off-brand pitfall to avoid>.
```

- [ ] **Step 3: Write `docs/brand/tone-of-voice.md` template**

```markdown
# Tone of voice

## Audience

<Describe who you're talking to. Role, context, goals, pain.>

## Pronouns

- Author: `je` / `I` / `we` — pick one, stay consistent.
- Reader: `vous` / `you`.

## Tone adjectives

Pick 3 to 5 and commit:
1. <adjective>
2. <adjective>
3. <adjective>

## Rules

- **Forbidden:** <e.g., emojis, em-dashes, anglicisms, corporate buzzwords>.
- **Required:** <e.g., statistics are always sourced with a link to the exact page, prices in euros, RGPD mention if AI is involved>.

## Do / Don't examples

- **Do:** "I help marketing teams integrate AI in 8 weeks."
- **Don't:** "We leverage cutting-edge AI to revolutionize your marketing stack 🚀"
```

- [ ] **Step 4: Write `docs/brand/illustration-prompt.md` template**

```markdown
# Illustration prompt — Gemini Image

> This is the prompt template used by `scripts/generate-image.py` (Plan 3). The only placeholder is `{{subject_description}}`, filled automatically per illustration by `/new-blog-article` or `/new-page`.

## Template

```
[Base style adjective, e.g. "elegant hand-drawn sketch"] illustration on a flat [dark|light] background color [primary bg hex from palette]. Thin [warm|cool] brush strokes in [accent hex] and [secondary hex]. {{subject_description}}. Editorial illustration feel. No text, no words. Wide 16:9. Minimal composition.
```

## Guidance for `/brand-setup`

- Pull bg color from `--midnight` (or whichever token is the primary background in `brand.md`).
- Pull accent and secondary from the two other dominant tokens.
- Base style adjective should match the brand's visual character (hand-drawn, flat geometric, collage, photographic, 3D render, etc.).
- Adjust temperature (warm/cool) to the palette.

## Example (filled, for reference only)

```
Elegant hand-drawn sketch style illustration on a flat dark background color #0D1B2A. Thin warm brush strokes in #F9DC5C and #ACCBE1. Two marketers collaborating at a whiteboard with floating UI elements. Editorial illustration feel. No text, no words. Wide 16:9. Minimal composition.
```
```

- [ ] **Step 5: Write `docs/brand/toolbelt.md` template**

```markdown
# Toolbelt

Log of Claude Code tools installed on this project. Updated by the setup wizard and by `/setup-integration`.

## Format

| Tool | Type | Installed | Status | Notes |
|---|---|---|---|---|
| Superpowers | Plugin | YYYY-MM-DD | active | `/plugin install superpowers@claude-plugins-official` |
| UI/UX Pro Max | Skill | YYYY-MM-DD | active | cloned to local skills path |
| 21st.dev | MCP | YYYY-MM-DD | active | `claude mcp add 21st-dev` |

## Pending decisions

<list tools mentioned during setup as "remind me later">
```

- [ ] **Step 6: Write `docs/components.md` skeleton**

```markdown
# Components catalog

Reusable HTML/CSS patterns available in this project. Auto-updated by `/new-page` and `/new-section` when a new pattern is introduced. Keep entries compact — the goal is quick recall for Claude, not a design system book.

## Layout

_None yet. The starter ships with placeholder pages only. Components appear here as they are created._

## Content blocks

_None yet._

## Forms and CTAs

_None yet._

## Blog-specific

See `docs/blog-components.md` once the blog module is active (Plan 3).
```

- [ ] **Step 7: Write `docs/inspirations/README.md`, `docs/content/README.md`, `docs/drafts/README.md`**

Each one line:

`docs/inspirations/README.md`:
```markdown
# Inspirations

Drop reference images (webp, jpg, png) here. Used by `/brand-setup` in "help-me" mode and by Claude for visual context. Gitignored by default.
```

`docs/content/README.md`:
```markdown
# Content

Raw texts, briefs, transcripts, source material. Used by Claude as input for `/new-page`, `/new-blog-article`, `/new-section`. Gitignored by default.
```

`docs/drafts/README.md`:
```markdown
# Drafts

Work-in-progress ideas, outlines, abandoned pages. Not yet promoted to real pages. Gitignored by default.
```

### Task 9: First commit — documentation foundation

- [ ] **Step 1: Stage and commit**

```bash
git add LICENSE README.md CONTRIBUTING.md SETUP.md .gitignore .env.example docs/
git commit -m "chore: bootstrap docs and licensing"
```

Expected: commit succeeds. `git log --oneline` shows one commit.

### Task 10: Verify docs tree

- [ ] **Step 1: Print tree**

```bash
ls -R docs/
```

Expected output (paths):
```
docs/:
README.md  brand  components.md  content  drafts  inspirations  superpowers

docs/brand:
brand.md  illustration-prompt.md  tone-of-voice.md  toolbelt.md

docs/content:
README.md

docs/drafts:
README.md

docs/inspirations:
README.md

docs/superpowers:
plans  specs
```

---

## Phase 3 — Design tokens and base CSS (Tasks 11-15)

### Task 11: Create `assets/css/tokens.css`

**Files:**
- Create: `assets/css/tokens.css`

- [ ] **Step 1: Write tokens**

```css
/* ═══════════════════════════════════════
   DESIGN TOKENS
   Source of truth for every visual value.
   Replace placeholder values in /brand-setup
   or manually, aligned with docs/brand/brand.md.
   ═══════════════════════════════════════ */

:root {
    /* Palette (placeholders — replace per brand) */
    --midnight:      #0D1B2A;
    --deep-blue:     #1B4965;
    --soft-blue:     #7C98B3;
    --light-blue:    #ACCBE1;
    --accent:        #F9DC5C;
    --off-white:     #FAFAFA;
    --cream:         #FDF8E8;

    /* Palette with opacity variants */
    --accent-dim:    rgba(249, 220, 92, 0.12);
    --accent-glow:   rgba(249, 220, 92, 0.25);

    /* Typography */
    --font-display:  'YourDisplayFont', cursive;
    --font-body:     'Plus Jakarta Sans', system-ui, sans-serif;

    --fs-xs:         0.75rem;
    --fs-sm:         0.875rem;
    --fs-base:       1rem;
    --fs-md:         1.125rem;
    --fs-lg:         1.5rem;
    --fs-xl:         2rem;
    --fs-2xl:        clamp(2rem, 4vw, 3.2rem);
    --fs-hero:       clamp(2.5rem, 6vw, 5rem);

    /* Spacing scale */
    --space-xs:      0.5rem;
    --space-sm:      1rem;
    --space-md:      2rem;
    --space-lg:      4rem;
    --space-xl:      6rem;
    --space-2xl:     10rem;

    /* Radii */
    --radius-sm:     4px;
    --radius-md:     8px;
    --radius-lg:     16px;
    --radius-full:   999px;

    /* Container */
    --container-max: 1320px;
    --container-pad: clamp(1.5rem, 4vw, 3rem);

    /* Motion */
    --ease-out:      cubic-bezier(0.16, 1, 0.3, 1);
    --transition:    0.3s var(--ease-out);
}
```

### Task 12: Create `assets/css/main.css`

**Files:**
- Create: `assets/css/main.css`

- [ ] **Step 1: Write reset + utilities + nav + footer base**

```css
/* ═══════════════════════════════════════
   RESET
   ═══════════════════════════════════════ */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; overflow-x: clip; }

body {
    font-family: var(--font-body);
    background: var(--midnight);
    color: var(--off-white);
    font-size: var(--fs-base);
    line-height: 1.6;
    overflow-x: clip;
    -webkit-font-smoothing: antialiased;
}

a { color: inherit; text-decoration: none; }
img { max-width: 100%; display: block; }
button { font-family: inherit; border: none; background: none; color: inherit; cursor: pointer; }

::selection { background: var(--accent); color: var(--midnight); }

/* ═══════════════════════════════════════
   UTILITIES
   ═══════════════════════════════════════ */
.sr-only {
    position: absolute;
    width: 1px; height: 1px;
    padding: 0; margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

.container {
    max-width: var(--container-max);
    margin: 0 auto;
    padding: 0 var(--container-pad);
}

.script { font-family: var(--font-display); }
.accent { color: var(--accent); }
.soft   { color: var(--soft-blue); }

.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s var(--ease-out), transform 0.8s var(--ease-out);
}
.reveal.visible {
    opacity: 1;
    transform: none;
}

/* ═══════════════════════════════════════
   SECTION DEFAULTS
   ═══════════════════════════════════════ */
section { padding: var(--space-xl) 0; overflow: clip; }

.section-number {
    font-size: var(--fs-xs);
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: var(--space-sm);
}

.section-title {
    font-family: var(--font-body);
    font-size: var(--fs-2xl);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.025em;
    max-width: 800px;
}
.section-title em {
    font-family: var(--font-display);
    font-style: normal;
    color: var(--accent);
    font-weight: 400;
    font-size: 1.1em;
}

/* ═══════════════════════════════════════
   NAVIGATION
   ═══════════════════════════════════════ */
nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 100;
    padding: 1.25rem 0;
    transition: padding 0.5s;
}
nav .container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: background 0.5s, backdrop-filter 0.5s, border-radius 0.5s, border 0.5s, padding 0.5s;
}
nav.scrolled .container {
    background: rgba(13, 27, 42, 0.72);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(124, 152, 179, 0.12);
    border-radius: var(--radius-lg);
    padding: 0.6rem 1.25rem;
}
.nav-logo { display: inline-flex; align-items: center; }
.nav-links {
    display: flex;
    gap: 2rem;
    list-style: none;
    align-items: center;
}
.nav-links a { font-size: var(--fs-sm); font-weight: 500; }
.nav-links a:hover { color: var(--accent); }
.nav-cta {
    background: var(--accent);
    color: var(--midnight);
    padding: 0.6rem 1.2rem;
    border-radius: var(--radius-full);
    font-weight: 600;
}
.nav-hamburger {
    display: none;
    flex-direction: column;
    gap: 4px;
    cursor: pointer;
}
.nav-hamburger span {
    width: 24px; height: 2px;
    background: var(--off-white);
    transition: transform 0.3s, opacity 0.3s;
}

@media (max-width: 860px) {
    .nav-links {
        position: fixed;
        top: 0; right: 0; bottom: 0;
        width: min(80vw, 320px);
        background: var(--midnight);
        flex-direction: column;
        justify-content: center;
        transform: translateX(100%);
        transition: transform 0.4s var(--ease-out);
        padding: 2rem;
    }
    .nav-links.open { transform: translateX(0); }
    .nav-hamburger { display: flex; }
}

/* ═══════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════ */
.btn-primary,
.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.9rem 1.5rem;
    border-radius: var(--radius-full);
    font-weight: 600;
    font-size: var(--fs-sm);
    transition: transform var(--transition), background var(--transition);
}
.btn-primary {
    background: var(--accent);
    color: var(--midnight);
}
.btn-primary:hover { transform: translateY(-2px); }
.btn-secondary {
    border: 1px solid rgba(250, 250, 250, 0.2);
    color: var(--off-white);
}
.btn-secondary:hover { border-color: var(--accent); color: var(--accent); }

/* ═══════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════ */
footer {
    padding: var(--space-lg) 0 var(--space-md);
    border-top: 1px solid rgba(124, 152, 179, 0.12);
    color: var(--soft-blue);
    font-size: var(--fs-sm);
}
footer .container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: var(--space-md);
}
footer a:hover { color: var(--accent); }
.footer-links { display: flex; gap: var(--space-sm); list-style: none; flex-wrap: wrap; }

/* ═══════════════════════════════════════
   REDUCED MOTION
   ═══════════════════════════════════════ */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

### Task 13: Create per-page CSS stubs

**Files:**
- Create: `assets/css/home.css`
- Create: `assets/css/blog.css`
- Create: `assets/css/projects.css`
- Create: `assets/css/legal.css`
- Create: `assets/css/404.css`
- Create: `assets/css/cookie-consent.css`

Each file starts with a header comment explaining its scope. Content will grow per page in later plans.

- [ ] **Step 1: Write `home.css`**

```css
/* ═══════════════════════════════════════
   HOME PAGE
   Styles specific to index.html.
   Keep shared patterns in main.css.
   ═══════════════════════════════════════ */

.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding-top: 6rem;
}
.hero-title {
    font-size: var(--fs-hero);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    max-width: 14ch;
}
.hero-desc {
    margin-top: var(--space-sm);
    color: var(--soft-blue);
    max-width: 46ch;
    font-size: var(--fs-md);
}
.hero-actions {
    margin-top: var(--space-md);
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
}
```

- [ ] **Step 2: Write `blog.css`**

```css
/* ═══════════════════════════════════════
   BLOG
   Index (blog/index.html) and article
   (blog/_template-article.html).
   Components documented in docs/components.md
   once Plan 3 runs.
   ═══════════════════════════════════════ */

.blog-hero {
    padding: 8rem 0 var(--space-md);
    text-align: center;
}

.blog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-md);
    margin-top: var(--space-md);
}

.blog-card {
    background: var(--midnight-light, #112240);
    border: 1px solid rgba(124, 152, 179, 0.12);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: transform var(--transition), border-color var(--transition);
}
.blog-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
}
.blog-card img {
    aspect-ratio: 16 / 9;
    object-fit: cover;
    width: 100%;
}
.blog-card-body { padding: var(--space-sm); }
.blog-card-title {
    font-size: var(--fs-md);
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 0.5rem;
}
.blog-card-meta {
    font-size: var(--fs-xs);
    color: var(--soft-blue);
}
```

- [ ] **Step 3: Write `projects.css`**

```css
/* ═══════════════════════════════════════
   PROJECTS
   projects/index.html and projects/_template-project.html
   ═══════════════════════════════════════ */

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: var(--space-md);
    margin-top: var(--space-md);
}

.project-card {
    background: var(--midnight-light, #112240);
    border: 1px solid rgba(124, 152, 179, 0.12);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: transform var(--transition);
}
.project-card:hover { transform: translateY(-4px); }
.project-card img {
    aspect-ratio: 16 / 10;
    object-fit: cover;
    width: 100%;
}
.project-card-body { padding: var(--space-sm); }
```

- [ ] **Step 4: Write `legal.css`**

```css
/* ═══════════════════════════════════════
   LEGAL PAGES
   Privacy, Terms, Cookies.
   ═══════════════════════════════════════ */

.legal-content {
    max-width: 72ch;
    margin: 0 auto;
    padding: 8rem var(--container-pad) var(--space-xl);
}
.legal-content h1 {
    font-size: var(--fs-2xl);
    font-weight: 800;
    margin-bottom: var(--space-md);
}
.legal-content h2 {
    font-size: var(--fs-lg);
    font-weight: 700;
    margin: var(--space-md) 0 var(--space-sm);
}
.legal-content p { margin-bottom: var(--space-sm); }
.legal-content ul { margin-bottom: var(--space-sm); padding-left: 1.5rem; }
.legal-content a { color: var(--accent); border-bottom: 1px solid var(--accent-dim); }
```

- [ ] **Step 5: Write `404.css`**

```css
/* ═══════════════════════════════════════
   404 PAGE
   ═══════════════════════════════════════ */

.error-wrap {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--container-pad);
    gap: var(--space-sm);
}
.error-code {
    font-family: var(--font-display);
    font-size: clamp(6rem, 18vw, 14rem);
    color: var(--accent);
    line-height: 1;
}
.error-title {
    font-size: var(--fs-xl);
    font-weight: 700;
}
.error-desc { color: var(--soft-blue); max-width: 46ch; }
```

- [ ] **Step 6: Write `cookie-consent.css` stub**

```css
/* ═══════════════════════════════════════
   COOKIE CONSENT
   Scoped styles for the cookie banner.
   Used when module "cookie-consent" is active.
   ═══════════════════════════════════════ */

#cookie-consent {
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    max-width: 520px;
    width: calc(100% - 3rem);
    background: rgba(13, 27, 42, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(124, 152, 179, 0.2);
    border-radius: var(--radius-lg);
    padding: var(--space-sm);
    z-index: 200;
    display: none;
    font-size: var(--fs-sm);
}
#cookie-consent.visible { display: block; }
#cookie-consent .actions { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
```

### Task 14: Create `assets/js/shared.js`

**Files:**
- Create: `assets/js/shared.js`

- [ ] **Step 1: Write shared JS**

```javascript
/* ═══════════════════════════════════════
   SHARED JS
   Nav scroll state, mobile hamburger,
   reveal-on-scroll, scroll-to-top button.
   Kept dependency-free, vanilla.
   ═══════════════════════════════════════ */

(function () {
    // Nav scroll state
    const nav = document.querySelector('nav');
    if (nav) {
        const onScroll = () => {
            nav.classList.toggle('scrolled', window.scrollY > 40);
        };
        document.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // Mobile hamburger
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });
        navLinks.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => navLinks.classList.remove('open'));
        });
    }

    // Reveal on scroll
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        reveals.forEach(el => io.observe(el));
    }

    // Scroll progress bar + back-to-top
    const scrollBar = document.getElementById('scrollProgress');
    const scrollTop = document.getElementById('scrollTop');
    if (scrollBar || scrollTop) {
        const onScrollProgress = () => {
            const h = document.documentElement;
            const ratio = h.scrollTop / (h.scrollHeight - h.clientHeight);
            if (scrollBar) scrollBar.style.width = (ratio * 100) + '%';
            if (scrollTop) {
                const show = h.scrollTop > 600;
                scrollTop.style.opacity = show ? '1' : '0';
                scrollTop.style.pointerEvents = show ? 'auto' : 'none';
                scrollTop.style.transform = show ? 'translateY(0)' : 'translateY(10px)';
            }
        };
        document.addEventListener('scroll', onScrollProgress, { passive: true });
        onScrollProgress();
    }
    if (scrollTop) {
        scrollTop.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
})();
```

### Task 15: Create `assets/js/cookie-consent.js` stub

Minimal dependency-free consent banner. Appears only when the module is activated (later, the HTML `<script src="...">` in pages is added by `/setup-integration cookie-consent`). Stub ships now for completeness.

**Files:**
- Create: `assets/js/cookie-consent.js`

- [ ] **Step 1: Write stub**

```javascript
/* ═══════════════════════════════════════
   COOKIE CONSENT
   Minimal, dependency-free. Remembers choice
   in localStorage. Call window.cookieConsent.accept()
   or .decline() from your analytics loader to
   gate script insertion.
   ═══════════════════════════════════════ */

(function () {
    const KEY = 'cc:choice:v1';
    const stored = localStorage.getItem(KEY);

    const banner = document.getElementById('cookie-consent');
    if (!banner) return;

    if (!stored) banner.classList.add('visible');

    const accept = () => { localStorage.setItem(KEY, 'accept'); banner.classList.remove('visible'); window.dispatchEvent(new CustomEvent('cookies:accepted')); };
    const decline = () => { localStorage.setItem(KEY, 'decline'); banner.classList.remove('visible'); window.dispatchEvent(new CustomEvent('cookies:declined')); };

    banner.querySelector('[data-cc-accept]')?.addEventListener('click', accept);
    banner.querySelector('[data-cc-decline]')?.addEventListener('click', decline);

    window.cookieConsent = {
        status: () => localStorage.getItem(KEY),
        accept, decline
    };

    if (stored === 'accept') window.dispatchEvent(new CustomEvent('cookies:accepted'));
})();
```

---

## Phase 4 — Assets scaffolding (Task 16)

### Task 16: Create `assets/` subfolder READMEs

**Files:**
- Create: `assets/fonts/README.md`
- Create: `assets/photos/README.md`
- Create: `assets/icons/README.md`
- Create: `assets/illustrations-blog/README.md`

- [ ] **Step 1: Write font README**

```markdown
# Fonts

Drop your WOFF2 (and WOFF fallback) files here.

## Declare in `assets/css/main.css` or a dedicated `fonts.css`:

    @font-face {
        font-family: 'YourFont';
        src: url('../fonts/your-font/YourFont.woff2') format('woff2'),
             url('../fonts/your-font/YourFont.woff')  format('woff');
        font-display: swap;
    }

## Preload in `<head>` of `index.html`:

    <link rel="preload" href="assets/fonts/your-font/YourFont.woff2" as="font" type="font/woff2" crossorigin>

Keep the display font local for reliability and performance. Body fonts can use Google Fonts with `preconnect`.
```

- [ ] **Step 2: Write photos README**

```markdown
# Photos

Hero photos, team photos, testimonial avatars, project screenshots.

Optimize before committing:

    bash scripts/optimize-image.sh path/to/photo.jpg

Outputs `.webp` at quality 82, roughly halving size.

Always set `width` and `height` attributes on `<img>` to prevent layout shift.
Always set `loading="lazy"` unless the image is above the fold.
```

- [ ] **Step 3: Write icons README**

```markdown
# Icons

Two approaches recommended:

1. **Inline SVG** for one-off icons. Keep them small (< 2 KB).
2. **Lucide** for large icon sets. Include `lucide-1.8.0.min.js` locally (pinned) and call `lucide.createIcons()` after DOM ready.

Avoid icon fonts.
```

- [ ] **Step 4: Write illustrations-blog README**

```markdown
# Blog illustrations

Auto-generated by `scripts/generate-image.py` (Plan 3) from the brand prompt in `docs/brand/illustration-prompt.md`.

Naming convention: `<article-slug>.webp`, 1200×675 (16:9), background matching the primary palette token.
```

---

## Phase 5 — HTML placeholder pages (Tasks 17-22)

### Task 17: Create `index.html` (home)

**Files:**
- Create: `index.html`

- [ ] **Step 1: Write home placeholder**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your site — tagline</title>
    <meta name="description" content="Replace with a 150-char description for search and social.">
    <link rel="canonical" href="https://example.com/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://example.com/">
    <meta property="og:title" content="Your site">
    <meta property="og:description" content="Replace with a 150-char description for search and social.">
    <meta property="og:site_name" content="Your site">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"Organization","name":"Your site","url":"https://example.com"}
    </script>
    <link rel="icon" type="image/svg+xml" href="logo-principal.svg">
    <link rel="manifest" href="site.webmanifest">
    <meta name="theme-color" content="#0D1B2A">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap"></noscript>

    <link rel="stylesheet" href="assets/css/tokens.css">
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="assets/css/home.css">
</head>
<body>

<div id="scrollProgress" style="position:fixed;bottom:0;left:0;height:3px;width:0%;background:var(--accent);z-index:101;"></div>
<a href="#" id="scrollTop" aria-label="Back to top" style="position:fixed;bottom:1.5rem;right:1.5rem;width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:rgba(13,27,42,0.35);backdrop-filter:blur(20px);border:1px solid rgba(124,152,179,0.08);border-radius:12px;z-index:102;opacity:0;pointer-events:none;transition:opacity 0.3s,transform 0.3s;transform:translateY(10px);">↑</a>

<nav>
    <div class="container">
        <a href="/" class="nav-logo" aria-label="Home">
            <img src="logo-principal.svg" alt="Logo" width="40" height="40">
        </a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="#contact" class="nav-cta">Contact</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu">
            <span></span><span></span><span></span>
        </button>
    </div>
</nav>

<main>
    <header class="hero">
        <div class="container">
            <h1 class="hero-title">Your headline <em class="script">goes here</em></h1>
            <p class="hero-desc">Replace this tagline and the CTAs with your own copy during <code>/start-new-site</code> or by editing <code>index.html</code> manually.</p>
            <div class="hero-actions">
                <a href="#contact" class="btn-primary">Primary CTA</a>
                <a href="/projects/" class="btn-secondary">Secondary CTA</a>
            </div>
        </div>
    </header>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="assets/js/shared.js"></script>

</body>
</html>
```

### Task 18: Create `404.html`

**Files:**
- Create: `404.html`

- [ ] **Step 1: Write 404**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 — page not found</title>
    <meta name="robots" content="noindex">
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/404.css">
</head>
<body>
    <main class="error-wrap">
        <p class="error-code">404</p>
        <h1 class="error-title">Page not found</h1>
        <p class="error-desc">The page you're looking for doesn't exist or has been moved.</p>
        <a href="/" class="btn-primary">Back to home</a>
    </main>
</body>
</html>
```

### Task 19: Create `about/index.html`

**Files:**
- Create: `about/index.html`

- [ ] **Step 1: Write about placeholder**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About — Your site</title>
    <meta name="description" content="About page placeholder.">
    <link rel="canonical" href="https://example.com/about/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://example.com/about/">
    <meta property="og:title" content="About — Your site">
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>

<nav>
    <div class="container">
        <a href="/" class="nav-logo"><img src="/logo-principal.svg" alt="Logo" width="40" height="40"></a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
</nav>

<main>
    <section style="padding-top: 8rem;">
        <div class="container">
            <p class="section-number">About</p>
            <h1 class="section-title">Your story <em>goes here</em></h1>
            <p style="margin-top: var(--space-sm); color: var(--soft-blue); max-width: 60ch;">Replace this placeholder with your about copy.</p>
        </div>
    </section>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="/assets/js/shared.js"></script>
</body>
</html>
```

### Task 20: Create `projects/index.html` and `projects/_template-project.html`

**Files:**
- Create: `projects/index.html`
- Create: `projects/_template-project.html`

- [ ] **Step 1: Write `projects/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projects — Your site</title>
    <meta name="description" content="Selected projects.">
    <link rel="canonical" href="https://example.com/projects/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://example.com/projects/">
    <meta property="og:title" content="Projects — Your site">
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/projects.css">
</head>
<body>

<nav>
    <div class="container">
        <a href="/" class="nav-logo"><img src="/logo-principal.svg" alt="Logo" width="40" height="40"></a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
</nav>

<main>
    <section style="padding-top: 8rem;">
        <div class="container">
            <p class="section-number">Projects</p>
            <h1 class="section-title">Selected <em>work</em></h1>
            <div class="projects-grid">
                <!-- Duplicate this card per project, or use /new-page to generate -->
                <a href="/projects/example/" class="project-card">
                    <img src="/assets/photos/project-placeholder.webp" alt="Example project" width="640" height="400" loading="lazy">
                    <div class="project-card-body">
                        <h2 class="blog-card-title">Example project</h2>
                        <p class="blog-card-meta">One-line summary.</p>
                    </div>
                </a>
            </div>
        </div>
    </section>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="/assets/js/shared.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write `projects/_template-project.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Project title] — Your site</title>
    <meta name="description" content="[Project short description]">
    <link rel="canonical" href="https://example.com/projects/[slug]/">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://example.com/projects/[slug]/">
    <meta property="og:title" content="[Project title]">
    <meta property="og:image" content="https://example.com/assets/photos/[slug]-cover.webp">
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/projects.css">
</head>
<body>

<nav>
    <div class="container">
        <a href="/" class="nav-logo"><img src="/logo-principal.svg" alt="Logo" width="40" height="40"></a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
</nav>

<main>
    <article style="padding: 8rem 0 var(--space-xl);">
        <div class="container" style="max-width: 900px;">
            <p class="section-number">[Client / Category]</p>
            <h1 class="section-title">[Project title]</h1>
            <p style="color: var(--soft-blue); margin-top: var(--space-sm);">[One-line summary / date]</p>
            <img src="/assets/photos/[slug]-cover.webp" alt="[Project cover]" width="1200" height="750" loading="eager" style="width:100%; margin: var(--space-md) 0;">
            <p>[Project body. Replace with real content via /new-page "project detail" or manually.]</p>
        </div>
    </article>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="/assets/js/shared.js"></script>
</body>
</html>
```

### Task 21: Create `blog/index.html` and `blog/_template-article.html`

**Files:**
- Create: `blog/index.html`
- Create: `blog/_template-article.html`

- [ ] **Step 1: Write `blog/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — Your site</title>
    <meta name="description" content="Articles and essays.">
    <link rel="canonical" href="https://example.com/blog/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://example.com/blog/">
    <meta property="og:title" content="Blog — Your site">
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/blog.css">
</head>
<body>

<nav>
    <div class="container">
        <a href="/" class="nav-logo"><img src="/logo-principal.svg" alt="Logo" width="40" height="40"></a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
</nav>

<main>
    <header class="blog-hero">
        <div class="container">
            <p class="section-number">Blog</p>
            <h1 class="section-title" style="margin: 0 auto;">Articles &amp; <em>essays</em></h1>
        </div>
    </header>
    <section style="padding-top: 0;">
        <div class="container">
            <div class="blog-grid">
                <!-- Card sample. Duplicate per article or use /new-blog-article (Plan 3). -->
                <a href="/blog/example-article/" class="blog-card">
                    <img src="/assets/illustrations-blog/example-article.webp" alt="Example article cover" width="640" height="360" loading="lazy">
                    <div class="blog-card-body">
                        <h2 class="blog-card-title">Example article title</h2>
                        <p class="blog-card-meta">2026-04-21 · 5 min read</p>
                    </div>
                </a>
            </div>
        </div>
    </section>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="/assets/js/shared.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write `blog/_template-article.html`**

Minimal template. Plan 3 extends it with the full component catalog (callouts, blockquote, code blocks, tables, FAQ, podcast player).

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Article title] — Your site</title>
    <meta name="description" content="[Article 150-char description]">
    <link rel="canonical" href="https://example.com/blog/[slug]/">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://example.com/blog/[slug]/">
    <meta property="og:title" content="[Article title]">
    <meta property="og:image" content="https://example.com/assets/illustrations-blog/[slug].webp">
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"Article","headline":"[Article title]","datePublished":"[YYYY-MM-DD]","author":{"@type":"Person","name":"[Author]"},"image":"https://example.com/assets/illustrations-blog/[slug].webp","mainEntityOfPage":"https://example.com/blog/[slug]/"}
    </script>
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/blog.css">
</head>
<body>

<nav>
    <div class="container">
        <a href="/" class="nav-logo"><img src="/logo-principal.svg" alt="Logo" width="40" height="40"></a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
</nav>

<main>
    <article style="padding: 8rem 0 var(--space-xl);">
        <div class="container" style="max-width: 760px;">
            <nav class="article-breadcrumb" aria-label="Breadcrumb" style="font-size: var(--fs-sm); color: var(--soft-blue); margin-bottom: var(--space-sm);">
                <a href="/">Home</a> / <a href="/blog/">Blog</a> / <span>[Article title]</span>
            </nav>
            <p class="section-number">[Category]</p>
            <h1 class="section-title">[Article title]</h1>
            <p style="color: var(--soft-blue); margin-top: var(--space-sm);">[YYYY-MM-DD] · [N] min read</p>
            <img src="/assets/illustrations-blog/[slug].webp" alt="[Cover alt text]" width="1200" height="675" loading="eager" style="width:100%; border-radius: var(--radius-lg); margin: var(--space-md) 0;">
            <p>[Article body. Plan 3 adds component blocks: blockquote, article-callout, code-block, table-wrapper, article-img-*, article-cta-inline, article-faq, podcast player.]</p>
        </div>
    </article>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="/assets/js/shared.js"></script>
</body>
</html>
```

### Task 22: Create legal pages

**Files:**
- Create: `legal/privacy/index.html`
- Create: `legal/terms/index.html`
- Create: `legal/cookies/index.html`

- [ ] **Step 1: Write `legal/privacy/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy policy — Your site</title>
    <meta name="description" content="Privacy policy.">
    <link rel="canonical" href="https://example.com/legal/privacy/">
    <meta name="robots" content="index, follow">
    <link rel="icon" type="image/svg+xml" href="/logo-principal.svg">
    <meta name="theme-color" content="#0D1B2A">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/legal.css">
</head>
<body>

<nav>
    <div class="container">
        <a href="/" class="nav-logo"><img src="/logo-principal.svg" alt="Logo" width="40" height="40"></a>
        <ul class="nav-links" id="navLinks">
            <li><a href="/about/">About</a></li>
            <li><a href="/projects/">Projects</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        <button class="nav-hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
</nav>

<main class="legal-content">
    <h1>Privacy policy</h1>
    <p>Last updated: [YYYY-MM-DD]</p>

    <h2>1. Data we collect</h2>
    <p>Replace with a plain-language description of what you collect, how, and why.</p>

    <h2>2. Cookies</h2>
    <p>See our <a href="/legal/cookies/">cookie policy</a>.</p>

    <h2>3. Your rights (GDPR)</h2>
    <ul>
        <li>Access</li>
        <li>Rectification</li>
        <li>Erasure</li>
        <li>Portability</li>
        <li>Objection</li>
    </ul>

    <h2>4. Contact</h2>
    <p>Email: [contact@example.com]</p>
</main>

<footer>
    <div class="container">
        <p>© <span id="year">2026</span> Your site</p>
        <ul class="footer-links">
            <li><a href="/legal/privacy/">Privacy</a></li>
            <li><a href="/legal/terms/">Terms</a></li>
            <li><a href="/legal/cookies/">Cookies</a></li>
        </ul>
    </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="/assets/js/shared.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write `legal/terms/index.html`**

Copy `legal/privacy/index.html`, change `<title>`, `<link rel="canonical">`, `<meta name="description">`, `<h1>`, and the body sections to terms placeholders (acceptance, use, IP, liability, governing law). Path: `/legal/terms/`.

- [ ] **Step 3: Write `legal/cookies/index.html`**

Same, with cookies placeholders (what cookies we use, strictly necessary vs. analytics vs. marketing, how to opt out, link to browser guides). Path: `/legal/cookies/`.

### Task 23: Create `sitemap.xml`, `robots.txt`, `robots-staging.txt`, `site.webmanifest`, logo placeholder

**Files:**
- Create: `sitemap.xml`
- Create: `robots.txt`
- Create: `robots-staging.txt`
- Create: `site.webmanifest`
- Create: `logo-principal.svg`

- [ ] **Step 1: Write `sitemap.xml`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/</loc>
        <priority>1.0</priority>
        <changefreq>weekly</changefreq>
    </url>
    <url>
        <loc>https://example.com/about/</loc>
        <priority>0.8</priority>
        <changefreq>monthly</changefreq>
    </url>
    <url>
        <loc>https://example.com/projects/</loc>
        <priority>0.8</priority>
        <changefreq>monthly</changefreq>
    </url>
    <url>
        <loc>https://example.com/blog/</loc>
        <priority>0.8</priority>
        <changefreq>weekly</changefreq>
    </url>
    <url>
        <loc>https://example.com/legal/privacy/</loc>
        <priority>0.3</priority>
        <changefreq>yearly</changefreq>
    </url>
    <url>
        <loc>https://example.com/legal/terms/</loc>
        <priority>0.3</priority>
        <changefreq>yearly</changefreq>
    </url>
    <url>
        <loc>https://example.com/legal/cookies/</loc>
        <priority>0.3</priority>
        <changefreq>yearly</changefreq>
    </url>
</urlset>
```

- [ ] **Step 2: Write `robots.txt`**

```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

- [ ] **Step 3: Write `robots-staging.txt`**

```
User-agent: *
Disallow: /
```

- [ ] **Step 4: Write `site.webmanifest`**

```json
{
    "name": "Your site",
    "short_name": "Your site",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0D1B2A",
    "theme_color": "#0D1B2A",
    "icons": [
        { "src": "/logo-principal.svg", "sizes": "any", "type": "image/svg+xml" }
    ]
}
```

- [ ] **Step 5: Write `logo-principal.svg`** (placeholder mark)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" fill="none" aria-label="Logo placeholder">
    <circle cx="40" cy="40" r="36" stroke="#FAFAFA" stroke-width="3" fill="none"/>
    <circle cx="40" cy="40" r="8" fill="#F9DC5C"/>
</svg>
```

### Task 24: Commit static pages

- [ ] **Step 1: Stage and commit**

```bash
git add assets/ index.html 404.html about/ projects/ blog/ legal/ sitemap.xml robots.txt robots-staging.txt site.webmanifest logo-principal.svg
git commit -m "feat: scaffold static pages, tokens, and shared CSS/JS"
```

Expected: commit succeeds.

### Task 25: Browser smoke test

- [ ] **Step 1: Open home in browser**

```bash
open index.html
```

Expected: page renders with dark background, accent yellow heading "your headline goes here", nav across top, footer at bottom. No console errors (check DevTools).

- [ ] **Step 2: Navigate each page**

Click About, Projects, Blog, each legal page. All should render styled.

- [ ] **Step 3: Responsive check**

Resize viewport below 860px. Nav should collapse to hamburger. Click hamburger, drawer should open.

- [ ] **Step 4: 404 test**

Open `404.html` directly. Should render the styled 404 page.

---

## Phase 6 — Security and deploy infrastructure (Tasks 26-31)

### Task 26: Create `.htaccess` (production)

**Files:**
- Create: `.htaccess`

- [ ] **Step 1: Write production `.htaccess`**

Note on CSP: the directive below is the **baseline**. It allows self + Google Fonts only. When modules (Cal.com, Brevo, GA, etc.) are activated in Plan 4, the `/setup-integration` command mutates this CSP to whitelist the required hosts. The comment marker `# CSP:module:<name>` helps those automated edits locate the directive.

```apache
# ═══════════════════════════════════════
# DIRECTORY LISTING & ERROR PAGES
# ═══════════════════════════════════════
Options -Indexes
ErrorDocument 403 /404.html
ErrorDocument 404 /404.html

# Noindex for docs/media files (PDFs, etc.)
<IfModule mod_headers.c>
    <FilesMatch "\.(pdf)$">
        Header set X-Robots-Tag "noindex, nofollow"
    </FilesMatch>
</IfModule>

# ═══════════════════════════════════════
# CLEAN URLs
# ═══════════════════════════════════════
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} !on
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]

# Force non-www canonical (edit for your domain)
# RewriteCond %{HTTP_HOST} ^www\.example\.com$ [NC]
# RewriteRule ^ https://example.com%{REQUEST_URI} [R=301,L]

# Redirect .html to clean URLs
RewriteCond %{THE_REQUEST} \s/(.+)\.html[\s?] [NC]
RewriteRule ^ /%1 [R=301,L]

# Internal rewrite to serve .html for clean URL
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.+)$ $1.html [L]

# ═══════════════════════════════════════
# SECURITY HEADERS
# ═══════════════════════════════════════
<IfModule mod_headers.c>
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains" env=HTTPS
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()"
    Header always set Cross-Origin-Opener-Policy "same-origin-allow-popups"

    # CSP: baseline — modules extend this via /setup-integration.
    # CSP:module:baseline
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-src 'self';"
</IfModule>

# ═══════════════════════════════════════
# CACHE CONTROL
# ═══════════════════════════════════════
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/x-icon "access plus 1 year"
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType application/font-woff2 "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType text/javascript "access plus 1 month"
    ExpiresByType text/html "access plus 1 hour"
</IfModule>

# ═══════════════════════════════════════
# COMPRESSION
# ═══════════════════════════════════════
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript application/json image/svg+xml
</IfModule>

# ═══════════════════════════════════════
# MIME
# ═══════════════════════════════════════
<IfModule mod_mime.c>
    AddType image/webp .webp
    AddType application/javascript .js
</IfModule>
```

### Task 27: Create `.htaccess-staging`

**Files:**
- Create: `.htaccess-staging`

- [ ] **Step 1: Write staging `.htaccess`**

```apache
# ═══════════════════════════════════════
# STAGING — HTTP BASIC AUTH + INHERITS PROD RULES
# ═══════════════════════════════════════
AuthType Basic
AuthName "Staging — restricted"
AuthUserFile /home/<your-host-user>/staging/.htpasswd
Require valid-user

Options -Indexes
ErrorDocument 403 /404.html
ErrorDocument 404 /404.html

RewriteEngine On

RewriteCond %{HTTPS} !on
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]

RewriteCond %{THE_REQUEST} \s/(.+)\.html[\s?] [NC]
RewriteRule ^ /%1 [R=301,L]

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.+)$ $1.html [L]

<IfModule mod_headers.c>
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set X-Robots-Tag "noindex, nofollow"
</IfModule>
```

Note: `AuthUserFile` path must be absolute on the server. The placeholder `/home/<your-host-user>/staging/.htpasswd` is replaced by the setup wizard in Plan 2, or manually during setup. Document this clearly in `SETUP.md` (already mentioned in Task 7).

### Task 28: Create `scripts/htpasswd-gen.sh`

**Files:**
- Create: `scripts/htpasswd-gen.sh`

- [ ] **Step 1: Write script**

```bash
#!/usr/bin/env bash
# ═══════════════════════════════════════
# STAGING .htpasswd GENERATOR
# Creates .htpasswd with a random password,
# prints credentials once. User must store them
# in their password manager.
# ═══════════════════════════════════════

set -euo pipefail

if ! command -v htpasswd >/dev/null 2>&1; then
    echo "htpasswd not installed. macOS: already included. Linux: apt-get install apache2-utils"
    exit 1
fi

USER="${1:-staging}"
PASS="$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 20)"

htpasswd -cbB .htpasswd "$USER" "$PASS" >/dev/null

cat <<EOF
.htpasswd generated.

Username: $USER
Password: $PASS

STORE THIS NOW in your password manager. Not shown again.

File: .htpasswd (gitignored by default)
Upload it to your SFTP host at the staging root, alongside .htaccess-staging
renamed to .htaccess — the GitHub Actions staging workflow does this for you.
EOF
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/htpasswd-gen.sh
```

### Task 29: Create `scripts/optimize-image.sh`

**Files:**
- Create: `scripts/optimize-image.sh`

- [ ] **Step 1: Write script**

```bash
#!/usr/bin/env bash
# ═══════════════════════════════════════
# IMAGE OPTIMIZER
# Converts JPG/PNG to WebP q=82, keeps original.
# Requires: cwebp (brew install webp / apt install webp)
# ═══════════════════════════════════════

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <image.jpg|png> [quality=82]"
    exit 1
fi

INPUT="$1"
QUALITY="${2:-82}"

if [ ! -f "$INPUT" ]; then
    echo "File not found: $INPUT"
    exit 1
fi

if ! command -v cwebp >/dev/null 2>&1; then
    echo "cwebp not installed. macOS: brew install webp. Debian/Ubuntu: apt-get install webp"
    exit 1
fi

OUTPUT="${INPUT%.*}.webp"
cwebp -q "$QUALITY" "$INPUT" -o "$OUTPUT"

echo "Written: $OUTPUT"
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/optimize-image.sh
```

### Task 30: Create `api/_env.php`

**Files:**
- Create: `api/_env.php`

- [ ] **Step 1: Write env loader**

```php
<?php
/**
 * ═══════════════════════════════════════
 * ENV LOADER
 * Reads .env at the site root and exposes values
 * via getenv(). Include this at the top of every
 * PHP endpoint in api/:
 *
 *     require_once __DIR__ . '/_env.php';
 *     $key = getenv('BREVO_API_KEY') ?: '';
 *
 * The .env file must NEVER be committed to git.
 * It must be created manually on the host via
 * SFTP at the site root.
 * ═══════════════════════════════════════
 */

(function () {
    $envPath = realpath(__DIR__ . '/../.env');
    if ($envPath === false || !is_readable($envPath)) {
        return; // no .env — fail silently; callers handle missing vars.
    }

    $lines = @file($envPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if ($lines === false) return;

    foreach ($lines as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#')) continue;

        $eq = strpos($line, '=');
        if ($eq === false) continue;

        $name  = trim(substr($line, 0, $eq));
        $value = trim(substr($line, $eq + 1));

        // Strip surrounding quotes if present
        if (strlen($value) >= 2) {
            $first = $value[0];
            $last  = $value[strlen($value) - 1];
            if (($first === '"' && $last === '"') || ($first === "'" && $last === "'")) {
                $value = substr($value, 1, -1);
            }
        }

        if ($name !== '' && getenv($name) === false) {
            putenv("$name=$value");
        }
    }
})();
```

### Task 31: Create `api/webhook.php.example`

**Files:**
- Create: `api/webhook.php.example`

Generic inbound webhook template. Demonstrates the `_env.php` loader and the CORS/validation pattern that Plan 4 modules follow.

- [ ] **Step 1: Write template**

```php
<?php
/**
 * Generic webhook receiver — example.
 * Copy to webhook-<yourname>.php and customize.
 */

require_once __DIR__ . '/_env.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: ' . (getenv('SITE_URL') ?: 'https://example.com'));
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST')     { http_response_code(405); echo json_encode(['error' => 'method not allowed']); exit; }

$raw   = file_get_contents('php://input');
$input = json_decode($raw, true);
if (!is_array($input)) { http_response_code(400); echo json_encode(['error' => 'invalid json']); exit; }

// ... validation & business logic here ...

echo json_encode(['success' => true]);
```

### Task 32: Commit security and scripts

- [ ] **Step 1: Stage and commit**

```bash
git add .htaccess .htaccess-staging api/ scripts/
git commit -m "feat: add security defaults, env loader, and helper scripts"
```

Expected: commit succeeds.

---

## Phase 7 — GitHub Actions workflows (Tasks 33-35)

### Task 33: Create `deploy-staging.yml`

**Files:**
- Create: `.github/workflows/deploy-staging.yml`

- [ ] **Step 1: Write workflow**

```yaml
name: Deploy to Staging

on:
  push:
    branches: [staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Prepare staging payload (noindex + robots block + htpasswd + strip GA + clean internals)
        run: |
          # Use staging robots
          cp robots-staging.txt robots.txt

          # Inject noindex meta into every HTML
          find . -name "*.html" -not -path "./.git/*" -exec sed -i 's/<head>/<head><meta name="robots" content="noindex, nofollow">/' {} \;

          # Remove sitemap from staging payload (not for public indexing)
          rm -f sitemap.xml

          # Strip GA blocks between the markers
          find . -name "*.html" -not -path "./.git/*" -exec sed -i '/<!-- GA_START -->/,/<!-- GA_END -->/d' {} \;

          # Swap in staging .htaccess
          cp .htaccess-staging .htaccess

          # Remove internals that must not ship
          rm -rf .git .claude .github docs .superpowers \
                 .htaccess-staging robots-staging.txt \
                 .env.example SETUP.md CONTRIBUTING.md \
                 docs/superpowers

      - name: Deploy via SFTP
        env:
          LFTP_PASSWORD: ${{ secrets.OVH_PASSWORD }}
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y -qq lftp > /dev/null 2>&1
          lftp -u "${{ secrets.OVH_USERNAME }}","$LFTP_PASSWORD" \
            -e "set sftp:auto-confirm yes; set net:timeout 30; set net:max-retries 2; mirror -R --verbose . ${{ secrets.OVH_STAGING_DIR }}; quit" \
            sftp://${{ secrets.OVH_HOST }}
```

### Task 34: Create `deploy-production.yml`

**Files:**
- Create: `.github/workflows/deploy-production.yml`

- [ ] **Step 1: Write workflow**

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Clean non-production files
        run: |
          rm -rf .git .claude .github .superpowers \
                 .htaccess-staging robots-staging.txt \
                 .env.example SETUP.md CONTRIBUTING.md
          # Keep docs/<anything>.pdf, drop the rest under docs/
          find docs -type f ! -name "*.pdf" -delete 2>/dev/null || true
          find docs -type d -empty -delete 2>/dev/null || true

      - name: Deploy via SFTP
        env:
          LFTP_PASSWORD: ${{ secrets.OVH_PASSWORD }}
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y -qq lftp > /dev/null 2>&1
          lftp -u "${{ secrets.OVH_USERNAME }}","$LFTP_PASSWORD" \
            -e "set sftp:auto-confirm yes; set net:timeout 30; set net:max-retries 2; mirror -R --verbose . ${{ secrets.OVH_PROD_DIR }}; quit" \
            sftp://${{ secrets.OVH_HOST }}
```

### Task 35: Commit workflows

- [ ] **Step 1: Stage and commit**

```bash
git add .github/
git commit -m "ci: add SFTP deploy workflows for staging and main"
```

Expected: commit succeeds. `git log --oneline` shows 4 commits total (bootstrap, pages, security, ci).

---

## Phase 8 — Final verification (Tasks 36-38)

### Task 36: Tree check

- [ ] **Step 1: Print full tree, excluding `.git`**

```bash
find . -type f -not -path "./.git/*" | sort
```

Expected (at minimum, order may vary — verify each path exists):

```
./.env.example
./.gitignore
./.github/workflows/deploy-production.yml
./.github/workflows/deploy-staging.yml
./.htaccess
./.htaccess-staging
./404.html
./CONTRIBUTING.md
./LICENSE
./README.md
./SETUP.md
./about/index.html
./api/_env.php
./api/webhook.php.example
./assets/css/404.css
./assets/css/blog.css
./assets/css/cookie-consent.css
./assets/css/home.css
./assets/css/legal.css
./assets/css/main.css
./assets/css/projects.css
./assets/css/tokens.css
./assets/fonts/README.md
./assets/icons/README.md
./assets/illustrations-blog/README.md
./assets/js/cookie-consent.js
./assets/js/shared.js
./assets/photos/README.md
./blog/_template-article.html
./blog/index.html
./docs/README.md
./docs/brand/brand.md
./docs/brand/illustration-prompt.md
./docs/brand/tone-of-voice.md
./docs/brand/toolbelt.md
./docs/components.md
./docs/content/README.md
./docs/drafts/README.md
./docs/inspirations/README.md
./docs/superpowers/plans/2026-04-21-plan-1-foundation.md
./docs/superpowers/specs/2026-04-21-claude-site-starter-design.md
./index.html
./legal/cookies/index.html
./legal/privacy/index.html
./legal/terms/index.html
./logo-principal.svg
./projects/_template-project.html
./projects/index.html
./robots-staging.txt
./robots.txt
./scripts/htpasswd-gen.sh
./scripts/optimize-image.sh
./site.webmanifest
./sitemap.xml
```

### Task 37: HTML validation (manual)

- [ ] **Step 1: Run a validator on each HTML file**

Manual: paste each page's source into https://validator.w3.org/ or use local `vnu.jar` if available. Expected: no errors. Warnings about placeholder alt text are acceptable at this stage.

- [ ] **Step 2: Lighthouse smoke test (local)**

Open `index.html` in Chrome, DevTools → Lighthouse, run on "Performance, SEO, Best Practices, Accessibility" with device Mobile. Expected: SEO and Accessibility above 90 with placeholders. Performance will vary since fonts load over network. Record scores in a scratchpad for baseline.

### Task 38: Final commit

- [ ] **Step 1: Check status**

```bash
git status
```

Expected: `nothing to commit, working tree clean`.

- [ ] **Step 2: Log**

```bash
git log --oneline
```

Expected: 4 commits matching the phase boundaries.

---

## Success criteria for Plan 1

Plan 1 is complete when:

1. `git log` shows 4 clean commits corresponding to the phases.
2. `index.html` opens in a browser and renders with tokens, nav, hero, footer.
3. All 7 other HTML pages render without console errors and navigate between each other.
4. Responsive behavior works (hamburger under 860px).
5. `.htaccess` and `.htaccess-staging` are present, commented, and valid Apache syntax.
6. `.github/workflows/*.yml` parse cleanly (paste into https://rhysd.github.io/actionlint/ or use `gh workflow view` after first push to confirm).
7. No secrets or real keys anywhere in the tree. `grep -iE "key|token|password|secret" -r . --exclude-dir=.git` returns only variable names and placeholder labels.
8. `docs/brand/brand.md`, `tone-of-voice.md`, `illustration-prompt.md`, `toolbelt.md`, `components.md` exist as templates.

## Known gaps (by design, addressed in subsequent plans)

- No `.claude/commands/`, no skill → Plan 2.
- Full `README.md` (Security section, Lighthouse workflow, slash command quickstart) → Plan 2.
- Blog components (callouts, FAQ, podcast player, table wrapper) → Plan 3.
- `generate-image.py`, `generate-podcast.py`, `sitemap-update.py` → Plan 3.
- `api/brevo.php.example`, Cal.com embed, analytics, cookie banner integration → Plan 4.
- Dogfood end-to-end test (create a site from scratch using `/start-new-site`) → after Plan 2.

---

**End of Plan 1.**
