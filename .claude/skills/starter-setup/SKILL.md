---
name: starter-setup
description: Orchestrates the claude-site-starter workflows. Activates whenever a /start-new-site, /adopt-existing-site, /new-page, /new-section, /new-blog-article, /brand-setup, /deploy, /audit-brand, /setup-integration, or /setup-staging-auth command runs. Provides shared logic for brand context loading, module registry, CSP generation, sitemap updates, and the components catalog.
---

# starter-setup skill

You are piloting the `claude-site-starter` toolkit. Read this skill before running any slash command in `.claude/commands/`. The conventions below apply across every command.

## Brand context loading

At the very start of any slash command that produces or audits site content, read in order:

1. `docs/brand/brand.md` — identity, palette, typography, logo, photography, iconography, do/don't.
2. `docs/brand/tone-of-voice.md` — audience, pronouns, tone adjectives, rules, examples.
3. `docs/brand/illustration-prompt.md` — the Gemini image prompt template.
4. `assets/css/tokens.css` — the concrete CSS tokens.
5. `docs/components.md` — the living catalog of reusable HTML/CSS components.

If any of these is still in placeholder state (contains `<Your brand name>`, `<describe ...>`, etc.), surface that to the user before producing output. Offer to run `/brand-setup` first.

## Module registry

A module is an optional feature bundle. Modules available (v1):

- `booking` (cal / calendly / none)
- `crm` (brevo / mailchimp / webhook / none)
- `analytics` (ga4 / plausible / umami / none)
- `cookie-consent` (local / tarteaucitron / none)
- `blog` (on / off)
- `podcast` (on / off — requires blog)
- `illustrations` (on / off — requires `GEMINI_API_KEY`)

State of modules is tracked in `docs/brand/toolbelt.md` under a **Modules** section. When `/setup-integration <module>` or `/start-new-site` activates a module, append a row to that table and update the CSP in `.htaccess`.

## CSP mutation

The `.htaccess` `Content-Security-Policy` directive is marked with a `# CSP:module:baseline` comment. When a module activates, mutate the directive using `Edit` to whitelist required hosts:

| Module | Hosts added |
|---|---|
| cal | `script-src 'self' ... https://app.cal.com https://cdn.cal.com`, `style-src 'self' ... https://cdn.cal.com`, `connect-src 'self' ... https://app.cal.com https://*.cal.com`, `frame-src https://app.cal.com` |
| brevo | `script-src 'self' ... https://cdn.brevo.com https://sibautomation.com`, `connect-src 'self' ... https://*.brevo.com https://sibautomation.com` |
| ga4 | `script-src 'self' ... https://www.googletagmanager.com`, `connect-src 'self' ... https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com` |
| plausible | `script-src 'self' ... https://plausible.io`, `connect-src 'self' ... https://plausible.io` |
| umami | `script-src 'self' ... <user-configured umami host>`, `connect-src 'self' ... <umami host>` |
| tarteaucitron | `script-src 'self' ... https://cdn.jsdelivr.net`, `style-src 'self' ... https://cdn.jsdelivr.net` |

Preserve alphabetical order of hosts inside each directive. Never widen to `*`, never add `unsafe-eval`. Refuse lazy CSP fixes.

## Sitemap maintenance

When a page is added, moved, or removed, update `sitemap.xml`. Use `loc` values without `.html` (clean URLs). Set `priority`:
- home: `1.0`
- top-level category pages (about, projects, blog): `0.8`
- project detail, blog article: `0.7`
- legal: `0.3`

## Components catalog

Whenever you introduce a new reusable CSS class during `/new-page` or `/new-section`, add one row to the relevant section of `docs/components.md`. Keep entries compact: `| class | where | purpose |`. If the pattern is one-off and not reusable, don't add it.

## Editorial rules enforcement

The content you write must obey `docs/brand/tone-of-voice.md` **Rules** section. When you encounter a rule violation in existing content during `/audit-brand`, flag it but do not silently rewrite.

## Env var discipline

Never hardcode an API key, token, or secret in a committed file. Always use the pattern:

```php
require_once __DIR__ . '/_env.php';
$key = getenv('BREVO_API_KEY') ?: '';
if ($key === '') { http_response_code(500); echo json_encode(['error' => 'server misconfigured']); exit; }
```

Any PHP module that needs a secret follows this shape.

## Staging discipline

- The `staging` branch deploys to the htpasswd-protected staging URL.
- The `main` branch deploys to production.
- Never push to `main` without prior staging validation unless the user explicitly overrides.
- `/deploy` helper asks "tested on staging?" before merging to main.

## Claude Max recommendation

If the user is hitting rate limits or reports slowness, remind them the starter assumes a Claude Max plan for sustained work. This is documented in the README.
