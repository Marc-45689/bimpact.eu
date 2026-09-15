#!/usr/bin/env bash
# ═══════════════════════════════════════
# CPANEL GIT DEPLOYMENT — STAGING
#
# Invoked by .cpanel.yml after cPanel's "Git Version Control" pulls this
# branch. Runs from the git checkout directory itself, so it copies to a
# scratch directory first rather than mutating tracked files in place
# (a dirty working tree would break the next `git pull`).
#
# Mirrors the "Prepare staging payload" step from the old GitHub Actions
# lftp-based deploy-staging.yml, which can't reach this host: o2switch
# blocks inbound port 22 by IP allowlist, and GitHub Actions runners use
# rotating IPs that can't be whitelisted. This has the o2switch server
# pull from GitHub over outbound HTTPS instead, which isn't restricted.
#
# Usage: scripts/cpanel-deploy-staging.sh /absolute/path/to/staging/docroot
# ═══════════════════════════════════════

set -euo pipefail

DEPLOYPATH="${1:?Usage: cpanel-deploy-staging.sh <deploy-path>}"
SRC="$(pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

rsync -a --exclude='.git' "$SRC"/ "$TMP"/
cd "$TMP"

cp robots-staging.txt robots.txt
find . -name "*.html" -exec sed -i 's/<head>/<head><meta name="robots" content="noindex, nofollow">/' {} \;
rm -f sitemap.xml
find . -name "*.html" -exec sed -i '/<!-- GA_START -->/,/<!-- GA_END -->/d' {} \;
cp .htaccess-staging .htaccess

rm -rf .git .claude .github .superpowers .cpanel.yml \
       .htaccess-staging robots-staging.txt \
       .env.example SETUP.md CLAUDE.md
find docs -type f ! -name "*.pdf" -delete 2>/dev/null || true
find docs -type d -empty -delete 2>/dev/null || true

# cPanel's deployment task shell can leave a restrictive umask, which
# produces an unreadable .htaccess (Apache then 403s the whole site with
# "unable to read htaccess file, denying access to be safe"). Normalize
# to standard docroot permissions before publishing.
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

rsync -a --delete --exclude='.htpasswd' "$TMP"/ "$DEPLOYPATH"/
