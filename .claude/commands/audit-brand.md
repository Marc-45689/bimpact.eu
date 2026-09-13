---
description: Audit a page (or the whole site) against brand tokens, editorial rules, SEO, accessibility, and CSP coherence. Report violations without auto-rewriting.
---

You are piloting `/audit-brand`. Load the `starter-setup` skill.

## Scope

If the user passes a path (e.g. `blog/example-article/index.html`), audit only that file. Otherwise audit every HTML file.

## Checks

### 1. Design tokens

- Any hex color in inline styles or CSS that is **not** declared in `assets/css/tokens.css` → flag. Exception: `rgba()` opacity variants that reference a token color.
- Any `font-family` in inline styles → flag unless it references `var(--font-display)` or `var(--font-body)`.

### 2. Editorial rules

Read `docs/brand/tone-of-voice.md` rules. For each forbidden item in the rules (emojis, em-dashes, banned terms), scan every HTML for violations → flag with line number.

For each required item (stats sourced, currency, GDPR mentions where relevant), heuristically check and flag absence where contextually expected.

### 3. SEO

Per page:
- `<title>` present, non-empty, < 60 chars
- `<meta name="description">` present, 120-170 chars
- `<link rel="canonical">` present, matches expected URL
- `<meta property="og:type">`, `og:url`, `og:title`, `og:image` present
- JSON-LD schema present for home (Organization), article (Article), category pages (BreadcrumbList where applicable)
- All internal links: no `.html` suffix (clean URLs)

### 4. Accessibility

- Every `<img>` has `alt`, `width`, `height`.
- Above-the-fold images use `loading="eager"`, others `loading="lazy"`.
- `<h1>` appears exactly once per page.
- Heading hierarchy not skipped (no `<h1>` then `<h3>` without `<h2>`).
- Forms: every `<input>` has an associated `<label>`.
- Buttons without text have `aria-label`.

### 5. CSP coherence

Parse the `Content-Security-Policy` header in `.htaccess`. For every `<script src="https://…">` in every HTML page, confirm the host is whitelisted in `script-src`. Same for `<link rel="stylesheet" href="https://…">` vs `style-src`, fonts vs `font-src`, iframes vs `frame-src`, XHR / fetch targets vs `connect-src`. Flag mismatches.

### 6. Secrets

`grep -iE "(api[_-]?key|token|secret|password)\\s*=" -r .` excluding `.git`, `.gitignore`, `.env.example`. Anything that looks like a real value rather than a placeholder → flag as a potential leak.

## Output

Print a markdown report with sections per check. For each violation:
- File path + line (when applicable)
- What's wrong
- Suggested fix

Do **not** auto-rewrite content. Let the user decide.

Finish with a summary: count of issues by severity (critical / warning / info).
