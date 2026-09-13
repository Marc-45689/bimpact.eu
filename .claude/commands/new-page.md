---
description: Create a new page that respects the brand, the design system, and reuses existing components. Updates nav, sitemap, and the components catalog.
---

You are piloting `/new-page`. Load the `starter-setup` skill.

## Step 1 — Load context

Read:
- `docs/brand/brand.md`
- `docs/brand/tone-of-voice.md`
- `assets/css/tokens.css`
- `docs/components.md`

Then glob the existing HTML pages to confirm which components are already in use. If a pattern is used twice and not yet in `components.md`, flag it to the user and offer to add it.

## Step 2 — Understand the request

The user passes a description as the slash command argument or in a follow-up message. Ask clarifying questions if needed (this is a good spot to invoke the `superpowers:brainstorming` skill if the scope is fuzzy). Extract:
- Purpose of the page (what should it accomplish for which audience)
- Sections in priority order
- Target URL (slug)
- Any CTAs and where they point
- SEO intent (keyword, canonical, social share image)

## Step 3 — Propose an outline

Present:
- Proposed file path (`<slug>/index.html` under the appropriate parent).
- Section list with the reused components (by class name) and any new components needed.
- Meta (title, description, canonical, OG tags, schema.org type applicable).
- Whether the page joins the nav, which nav position.
- Sitemap update planned.

Wait for user validation.

## Step 4 — Generate

Create the HTML page from the appropriate template (`projects/_template-project.html`, `blog/_template-article.html`, or the home as baseline). Apply the confirmed outline. For a new component, add scoped styles in `assets/css/<page>.css` (or reuse existing CSS file when it matches the page family). Update `<nav>` in every top-level HTML page if the new page joins the menu.

## Step 5 — Update the catalog and sitemap

- Add any new reusable component to `docs/components.md`.
- Add the new URL to `sitemap.xml` with the right priority and changefreq.
- If the page is a blog article, additionally update `blog/index.html` card list.

## Step 6 — Audit

Run `/audit-brand` on the new page. Report the results. Fix anything flagged.

## Step 7 — Commit

Stage and commit with a message like `feat: add <page name> page`. Do not push. Ask the user whether to deploy to staging now (`/deploy`).
