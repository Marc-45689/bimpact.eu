# Toolbelt

Log of Claude Code tools installed on this project. Updated by the setup wizard and by `/setup-integration`.

## Installed

| Tool | Type | Installed | Status | Notes |
|---|---|---|---|---|
| UI/UX Pro Max | Skill | 2026-09-14 | active | Sparse-cloned `.claude/skills/ui-ux-pro-max/` (data + scripts + SKILL.md only) from `nextlevelbuilder/ui-ux-pro-max-skill` — no nested `.git`, no bundled `cli/`/`gallery`/fonts/extra skills. |
| Magnific (claude.ai connector) | MCP | 2026-09-14 | active | Account-level MCP (`mcp.magnific.com`), authenticated via `/mcp`. Not project-scoped — available in any Claude Code session on this account. Image/video/audio/3D generation. |

## Modules

| Module | Variant | Installed | Status | Notes |
|---|---|---|---|---|
| analytics | GA4 | 2026-09-14 | active | Measurement ID `G-PZEBPWJJFG`, not a secret (public client-side ID). Loaded by `assets/js/analytics.js`, gated behind cookie consent (`cookies:accepted` event / `bimpact_cookie_consent` localStorage key). `<!-- GA_START -->`/`<!-- GA_END -->` markers around the `<script>` tag in every page's `<head>` let `deploy-staging.yml` strip it so staging traffic never reaches GA. CSP: `script-src` allows `https://www.googletagmanager.com`; `connect-src` allows `https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com` (`.htaccess` only — `.htaccess-staging` has no CSP header at all today, pre-existing gap, not module-specific). |
| cookie-consent | local minimal | 2026-09-14 | active | `assets/js/cookie-consent.js` + `.cookie-banner` markup on every page (see `docs/components.md`). Opt-in (no cookie until "Accepter"), reopenable via the footer's "Gérer les cookies" button. No third-party host, no CSP change needed. |

## Reference

- **Superpowers** (Plugin) — `/plugin install superpowers@claude-plugins-official`
- **UI/UX Pro Max** (Skill) — clone to local skills path
- **21st.dev** (MCP) — `claude mcp add 21st-dev` (or manual usage: visit https://21st.dev/mcp, copy prompts)
- **Canva / Gmail / Notion / Drive** (MCP) — optional, install on demand

## Pending decisions

_tools mentioned during setup as "remind me later"_
