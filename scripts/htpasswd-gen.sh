#!/usr/bin/env bash
# ═══════════════════════════════════════
# STAGING .htpasswd CREDENTIALS GENERATOR
#
# Generates a random staging password and writes the credentials to
# .staging-credentials.txt (gitignored). Does NOT print the password to
# stdout — so Claude Code transcripts and shell history don't capture it.
#
# Next steps after running:
#   1. Open .staging-credentials.txt in your editor, save to your password manager.
#   2. Delete .staging-credentials.txt.
#   3. Configure GitHub Actions secrets:
#        gh secret set STAGING_HTPASSWD_USER --body "<user>"
#        gh secret set STAGING_HTPASSWD_PASS      # reads stdin, paste the password
#        gh secret set OVH_STAGING_HTPASSWD_PATH --body "/absolute/path/to/staging/.htpasswd"
#   4. Push to staging — the workflow will generate .htpasswd on the server.
# ═══════════════════════════════════════

set -euo pipefail

USER="${1:-staging}"
PASS="$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 20)"
CRED_FILE=".staging-credentials.txt"

cat > "$CRED_FILE" <<EOF
# Staging credentials — generated $(date -u +"%Y-%m-%dT%H:%M:%SZ")
# SAVE THESE TO YOUR PASSWORD MANAGER, THEN DELETE THIS FILE.
username: $USER
password: $PASS
EOF

chmod 600 "$CRED_FILE"

cat <<EOF
Credentials written to: $CRED_FILE (mode 600)

NEXT STEPS
  1. Open $CRED_FILE, copy to your password manager.
  2. rm $CRED_FILE
  3. Set the GitHub Actions secrets:
       gh secret set STAGING_HTPASSWD_USER --body "$USER"
       gh secret set STAGING_HTPASSWD_PASS     # paste the password when prompted (no --body flag)
       gh secret set OVH_STAGING_HTPASSWD_PATH --body "/absolute/server/path/to/staging/.htpasswd"
  4. Push to staging. The workflow generates .htpasswd on the server automatically.

The password was intentionally NOT printed here to keep it out of shell history
and Claude Code transcripts.
EOF
