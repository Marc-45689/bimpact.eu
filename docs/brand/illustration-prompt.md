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
- Background: `--midnight` (`#16283E`).
- Accent stroke: `--accent` (`#FF6A39`).
- Secondary stroke: `--deep-blue` (`#2F5679`).
- Temperature: cool overall (blueprint blues), warm accent only (orange).

## Example (filled, for reference only)

```
Flat technical line-art, blueprint schematic style illustration on a flat dark background color #16283E. Thin cool strokes in #2F5679, one warm accent stroke in #FF6A39. A technical drawing of an electrical distribution panel with BIM model wireframe overlay. Editorial illustration feel. No text, no words. Wide 16:9. Minimal composition.
```
