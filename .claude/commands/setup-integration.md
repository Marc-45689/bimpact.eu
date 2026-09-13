---
description: Activate a module on an existing site after setup. Usage: /setup-integration <booking|crm|analytics|cookie-consent|blog|podcast|illustrations>
---

You are piloting `/setup-integration`. Load the `starter-setup` skill.

## Step 1 — Identify the module

Parse the argument. If missing, ask the user which module:
- `booking` (Cal.com / Calendly)
- `crm` (Brevo / Mailchimp / webhook)
- `analytics` (GA4 / Plausible / Umami)
- `cookie-consent` (local minimal / tarteaucitron)
- `blog` (templates and catalog)
- `podcast` (Gemini TTS)
- `illustrations` (Gemini image)

## Step 2 — Ask sub-variant

If the module has alternatives, ask which. Store the answer.

## Step 3 — Apply

### booking

- **Cal.com:** inject the embed script and data-attributes into relevant CTAs, ask for the Cal username + event slug, set `CAL_USERNAME` and `CAL_EVENT_SLUG` in `.env.example`. Update CSP: add `https://app.cal.com https://cdn.cal.com` to `script-src` and `style-src`, `https://*.cal.com` to `connect-src`, `https://app.cal.com` to `frame-src`.
- **Calendly:** equivalent with `https://assets.calendly.com` + `https://calendly.com`.

### crm

- **Brevo:** copy `api/brevo.php.example` to `api/brevo.php` (or keep `.example` and instruct the user to configure it). Add a sample form to the home page that posts to `/api/brevo.php`. Add `BREVO_API_KEY` and `BREVO_LIST_DEFAULT` to `.env.example`. Update CSP to allow `https://cdn.brevo.com https://sibautomation.com` in `script-src` and `https://*.brevo.com https://sibautomation.com` in `connect-src`.
- **Mailchimp:** same pattern with a Mailchimp PHP proxy (`api/mailchimp.php`) and CSP entries.
- **Webhook:** configure `api/webhook.php` to POST to the user's n8n / Zapier / custom webhook URL.

### analytics

- **GA4:** add the gtag snippet in `<head>` wrapped in `<!-- GA_START --> ... <!-- GA_END -->` (so staging workflow can strip it). Add `GA4_MEASUREMENT_ID` to `.env.example`. Hook into `window.addEventListener('cookies:accepted', …)` if cookie consent is active. Update CSP `script-src` and `connect-src` for `https://www.googletagmanager.com`, `https://www.google-analytics.com`, `https://*.google-analytics.com`, `https://*.analytics.google.com`.
- **Plausible:** single `<script defer data-domain="…" src="https://plausible.io/js/script.js">`. Add `PLAUSIBLE_DOMAIN` to `.env.example`. CSP: `https://plausible.io` in `script-src` and `connect-src`.
- **Umami:** similar pattern with the Umami host and `UMAMI_WEBSITE_ID`.

### cookie-consent

- **Local minimal:** include `assets/js/cookie-consent.js` and the banner markup in the `<body>` of pages that load analytics.
- **tarteaucitron:** pin a specific version, compute SRI, update CSP for `https://cdn.jsdelivr.net`, include the tarteaucitron bootstrap.

### blog

Already scaffolded in Plan 1. This option is a no-op except to confirm the module is active (update `docs/brand/toolbelt.md`).

### podcast

Confirm `GEMINI_API_KEY` is set. Add `scripts/generate-podcast.py` if not present. Add the podcast player CSS + JS to `assets/css/blog.css` and the component block to `docs/components.md`.

### illustrations

Confirm `GEMINI_API_KEY` is set. Add `scripts/generate-image.py` if not present. Derive the prompt from the brand if `docs/brand/illustration-prompt.md` is still a placeholder.

## Step 4 — Log and commit

Append a row to the **Installed** table in `docs/brand/toolbelt.md`. Commit: `feat(integration): activate <module>`.

## Step 5 — Remind next steps

Tell the user which env vars need to be added on the server, which GitHub secrets (if any), and recommend `/deploy` to staging.
