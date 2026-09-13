---
description: Define or refine the brand universe (palette, fonts, tone, illustration prompt). Two modes: "I have everything" or "help me".
---

You are piloting `/brand-setup`. Load the `starter-setup` skill.

## Step 1 — Mode selection

Ask the user:
1. **I have everything.** Palette, fonts, logo, tone — just write it down.
2. **Help me.** The user has some inspirations and a rough idea. You propose a brand.

## Mode 1: transcribe

Collect:
- Palette: 5-7 hex values with roles (background primary, text on dark, accent, secondary text, alt background, optional cream / highlight).
- Fonts: display (where to get) and body (where to get). If Google Fonts, note the exact URL.
- Logo: path to an SVG or request the user drops it in the repo root as `logo-principal.svg`.
- Photography style, iconography style.
- Audience, pronouns, 3-5 tone adjectives, forbidden / required editorial rules.

Write:
- `docs/brand/brand.md` (palette table, typography, logo, photography, iconography, do/don't)
- `docs/brand/tone-of-voice.md` (audience, pronouns, adjectives, rules, examples)
- `docs/brand/illustration-prompt.md` (derived from the palette)
- `assets/css/tokens.css` (replace placeholder tokens with the real palette and fonts)

## Mode 2: assist

1. Ask the user to drop 5-10 inspirations into `docs/inspirations/` and/or describe their activity and values.
2. If the `design` or `brand` skill is available, delegate to it for palette and typography proposals.
3. Otherwise, generate proposals yourself based on the inspirations and description:
   - Propose 2-3 palettes (3-5 hex each with role assignments)
   - Propose 2-3 font pairings (display + body)
   - Propose 3-5 tone adjectives and a sample hero headline
4. Iterate with the user until they choose.
5. Write the same files as in Mode 1.

## Step 2 — Illustration prompt derivation

Independent of mode, produce `docs/brand/illustration-prompt.md` from the chosen palette:
- `[primary bg hex]` → the `--midnight` or equivalent dark-token
- `[accent hex]` → the `--accent`
- `[secondary hex]` → the next most prominent token
- Base style adjective → ask or infer from inspirations (hand-drawn sketch / flat geometric / collage / photographic / 3D render / minimal line-art)
- Warm / cool → inferred from palette

## Step 3 — Audit

If pages already exist, run `/audit-brand` to identify places where tokens.css has changed and hex values need updating in HTML inline styles. Offer to fix.

## Step 4 — Commit

Stage and commit: `brand: define <mode> brand universe`.
