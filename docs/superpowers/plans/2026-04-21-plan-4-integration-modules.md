# Plan 4 — Integration modules (retrospective)

> **Status:** implemented. This document is retrospective for methodological consistency.

**Goal:** Ship the interaction modules (booking, CRM, analytics, cookie consent) as copy-pastable snippets consumed by `/setup-integration`.

**Architecture:** One markdown file per module variant under `docs/integrations/`. Each file lists required env vars, the HTML/JS snippet to insert, and the CSP delta. Server-side modules (Brevo, Mailchimp) provide env-safe PHP proxies via the `api/_env.php` loader, eliminating the "key in clear" anti-pattern from the parent `/site` project.

## Files created

- `docs/integrations/README.md`
- `docs/integrations/booking-cal.md`
- `docs/integrations/booking-calendly.md`
- `docs/integrations/crm-brevo.md`
- `docs/integrations/crm-mailchimp.md`
- `docs/integrations/analytics-ga4.md`
- `docs/integrations/analytics-plausible.md`
- `docs/integrations/analytics-umami.md`
- `docs/integrations/cookies-local.md`
- `docs/integrations/cookies-tarteaucitron.md`
- `api/brevo.php.example` — full env-safe Brevo proxy.

## Verification checklist

- [x] Every integration file documents: required env vars, HTML/JS snippet, CSP delta.
- [x] All server-side PHP proxies go through `require_once __DIR__ . '/_env.php';` and `getenv()`.
- [x] CORS `Access-Control-Allow-Origin` is scoped to `SITE_URL` (or a literal fallback), not `*`.
- [x] OPTIONS preflight returns 204 and exits.
- [x] Request method is restricted to POST.
- [x] Email inputs are validated with `filter_var(..., FILTER_VALIDATE_EMAIL)` before forwarding.
- [x] Error responses are non-bavarous (no stack trace, no paths).
- [x] Analytics snippets (GA4) are wrapped in `<!-- GA_START -->` / `<!-- GA_END -->` so the staging workflow strips them.
- [x] Analytics that load after consent hook into the `cookies:accepted` window event dispatched by the local cookie module.
- [x] `tarteaucitron.md` recommends serving assets locally with pinned version to avoid CDN CSP holes.

## Known limitations

- `/setup-integration` has not been exercised end-to-end. The CSP delta tables in the skill and the per-integration markdown files have not been cross-verified line-by-line — the first real run may uncover formatting drift. Minor.
