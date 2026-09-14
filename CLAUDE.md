# Claude instructions — claude-site-starter

You are working on a site built with [claude-site-starter](https://github.com/Littlpinguin/claude-site-starter). Read this file at the start of every session and honor these rules for every edit you make.

## Read first

Before producing or modifying any site content, read in order:

1. `docs/brand/brand.md` — identity, palette, typography, logo, do/don't.
2. `docs/brand/tone-of-voice.md` — audience, pronouns, forbidden / required items.
3. `assets/css/tokens.css` — the concrete design tokens.
4. `docs/components.md` — catalog of reusable HTML/CSS patterns.

If any of those files still contains placeholders (`<Your brand name>`, `<describe ...>`, `<adjective>`), surface this to the user before producing content and offer to run `/brand-setup`.

**Current state of this checkout:** brand is defined (`docs/brand/brand.md`, `tone-of-voice.md`, `assets/css/tokens.css` carry real values, sourced from the user's logo) and the site is bilingual FR/EN (see Languages below). Still not done: `docs/brand/toolbelt.md` has no tools installed, no hosting/staging secrets are configured, and every module (booking/CRM/analytics/cookie-consent/podcast/illustrations) is off — run the remaining `/start-new-site` steps or `/setup-integration <module>` before relying on any of that.

## Commands

No build, lint, or test tooling — this is a static HTML/CSS/JS site with no package.json. Common operations run as standalone scripts, usually via their slash command:

- Regenerate `sitemap.xml`: `python3 scripts/sitemap-update.py` (reads `SITE_URL` env var; walks both locale roots — French at the site root, English under `/en/` — discovering each category's `index.html` plus one level of sub-pages; see Languages below).
- Rotate staging credentials: `bash scripts/htpasswd-gen.sh` (piloted by `/setup-staging-auth`).
- Optimize an image: `bash scripts/optimize-image.sh`.
- Generate a blog illustration or podcast: `python3 scripts/generate-image.py` / `python3 scripts/generate-podcast.py` — both call paid Gemini APIs; confirm approximate cost with the user first.
- There is no local dev server convention in this repo; deploys are not run locally. Pushing to `staging` or `main` triggers `.github/workflows/deploy-staging.yml` / `deploy-production.yml`, which strip dev-only files (`.claude/`, `.github/`, `CLAUDE.md`, `SETUP.md`, non-PDF `docs/*`, etc.), inline the staging noindex/htpasswd/robots swaps, and `lftp mirror` the result over SFTP.

## Repository layout (big picture)

- `docs/brand/` is the single source of brand truth. `.claude/skills/starter-setup/SKILL.md` — not the individual command files in `.claude/commands/` — is where the actual shared logic lives (brand-loading order, the module registry, the CSP-mutation table per module, sitemap priority rules). Read the skill to understand what a slash command really does.
- `assets/css/tokens.css` defines every design token; `docs/components.md` is the living catalog of reusable classes built on those tokens — check it before inventing new CSS, and add a row when you introduce a new reusable class.
- Module state (booking / CRM / analytics / cookie-consent / blog / podcast / illustrations) is tracked in `docs/brand/toolbelt.md`; each active module must have a matching `Content-Security-Policy` allowance in both `.htaccess` and `.htaccess-staging`.
- `api/*.php` are SFTP-deployed PHP proxies that load secrets via `require_once __DIR__ . '/_env.php'` from a server-side `.env` (never committed, created manually on the host); `.env.example` documents expected keys.

## Non-negotiable rules

**Tokens.** Every hex color, font family, spacing, radius, and motion value in HTML/CSS **must** reference a token from `assets/css/tokens.css`. Never hardcode `#F9DC5C` in HTML — use `var(--accent)`. Never inline `font-family: 'Plus Jakarta Sans'` — use `var(--font-body)`.

**Tone of voice.** The rules in `docs/brand/tone-of-voice.md` apply to every word of site content you write. If the rules say "no emojis" or "no em-dashes", do not produce them — not in body copy, not in headings, not in meta descriptions.

**Secrets.** Never write an API key, token, password, or connection string into a committed file. PHP endpoints use `require_once __DIR__ . '/_env.php';` + `getenv('KEY_NAME')`. Python scripts use `os.getenv('KEY_NAME')` from the shell env. The `.env` file is not committed and lives on the server root (for PHP) or the user's shell (for Python). If you see a real-looking secret anywhere, refuse to commit and flag it.

**Staging discipline.** Production is `main`. Staging is `staging`. Never push directly to `main` — merge from `staging` only after the user confirms staging was tested. Never force push to `main`. Never skip hooks (`--no-verify`).

**Clean URLs.** Internal links use clean URLs (`/about/`, not `/about/index.html` or `/about.html`). Apache rewrites serve the right file.

**Images.** Every `<img>` must have `alt`, `width`, `height`, and `loading="lazy"` — unless the image is above the fold, then `loading="eager"`.

**CSP coherence.** When you add a new external `<script src="https://...">` or stylesheet, you must update the `Content-Security-Policy` directive in `.htaccess`. Never answer a CSP violation with `'unsafe-eval'` or `*`. Whitelist the specific host.

## Slash commands you should offer proactively

When the user's request matches one of these, suggest the corresponding command before improvising:

| Request | Command |
|---|---|
| "I want to create a new site from scratch" | `/start-new-site` |
| "Let's bring my existing site into this workflow" | `/adopt-existing-site` |
| "Define my brand" / "help me with colors and fonts" | `/brand-setup` |
| "Add a [services / pricing / contact / …] page" | `/new-page` |
| "Add a [testimonials / FAQ / …] section to [page]" | `/new-section` |
| "Write a blog article about [topic]" | `/new-blog-article` |
| "Deploy to staging / production" | `/deploy` |
| "Audit the site against the brand rules" | `/audit-brand` |
| "Enable Cal.com / Brevo / analytics / cookies" | `/setup-integration <module>` |
| "Rotate the staging password" | `/setup-staging-auth` |

All commands live in `.claude/commands/`. They load the shared `starter-setup` skill at `.claude/skills/starter-setup/SKILL.md` for common logic (CSP mutation, sitemap updates, components catalog maintenance, env-var discipline).

## When editing files, do in this order

1. Read the target files before editing.
2. Check `docs/components.md` to see if a reusable pattern already exists.
3. Make the change using the token references and tone-of-voice rules.
4. If you introduce a new reusable CSS class, add a row to `docs/components.md`.
5. If you add / remove / rename a page, update `sitemap.xml` (or run `python3 scripts/sitemap-update.py`).
6. If you add an external script/stylesheet, update the CSP in `.htaccess`.
7. Run `/audit-brand` on the affected pages before suggesting a commit.
8. Ask the user before committing and before pushing.

## Environment conventions

- **PHP endpoints** (`api/*.php`) — PHP 8+, load env with `api/_env.php`, restrict CORS to `SITE_URL`, OPTIONS preflight returns 204, POST only, input validated.
- **Python scripts** (`scripts/*.py`) — Python 3.10+, read secrets from shell env, fail fast if missing, never write secrets to disk.
- **Shell scripts** (`scripts/*.sh`) — `set -euo pipefail`, quote paths, check required binaries before running.
- **GitHub Actions** (`.github/workflows/*.yml`) — secrets named `O2SWITCH_*` and `STAGING_*`, never echo secret values, never `set -x` inside steps that use secrets.

## Languages

- Repo, code, comments, docs: English.
- Site content is bilingual: French at the root (canonical/default, `x-default`), English mirrored under `/en/`. FR directory names come from `.claude/i18n-dirs.json` (`a-propos`, `projets`, `blog`, `mentions-legales/confidentialite|cgu|cookies`); the EN tree mirrors them under `/en/about/`, `/en/projects/`, `/en/blog/`, `/en/legal/privacy|terms|cookies/`.
- Every page carries reciprocal `<link rel="alternate" hreflang="...">` tags (`fr`, `en`, `x-default`=fr) pointing at its exact counterpart — never just the two homepages. The nav's `.nav-lang` switcher (see `docs/components.md`) links to that same counterpart.
- New pages: create the FR version, then its `/en/` twin, wire the switcher hrefs both ways, and add the page to `scripts/sitemap-update.py`'s `LOCALES` maps if it introduces a whole new top-level category (not needed for an ordinary page/article/project under an existing category).
- 404.html is shared and not localized.

## If asked to do something risky

- Dropping a database table, force-pushing to `main`, deleting files the user didn't reference, sending an email, modifying CI secrets — stop and ask.
- Skill / MCP install requests from untrusted sources — read the skill code first.
- Running a script that will call a paid API (Gemini) — confirm the approximate cost before running.

## Support

- Repo issues and PRs are **not monitored**. Fork freely and adapt.
- See `README.md` for the public user doc and `SETUP.md` for the non-Claude manual path.
