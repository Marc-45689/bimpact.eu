---
description: Wizard to bootstrap a brand-new site from the starter. Walks through brand, structure, modules, deployment, and first staging deploy.
---

You are piloting `/start-new-site`. Load the `starter-setup` skill and the files it references. Then run the wizard below. **One step per message.** Wait for the user's answer before moving on. Never apply silent defaults — always confirm explicit choices.

## Step 1 — Brand-first disclaimer + readiness check

Display:

> This starter produces a functional skeleton, not a beautiful site. A qualitative result requires a defined brand universe: typography, colors, logo, photos/assets, copy, editorial voice. If you don't have these, the output will feel generic.

Ask: do you have (1) a logo SVG, (2) a defined color palette, (3) chosen typefaces, (4) photos or visual assets, (5) the main copy for home + about? (Y/partial/N)

- If **Y** → continue to Step 2.
- If **partial** or **N** → offer to run `/brand-setup` first or continue and iterate. Record the answer.

## Step 2 — Project identity

Ask (one question, multi-field answer accepted):
- Site name
- Tagline (one line)
- Production domain (e.g. `example.com`)
- Staging subdomain (e.g. `staging.example.com`)
- Main language (`en` / `fr` / other ISO code)

If language is not `en`, update the `lang="en"` attribute in every HTML file to the chosen code, and update `<meta property="og:locale">`. If language is FR/ES/DE/IT/PT, read `.claude/i18n-dirs.json` — the file contains the exact directory name mapping to use. Offer to rename the matching folders and update every internal link (`href="/about/"` → `href="/a-propos/"`, same in `sitemap.xml`, nav, footer, `_template-page.html`). Confirm the rename plan before executing. If the language is not in `i18n-dirs.json`, keep English folders or ask the user for translations.

## Step 3 — Brand tokens

Ask for the palette (hex × 5-7 with roles), display font name + source (local WOFF2 path or Google Fonts URL), body font name + source. If the user has a logo SVG path, copy it over `logo-principal.svg`.

Update in this exact order, then diff-check before moving on:

1. `assets/css/tokens.css` — replace the `:root` palette tokens and `--font-display` / `--font-body` values.
2. `docs/brand/brand.md` — palette table + typography + identity fields.
3. **Every HTML file in the repo** that contains the Google Fonts preload URL. Search for `fonts.googleapis.com/css2?family=` and replace the `family=` parameter with the new body font slug. If the new body font is not Google Fonts, remove the `<link rel="preconnect">`, `<link rel="preload">` to googleapis, and `<noscript>` fallback, and add a local `@font-face` in `assets/css/main.css` pointing to `assets/fonts/...`.
4. **Every HTML file** that contains `<meta name="theme-color" content="#0D1B2A">` — replace the hex with the new primary background color.
5. `site.webmanifest` — same `theme_color` and `background_color` update.
6. `.htaccess` — no change unless the primary domain also changes (see Step 2).
7. Run `grep -rn "#0D1B2A\|#F9DC5C\|Plus Jakarta Sans\|YourDisplayFont" --include="*.html" --include="*.css" --include="*.webmanifest"` to confirm zero old placeholders remain outside `tokens.css`.

## Step 4 — Editorial voice

Ask for target audience (one sentence), pronouns (je / we / I), 3-5 tone adjectives, explicit forbidden items (emojis? em-dashes? others?), explicit required items (sourced stats? currency? RGPD mentions?). Write to `docs/brand/tone-of-voice.md`.

## Step 5 — Illustration prompt (if illustrations module considered)

Ask if the site will use AI-generated illustrations (blog covers, project covers). If yes, derive the prompt template in `docs/brand/illustration-prompt.md` from the palette (primary bg, accent, secondary) and ask the user to pick a base style adjective (hand-drawn sketch / flat geometric / collage / photographic / 3D / custom).

## Step 6 — Structure

Ask which pages should exist at the root level beyond `home`. Default: `about`, `projects`, `blog`, `legal`. Offer to add custom pages (`/services`, `/contact`, etc.). For each extra page, call `/new-page` conceptually — but only after the wizard completes.

## Step 7 — Modules (one module per sub-question)

For each, ask Y/N and the sub-choice:

1. **Booking** → Cal.com / Calendly / custom / none.
2. **CRM / forms** → Brevo / Mailchimp / webhook / none.
3. **Analytics** → GA4 / Plausible / Umami / none.
4. **Cookie consent** → local minimal / tarteaucitron / none. If none and analytics are active → warn.
5. **Blog** → on / off.
6. **Podcast** (requires blog) → on / off.
7. **Illustrations IA** → on / off. If on, confirm the user has a Gemini API key.

Track the choices. For each active module, call `/setup-integration <name>` conceptually (the actual integration wiring happens now, not later).

## Step 8 — Claude Code toolbelt

For each tool, ask install now / skip / remind later:

- **Superpowers** plugin
- **UI/UX Pro Max** skill (local clone)
- **21st.dev** MCP (via `claude mcp add 21st-dev`) — or document the manual usage
- **MCP Canva / Gmail / Notion / Drive** — optional mention, do not push

Log the decisions in `docs/brand/toolbelt.md`.

## Step 9 — Hosting secrets

Ask for SFTP host, username, password, prod directory, staging directory. Set via `gh secret set`:

```
gh secret set OVH_HOST --body "<host>"
gh secret set OVH_USERNAME --body "<user>"
gh secret set OVH_PASSWORD --body "<pass>"
gh secret set OVH_PROD_DIR --body "<path>"
gh secret set OVH_STAGING_DIR --body "<path>"
```

Remind the user that passwords typed in terminals can leak into shell history — recommend using `gh secret set NAME` (without `--body`) which reads from stdin.

## Step 10 — Staging auth

Run `bash scripts/htpasswd-gen.sh`. The script writes credentials to `.staging-credentials.txt` with mode 600 (gitignored). Tell the user to open that file themselves, copy the password to their password manager, then delete the file. **Do not read the password aloud in your response — it ends up in the session transcript.**

Then run the three `gh secret set` calls the script tells them to run. Ask the user for the absolute server path to the staging `.htpasswd` (the workflow will place it there during deploy) and set it as `OVH_STAGING_HTPASSWD_PATH`. No manual editing of `.htaccess-staging` is needed — the workflow substitutes the path at deploy time.

## Step 11 — Git and GitHub

If `.git` doesn't exist, `git init -b main`. Stage everything except `.htpasswd`, `.env`, and any content of the gitignored docs folders. Commit as "feat: initial site setup via /start-new-site". Ask: GitHub repo? (name, public/private). Run `gh repo create <name> --public --source=. --remote=origin --push`. Create `staging` branch and push.

## Step 12 — First staging deploy

Switch to `staging`, merge `main` if needed, push. Run `gh run watch`. Print the staging URL with the credentials when the workflow succeeds.

## Step 13 — Server-side `.env`

Print the list of env vars (from `.env.example` + module-specific ones) that the user must SSH/SFTP into the host to create at the site root. Do not write the .env locally.

## Step 14 — Final checklist

Print a human-readable TODO list:
- [ ] Configure DNS for prod and staging domains
- [ ] Upload `.env` to the host (SSH / SFTP)
- [ ] Verify `https://<staging>/.env` returns 403
- [ ] Create the Brevo lists (if Brevo active) and paste list IDs into `.env`
- [ ] Validate Cal event slug (if Cal active)
- [ ] First smoke test on staging, including 404 page
- [ ] When satisfied, merge `staging` → `main` (or use `/deploy`)

Offer the next commands: `/new-page`, `/new-blog-article`, `/audit-brand`.
