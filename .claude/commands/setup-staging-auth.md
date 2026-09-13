---
description: Initialize or rotate the staging htpasswd credentials.
---

You are piloting `/setup-staging-auth`. Load the `starter-setup` skill.

## Step 1 — Warn

`.htpasswd` will be regenerated. Any previous staging credentials stop working as soon as the workflow deploys. Tell the user. Confirm before proceeding.

## Step 2 — Generate

Run:

```bash
bash scripts/htpasswd-gen.sh staging
```

The script:
- creates `.htpasswd` with user `staging` and a 20-char random password
- prints username and password once

Display the credentials to the user and tell them to save to their password manager **immediately**.

## Step 3 — Update .htaccess-staging if needed

If the `AuthUserFile` path in `.htaccess-staging` still contains `<your-host-user>`, ask the user for the absolute path on the SFTP host where `.htpasswd` will live. Replace the placeholder. Do not commit `.htpasswd` — it's gitignored.

## Step 4 — Deploy to staging

If the user is on `staging`, commit the updated `.htaccess-staging` (if it changed) and push. The workflow uploads the new `.htpasswd` to the host. Remind the user that they may need to upload `.htpasswd` via SFTP manually if the workflow doesn't include it (depends on their host's staging root layout).

## Step 5 — Verify

Ask the user to open the staging URL in an incognito window, confirm the auth prompt appears, and that the new credentials work.
