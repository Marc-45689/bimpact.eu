#!/usr/bin/env bash
# ═══════════════════════════════════════
# CPANEL GIT DEPLOYMENT — DISPATCHER
#
# Invoked by .cpanel.yml, which is identical on `staging` and `main` so
# that merging one into the other never conflicts on that file. This
# script picks the right deploy target and payload transforms by reading
# whichever branch cPanel's "Git Version Control" actually checked out
# on the host, then hands off to the branch-specific script.
# ═══════════════════════════════════════

set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"

case "$BRANCH" in
  staging)
    exec /bin/bash scripts/cpanel-deploy-staging.sh /home/foma0863/staging.bimpact.eu/
    ;;
  main)
    exec /bin/bash scripts/cpanel-deploy-production.sh /home/foma0863/public_html/
    ;;
  *)
    echo "cpanel-deploy.sh: no deploy target configured for branch '$BRANCH'" >&2
    exit 1
    ;;
esac
