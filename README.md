# claude-site-starter

An opinionated, CMS-free, Claude Code-native starter for marketing websites. Static HTML + CSS + JS, SFTP deploy, AI-assisted content (blog illustrations and two-voice podcasts NotebookLM-style via Gemini).

> This is a personal, opinionated starter. Fork it, copy it, adapt it. Issues and PRs are not actively monitored — if you want to change something, change it in your fork. Inspired by the same "fork and run" usage model as [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).

---

## Install (copy / paste)

Use the green **"Use this template"** button on GitHub, or run:

```bash
gh repo create my-site --template Littlpinguin/claude-site-starter --public --clone
cd my-site
claude
```

Then in Claude Code:

```
/start-new-site
```

No template helper? Clone manually:

```bash
git clone --depth 1 https://github.com/Littlpinguin/claude-site-starter.git my-site
cd my-site
rm -rf .git
git init -b main
claude
```

---

## Before you start (the disclaimer)

> This starter produces a functional skeleton. It does not produce a beautiful site on its own. Qualitative output requires a defined brand universe: typography, colors, logo, photos/assets, copy, editorial voice. Invest time here first, or the rest will feel generic.

---

## Philosophy

- **Static-first.** HTML + CSS + JS vanilla. No framework, no bundler, no build.
- **Brand-first.** See disclaimer above.
- **Claude Code-native.** Slash commands, skills, and conventions designed for a human + Claude pair.
- **SFTP deploy.** Any $3-5 / month shared PHP 8+ host works.
- **AI-assisted content.** Blog illustrations and two-voice podcasts generated in your brand with Gemini.

---

## Requirements

- SFTP host with PHP 8+ (OVH, o2switch, Infomaniak, LWS…)
- GitHub account
- [Claude Code](https://claude.com/claude-code) installed
- **Claude Max plan recommended** ($100+/month). This workflow relies heavily on Claude for brainstorming, planning, implementation, and audits. A Pro plan will hit rate limits quickly on a real project. Max makes this method sustainable.
- Optional API keys: Gemini (illustrations + podcast), Brevo, Cal.com

---

## Quickstart — new site

```
claude
/start-new-site
```

The wizard walks you through: brand, structure, modules (booking, CRM, analytics, cookie consent, blog, podcast, illustrations), Claude Code toolbelt (Superpowers, UI/UX Pro Max, 21st.dev), SFTP secrets, staging auth, first deploy.

## Quickstart — adopt an existing repo or site

```
claude
/adopt-existing-site
```

Three scenarios handled automatically:
- **Static site** → injects the methodology (`.claude/`, workflows, `docs/superpowers/`, design tokens, headers) while preserving your existing structure.
- **Framework (Next.js, Astro, …)** → overlays the Claude Code layer only. Your build stays.
- **CMS (WordPress, Webflow, Squarespace, …)** → assisted migration to static, page by page, with URL redirects preserved.

---

## What you get

| Module | Default | Alternatives |
|---|---|---|
| Static pages | Home, About, Projects, Blog, Legal (privacy/terms/cookies), 404 | — |
| Design tokens | `tokens.css` with palette, fonts, spacing, radii | — |
| Booking | Cal.com embed | Calendly, custom, none |
| CRM / forms | Brevo via env-safe PHP proxy | Mailchimp, webhook, none |
| Analytics | Plausible or GA4 | Umami, none |
| Cookie consent | Minimal local, or tarteaucitron | none |
| Blog | Templates + component library | — |
| Illustrations IA | Gemini image, brand-aware prompt | none |
| Podcast | Gemini TTS, two-voice dialogue NotebookLM-style | none |
| Deployment | GitHub Actions → SFTP via `lftp` | — |
| Staging protection | `.htpasswd` + noindex + GA stripped | — |
| Security | HSTS, strict CSP, anti-clickjacking headers, env-based secrets | — |
| SEO | sitemap auto-maintained, schema.org JSON-LD per page type, clean URLs | — |

---

## Create a new page later

```
claude
/new-page "Services page with three offers, testimonials, and a FAQ"
```

Claude reads your `docs/brand/brand.md`, `tone-of-voice.md`, the CSS tokens, and `docs/components.md`, then scaffolds the page using existing components, suggests new ones if needed, and updates the nav + sitemap.

Other commands: `/new-section`, `/new-blog-article`, `/brand-setup`, `/audit-brand`, `/deploy`, `/setup-integration`, `/setup-staging-auth`.

---

## Improving your site with Lighthouse

Think of Claude Code as a senior webmaster and designer on your team:

1. Deploy to staging.
2. Run Google Lighthouse in Chrome DevTools (F12 → Lighthouse → Analyze page).
3. Copy the Opportunities and Diagnostics sections (Performance, SEO, Accessibility, Best Practices).
4. Paste to Claude:
   > Here are Lighthouse findings for my staging URL. Fix the ones that apply to our starter conventions. Propose changes before applying.
5. Claude proposes a plan, you approve, it implements.
6. Re-test on staging. When Lighthouse is happy, merge `staging` → `main`.

Same loop for content rewrites, new sections, brand audits, or performance regressions.

---

## Security

This starter ships with hardened defaults: HSTS, strict CSP generated from active modules, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP, clean URLs, `.htpasswd`-protected staging, noindex enforcement, env-based secrets with a dedicated PHP loader, OPTIONS preflight on PHP APIs, input validation, pinned CDN dependencies with SRI.

AI-assisted development adds its own pitfalls. Keep these in mind:

**Before every commit**
- Review Claude's diffs yourself. Pay extra attention to files under `api/`, `.env*`, `.github/workflows/`, `.htaccess`, and `.claude/settings*.json`.
- Never paste real API keys in a message to Claude. Use `.env` + `.env.example` with placeholders.
- Before pushing, grep the diff for secrets: `git diff | grep -iE "key|token|password|secret"`.

**Permissions**
- `.claude/settings.local.json` accumulates allowed commands over time. Prune periodically. Remove anything you don't recognize.
- Do not grant broad `Bash(rm:*)`, `Bash(git push --force:*)`, or unrestricted `WebFetch(*)`. Scope narrowly.

**Deployment discipline**
- Never deploy straight to production. Stage first.
  - `main` → production
  - `staging` → staging (htpasswd-protected, noindex, no analytics)
- If it fails on staging, it doesn't go to production.

**Staging authentication (required)**
A public staging URL without basic auth is a data and SEO risk. `/start-new-site` provisions `.htpasswd` for you. To rotate later:

```
claude
/setup-staging-auth
```

**Dependencies**
- CDN scripts are pinned and include Sub-Resource Integrity hashes. Do not replace with "latest" without updating the SRI hash.
- Before adding a new external script, update the CSP in `.htaccess` and let Claude compute the SRI hash.

**AI-specific traps**
- Claude can hallucinate package names, URLs, or function signatures. Verify before trusting.
- Refuse lazy CSP fixes ("add `unsafe-eval` to make this work"). Find the right way.
- Read any skill or MCP server's code before granting it broad permissions.
- Do not share Claude transcripts publicly if they contain internal URLs, paths, or private assets.

---

## Example

A site built with this methodology: **https://jessem.fr** (Jessy Martin Consulting).

_Screenshots and a short walkthrough GIF of `/start-new-site` will land here once the first dogfood run is complete._

---

## A note on AI-generated content

If you enable the illustration or podcast modules, images and audio are generated by Gemini. Before shipping, confirm for yourself:

- **Terms of service.** Gemini's usage policies apply. Review them for your jurisdiction and industry.
- **Copyright and style.** AI-generated illustrations are fine for marketing use in most jurisdictions, but emulating a living artist's recognizable style is risky. The default prompt is abstract / editorial on purpose.
- **Voice and GDPR.** The two-voice podcast uses Gemini's pre-trained voices. They are synthetic, not cloned from a real person. You don't need consent for these voices specifically, but if you swap them for cloned voices, consent becomes mandatory.
- **Disclosure.** Good practice: mention that the podcast is AI-generated in the article, and that illustrations are AI-assisted in an about or colophon page. Some jurisdictions make this mandatory.

The starter will not do this disclosure for you. It's your call.

---

## Stack

- HTML / CSS / JS vanilla — no framework, no bundler
- PHP 8+ for API proxies (Brevo, webhooks) with env-safe secret loading
- GitHub Actions → SFTP via `lftp`
- Apache `.htaccess` (security headers, clean URLs, cache, compression)
- Optional: Gemini API (illustrations + podcast TTS), Cal.com, Brevo, Plausible / GA4 / Umami
- Claude Code skills & MCPs: Superpowers, UI/UX Pro Max, 21st.dev

---

## Usage, forking, contributions

This is not a collaboratively-maintained project. Fork it freely, adapt anything, ship your own site. The code is MIT-licensed, so you owe nothing.

Issues and pull requests on this repository are not actively monitored. If you find a bug that breaks the starter out of the box, feel free to open an issue — but don't expect a response. Fork first, ask later.

See `SETUP.md` for the manual path (no Claude Code required).
See `docs/superpowers/specs/` for the full design.

---

## License

MIT — see `LICENSE`.
