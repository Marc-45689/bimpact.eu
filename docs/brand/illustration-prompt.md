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

## BIMpact settings

- Base style adjective: **flat technical line-art, blueprint schematic** — thin consistent stroke weight, no shading, evokes a technical drawing rather than a decorative illustration.
- Background: `--midnight` (`#0B2545`).
- Accent stroke: `--accent` (`#E8622C`).
- Secondary stroke: `--deep-blue` (`#1D4E89`).
- Temperature: cool overall (blueprint blues), warm accent only (orange).

## Example (filled, for reference only)

```
Flat technical line-art, blueprint schematic style illustration on a flat dark background color #0B2545. Thin cool strokes in #1D4E89, one warm accent stroke in #E8622C. A technical drawing of an electrical distribution panel with BIM model wireframe overlay. Editorial illustration feel. No text, no words. Wide 16:9. Minimal composition.
```
