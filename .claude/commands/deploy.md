---
description: Helper for the staging → production deploy discipline. Commits uncommitted work, pushes to staging, or merges staging into main with an explicit validation step.
---

You are piloting `/deploy`. Load the `starter-setup` skill.

## Step 1 — Locate

Check `git status` and the current branch.

## Step 2 — Branch logic

### If on `staging`

- If uncommitted changes exist, propose `git add -A`, show the diff summary, ask for a commit message, commit.
- `git push origin staging`.
- Run `gh run watch` (if available) to display the workflow status.
- On success, print the staging URL with a reminder of the htpasswd credentials (never re-display the password — just tell them to check their password manager).

### If on `main`

**Ask the user first:** "Has the change been tested on staging?". If no, refuse to proceed and propose switching to `staging` instead.

If yes:
- `git merge staging --no-ff -m "merge: staging to production"` (or fast-forward if history is clean).
- `git push origin main`.
- Run `gh run watch`.
- On success, print the production URL.

### If on any other branch

- Remind the user that deployment only goes through `main` or `staging`. Propose merging the current branch into `staging` for validation first.

## Step 3 — Safety notes

- Never `git push --force` on `main`.
- Never skip hooks (`--no-verify`) unless the user explicitly asks.
- If a workflow fails, read the logs, show the user, do not silently retry.
