# Illustration prompt — Gemini Image

> Prompt template used by `scripts/generate-image.py`. The only placeholder is `{{subject_description}}`, filled automatically per illustration by `/new-blog-article` or `/new-page`.

## Template

```
[Base style adjective, e.g. "elegant hand-drawn sketch"] illustration on a flat [dark|light] background color [primary bg hex from palette]. Thin [warm|cool] brush strokes in [accent hex] and [secondary hex]. {{subject_description}}. Editorial illustration feel. No text, no words. Wide 16:9. Minimal composition.
```

## Guidance for `/brand-setup`

- Pull bg color from `--midnight` (or whichever token is the primary background in `brand.md`).
- Pull accent and secondary from the two other dominant tokens.
- Base style adjective should match the brand's visual character (hand-drawn, flat geometric, collage, photographic, 3D render, etc.).
- Adjust temperature (warm/cool) to the palette.

## Example (filled, for reference only)

```
Elegant hand-drawn sketch style illustration on a flat dark background color #0D1B2A. Thin warm brush strokes in #F9DC5C and #ACCBE1. Two marketers collaborating at a whiteboard with floating UI elements. Editorial illustration feel. No text, no words. Wide 16:9. Minimal composition.
```
