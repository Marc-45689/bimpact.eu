# Brand

> Source of truth. Claude reads this at the start of every session. Keep it short, decisive, and up to date.

## Identity

- **Name:** <Your brand name>
- **Tagline:** <one line>
- **Positioning:** <one sentence — who you serve and what you do>

## Palette

| Token | Hex | Role |
|---|---|---|
| `--midnight` | `#0D1B2A` | Background primary |
| `--off-white` | `#FAFAFA` | Text on dark |
| `--accent` | `#F9DC5C` | Accent / highlights / CTAs |
| `--soft-blue` | `#7C98B3` | Secondary text |
| `--deep-blue` | `#1B4965` | Alt background |

Keep the palette small (5-7 tokens). Every hex in the site should map to a token. No ad-hoc colors.

## Typography

- **Display:** <font name> — used for emphasized script/italic words, never for body.
- **Body:** <font name> — sans-serif, weights 300-800.

Where to get them:
- Display: local WOFF2 in `assets/fonts/` (preload in `<head>`).
- Body: Google Fonts (preconnect + preload).

## Logo

- Full logo: `logo-principal.svg`
- Minimum size: 40px.
- Clear space: equivalent to the height of the "o" around the mark.

## Photography

- Style: <describe — e.g., natural light, warm tones, documentary>.
- Sources: <e.g., own shoots + curated Unsplash>.
- Retouch: <policies>.

## Iconography

- Style: <outline / filled / duotone / custom>.
- Library: <e.g., Lucide 1.8, pinned>.

## Do / Don't

- **Do:** <brand-consistent visual move>.
- **Don't:** <off-brand pitfall to avoid>.
