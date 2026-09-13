---
description: Analyze an existing website or repository and inject the claude-site-starter methodology. Adapts to the detected stack (static, framework, or CMS).
---

You are piloting `/adopt-existing-site`. Load the `starter-setup` skill before continuing. You adapt, you do not migrate the user's codebase unless they are on a CMS and explicitly choose migration.

## Step 1 — Collect sources

Ask the user for:
- Path to a local repo (optional)
- Live production URL (optional)
- Both are fine.

## Step 2 — Detect stack

Inspect the repo (if provided) and the live URL. Classify:

- **Static site** → HTML + CSS + JS, no `package.json`, no `wp-config.php`, no obvious framework artifacts.
- **Modern framework** → `package.json` with `next` / `astro` / `gatsby` / `eleventy` / `vite`.
- **CMS** → `wp-config.php`, `wp-content/`, `/wp-json/` exposed, `<meta name="generator" content="WordPress">`, Webflow / Squarespace / Wix markers in the HTML.
- **Unknown** → ask the user.

Print the detection result and the proposed strategy.

## Step 3 — Branch by scenario

### Scenario A — Static site (adapt)

1. **Analyze the design system**. Read all CSS files. Extract recurring color hex values, font-families, border-radius, spacing. Compare against `tokens.css`. Produce a proposed `assets/css/tokens.css` that formalizes the user's existing values.
2. **Analyze content**. List pages, navigation, recurring components (nav, footer, hero, cards, CTA, FAQ). Dump to `docs/brand/extracted.md`.
3. **Propose injection plan**. Show a diff: what gets added (`.claude/`, `.github/workflows/`, `docs/superpowers/`, `docs/brand/*.md`, `tokens.css` if approved, `.htaccess` merge if they don't already have one) and what stays untouched. Confirm step by step.
4. **Execute**. Apply the diff with validation after each file.
5. **CSP reconciliation**. If their `.htaccess` already has a CSP, merge with the starter baseline without widening.

### Scenario B — Modern framework (overlay)

1. Add only: `.claude/`, `docs/superpowers/`, `docs/brand/`, `docs/components.md`, `.claude/skills/starter-setup/`.
2. Do **not** add `.github/workflows/deploy-*.yml` — their framework likely has its own deploy.
3. Do **not** modify their build.
4. Ask if they want a secondary SFTP pipeline alongside (rare — only if they're deploying on Vercel + want a mirror).

### Scenario C — CMS (propose migration to static)

1. Warn explicitly: "This starter is static-first. Staying on your CMS means most of the value here is inaccessible. I can guide a migration to static page by page."
2. If the user agrees to migrate:
   1. Fetch `<domain>/sitemap.xml` (or `/wp-sitemap.xml`). List every URL.
   2. For each URL, WebFetch the rendered HTML. Extract textual content, meta tags, images (download local to `docs/migration/assets/`), slugs.
   3. Dump content per page into `docs/migration/<slug>.md` with the extracted text and the meta.
   4. Build `docs/migration/url-mapping.md`: old URL → new URL.
   5. For each page, **one at a time**, reconstruct the HTML static version in the starter structure using the detected tokens and existing components. **Wait for user validation between pages.** Never batch.
   6. Generate `.htaccess` `Redirect` or `RewriteRule` entries for every old URL → new URL to preserve SEO.
   7. Document in `docs/migration/gaps.md` the features that cannot be reproduced statically (dynamic plugins, form builders, e-commerce, membership, search) with static-friendly alternatives: Brevo for forms, Cal.com for booking, Snipcart / LemonSqueezy for light commerce, Algolia DocSearch or Pagefind for site search.
3. If the user declines migration: stop, offer Scenario B (overlay only), and flag the trade-off.

## Step 4 — Finalize

After any scenario, run `/audit-brand` on the affected pages, commit to a new branch `adopt/<date>`, and let the user review before merging.
