# Plan 3 — Content modules (retrospective)

> **Status:** implemented. This document is retrospective for methodological consistency.

**Goal:** Ship the blog component library, the AI-assisted illustration pipeline, the two-voice podcast pipeline, and the sitemap maintenance script.

**Architecture:** Three Python scripts in `scripts/`, all reading brand context (palette, prompt template) from `docs/brand/`. `generate-image.py` uses Gemini Imagen 3 (model configurable via `GEMINI_IMAGE_MODEL`). `generate-podcast.py` uses Gemini 2.5 Flash for dialogue generation and Gemini 2.5 Flash Preview TTS with two voices (Kore + Puck by default, configurable via env). `sitemap-update.py` walks the filesystem and regenerates `sitemap.xml`. Blog CSS in `assets/css/blog.css` defines the full component library (blockquote, callout, code-block, table-wrapper, image variants, CTA inline, FAQ accordion, podcast player). `docs/components.md` documents the catalog including copy-pastable HTML snippets for the FAQ accordion and podcast player.

## Files created

- `scripts/generate-image.py` — Imagen 3 → WebP 1200×675 with palette-aligned background normalization.
- `scripts/generate-podcast.py` — Gemini dialogue + TTS → MP3 via ffmpeg concat.
- `scripts/sitemap-update.py` — filesystem-driven sitemap regeneration.
- `assets/audio-blog/README.md`.

## Files updated

- `assets/css/blog.css` — extended with full component set (286 lines vs initial 60).
- `docs/components.md` — catalog + ready-to-paste HTML/JS snippets.

## Verification checklist

- [x] All three scripts are executable (`chmod +x`).
- [x] Model IDs are env-configurable (`GEMINI_IMAGE_MODEL`, `GEMINI_TEXT_MODEL`, `GEMINI_TTS_MODEL`, `GEMINI_TTS_VOICE_A`, `GEMINI_TTS_VOICE_B`).
- [x] Scripts fail early with clear messages when `GEMINI_API_KEY` or required binaries (`cwebp`, `ffmpeg`) are missing.
- [x] `generate-image.py` reads the prompt template from `docs/brand/illustration-prompt.md` and substitutes `{{subject_description}}`.
- [x] Background normalization reads the primary bg token from `assets/css/tokens.css`.
- [x] Podcast dialogue is parsed as `Alex:` / `Sam:` lines; voices are mapped deterministically.
- [x] Blog CSS covers every component listed in `docs/components.md` (blog-specific section).
- [x] `components.md` blog snippets include the FAQ accordion JS and the podcast player JS.

## Known limitations

- Scripts have never been run end-to-end with a real `GEMINI_API_KEY`. Model availability and response shapes may need adjustment at first dogfood. Document any issues in `docs/brand/toolbelt.md` under "Pending decisions".
