---
description: Full pipeline for a new blog article — outline, draft, illustration (Gemini), optional two-voice podcast (Gemini TTS NotebookLM-style), blog index update, sitemap.
---

You are piloting `/new-blog-article`. Load the `starter-setup` skill.

## Step 1 — Context

Read brand context. Glob `blog/*.html` to see the most recent articles and absorb the style. Load `docs/brand/illustration-prompt.md` and `docs/brand/tone-of-voice.md`.

## Step 2 — Topic and outline

Ask the user for a title or a subject. If ambiguous, invoke the `superpowers:brainstorming` skill. Propose an outline:
- Title (SEO-friendly, under 60 chars)
- Slug
- Reading time target
- H2/H3 structure with the angle and key arguments per section
- Suggested blockquotes, callouts, CTA inline placement
- Final FAQ (3-5 questions) for rich snippets
- Meta description (150-160 chars)

Wait for user validation.

## Step 3 — Draft

Write the article into `blog/<slug>/index.html` using the `_template-article.html` as a starting point. Respect `tone-of-voice.md` rigidly. Use the blog components from `docs/components.md`:
- `<blockquote>` for third-party quotes
- `.article-callout` for author insights
- `.article-code-block` for code with copy button
- `.article-img-left` / `.article-img-right` / `<figure class="article-img-center">` for image layouts
- `.table-wrapper` for tables
- `.article-cta-inline` placed after the third H2 or at a natural break
- `.article-faq` near the end

Update the `<title>`, meta description, canonical, OG tags, `og:image`, JSON-LD Article schema, and breadcrumb.

## Step 4 — Illustration (if module active)

Derive `{{subject_description}}` from the article angle. Call:

```bash
python3 scripts/generate-image.py \
  --slug "<slug>" \
  --subject "<subject_description>"
```

The script reads the prompt template from `docs/brand/illustration-prompt.md`, calls Gemini Image, saves `assets/illustrations-blog/<slug>.webp` at 1200×675, background corrected to match the primary palette token.

Insert the illustration into the article cover `<img>`. Ensure `alt` text is descriptive (not decorative).

## Step 5 — Podcast (if module active)

Call:

```bash
python3 scripts/generate-podcast.py blog/<slug>/index.html
```

The script extracts the article text, asks Gemini to generate a two-voice dialogue script (NotebookLM-style: two hosts, conversational, 4-6 min), synthesizes both voices via Gemini TTS, and produces `assets/audio-blog/<slug>.mp3` via ffmpeg.

Insert the podcast player block in the article (after the cover, before the first H2). The HTML + minimal JS for the player is in `docs/components.md` under "Blog-specific → Podcast player".

## Step 6 — Blog index update

Open `blog/index.html`. Prepend a new card in the grid (most recent first). Use the illustration as the card thumbnail. Meta line: date (YYYY-MM-DD) · reading time.

## Step 7 — Sitemap

Add the new URL to `sitemap.xml`:

```xml
<url>
    <loc>https://<domain>/blog/<slug></loc>
    <priority>0.7</priority>
    <changefreq>monthly</changefreq>
</url>
```

## Step 8 — Audit

Run `/audit-brand` on the article. Fix anything flagged.

## Step 9 — Commit

Stage and commit: `feat: publish article <title>`. Suggest `/deploy` to push staging.
