---
description: Add a new section to an existing page. Same discipline as /new-page, smaller scope.
---

You are piloting `/new-section`. Load the `starter-setup` skill.

## Step 1 — Context

Read brand context (see `/new-page` step 1). Identify the target page. Open its HTML. Identify where the new section will live (before / after which existing section).

## Step 2 — Outline

Present the proposed section: purpose, structure (sub-sections, components, CTAs), insertion point, any new CSS classes. Wait for validation.

## Step 3 — Generate

Insert the HTML block at the chosen location. Add CSS to the page's CSS file if needed. If a new reusable class is born, add it to `docs/components.md`.

## Step 4 — Audit + commit

Run `/audit-brand` on the page, then commit `feat: add <section name> to <page>`.
