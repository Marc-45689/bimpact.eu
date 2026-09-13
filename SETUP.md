# Manual setup (fallback without Claude Code)

Mirrors what `/start-new-site` does, for users who prefer manual setup or want to understand the moving parts.

## Prerequisites

- Git + GitHub CLI (`gh`) logged in.
- Python 3 for scripts (Plan 3+).
- SFTP credentials for your host.
- Apache with `mod_rewrite`, `mod_headers`, `mod_deflate`, `mod_expires`, `mod_mime` enabled (standard on any shared PHP 8+ host).
- `htpasswd` available locally (macOS ships it; Debian/Ubuntu: `apt-get install apache2-utils`).

## Step 1 — Clone

    gh repo create <your-site> --template <this-repo> --public --clone
    cd <your-site>

## Step 2 — Brand

1. Fill `docs/brand/brand.md` and `docs/brand/tone-of-voice.md`.
2. Replace palette and fonts in `assets/css/tokens.css` to match `brand.md`.
3. Drop your logo as `logo-principal.svg` and your favicon files under `assets/`.
4. Update the canonical domain in `index.html`, `sitemap.xml`, the `.htaccess` (non-www canonical block), and the robots files.

## Step 3 — SFTP secrets

    gh secret set OVH_HOST --body "sftp.host.example"
    gh secret set OVH_USERNAME --body "..."
    gh secret set OVH_PASSWORD --body "..."
    gh secret set OVH_PROD_DIR --body "/www/"
    gh secret set OVH_STAGING_DIR --body "/staging/"

## Step 4 — Staging auth

    bash scripts/htpasswd-gen.sh

Save the credentials in your password manager. The generated `.htpasswd` stays local (gitignored) and is uploaded to the staging host by the workflow.

Update `.htaccess-staging` — replace `/home/<your-host-user>/staging/.htpasswd` with the actual absolute path on your host.

## Step 5 — First staging deploy

    git checkout -b staging
    git push -u origin staging
    gh run watch

Open the staging URL (username + password from Step 4).

## Step 6 — Production

    git checkout main
    git merge staging
    git push origin main
    gh run watch

## Step 7 — Server-side `.env`

SSH or SFTP into your host. At the site root (where `index.html` lives), create a `.env` file with the keys from `.env.example`, filled in. This is read by PHP endpoints in `api/`.

Make sure `.env` is not served publicly. Apache denies dotfiles by default; verify by requesting `https://yourdomain.com/.env` — it must return 403.

---

More details in the design spec: `docs/superpowers/specs/2026-04-21-claude-site-starter-design.md`.
