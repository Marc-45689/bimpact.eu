#!/usr/bin/env bash
# ═══════════════════════════════════════
# CPANEL GIT DEPLOYMENT — PRODUCTION
#
# Invoked by scripts/cpanel-deploy.sh after cPanel's "Git Version Control"
# pulls `main`. Runs from the git checkout directory itself, so it copies
# to a scratch directory first rather than mutating tracked files in place
# (a dirty working tree would break the next `git pull`).
#
# Mirrors scripts/cpanel-deploy-staging.sh, minus the staging-only
# transforms (no noindex injection, no GA-block stripping, sitemap.xml
# and the real .htaccess ship as-is) since this checkout's files are
# already the production versions.
#
# Usage: scripts/cpanel-deploy-production.sh /absolute/path/to/prod/docroot
# ═══════════════════════════════════════

set -euo pipefail

DEPLOYPATH="${1:?Usage: cpanel-deploy-production.sh <deploy-path>}"
SRC="$(pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

rsync -a --exclude='.git' "$SRC"/ "$TMP"/
cd "$TMP"

rm -rf .git .claude .github .superpowers .cpanel.yml \
       .htaccess-staging robots-staging.txt \
       .env.example SETUP.md CLAUDE.md
find docs -type f ! -name "*.pdf" -delete 2>/dev/null || true
find docs -type d -empty -delete 2>/dev/null || true

# See cpanel-deploy-staging.sh for why: cPanel's deployment task shell can
# leave a restrictive umask that produces an unreadable .htaccess.
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

rsync -a --delete "$TMP"/ "$DEPLOYPATH"/
