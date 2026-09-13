# Brand

> Source of truth. Claude reads this at the start of every session. Keep it short, decisive, and up to date.

## Identity

- **Name:** BIMpact
- **Tagline:** Études techniques BIM pour vos lots CFO-CFA.
- **Positioning:** Chargé d'études techniques indépendant, spécialisé en modélisation BIM des lots courants forts et courants faibles (CFO-CFA), au service des bureaux d'études, entreprises BTP et maîtrises d'ouvrage.

## Palette

Direction: "Bleu technique / blueprint" — dominante bleu-marine technique, accent orange sécurité électrique, fond clair façon papier calque.

| Token | Hex | Role |
|---|---|---|
| `--midnight` | `#0B2545` | Background primary (bleu blueprint sombre) |
| `--midnight-light` | `#123A6E` | Background dark hover/panels |
| `--deep-blue` | `#1D4E89` | Alt background, structure |
| `--soft-blue` | `#7A93AC` | Secondary text |
| `--light-blue` | `#C7D4E0` | Borders, dividers |
| `--accent` | `#E8622C` | Accent / CTAs / highlights (orange sécurité électrique, écho CFO) |
| `--off-white` | `#F5F3EE` | Text on dark / background papier |
| `--cream` | `#ECE7D8` | Card background, subtle highlight surface |

Keep the palette small (5-7 tokens). Every hex in the site should map to a token. No ad-hoc colors.

## Typography

- **Display:** IBM Plex Sans (weights 500-700) — titres, hero, emphase.
- **Body:** IBM Plex Sans (weights 400-500) — texte courant.
- **Mono (`--font-mono`):** IBM Plex Mono — labels techniques courts, métadonnées, tags (ex. "CFO / CFA"), pas pour le corps de texte.

Where to get them:
- All three: Google Fonts (preconnect + preload), pas de fichier local à héberger.
- URL family param: `IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500`

## Logo

- Full logo: `logo-principal.svg` — **placeholder actuel**, pas de logo réel fourni. Recolorisé aux tokens de la marque en attendant. À remplacer dès qu'un logo définitif existe.
- Minimum size: 40px.
- Clear space: equivalent to the height of the "o" around the mark.

## Photography

- Style: pas de photographie — le site privilégie l'illustration technique/schématique (esprit plan, schéma de principe, ligne fine) plutôt que la photo, cohérent avec l'univers BIM.
- Sources: illustrations générées ou dessinées ad hoc, voir `docs/brand/illustration-prompt.md`.
- Retouch: n/a (pas de photo).

## Iconography

- Style: outline, trait fin, cohérent avec l'esthétique blueprint.
- Library: Lucide (voir `assets/icons/README.md`), pinned version, chargé en local avec SRI.

## Do / Don't

- **Do:** Réserver l'orange accent (`--accent`) aux CTA et points clés — un ou deux par écran maximum.
- **Don't:** Introduire une couleur hors palette (vert, rouge, violet) pour des états ad hoc — dériver toute nuance supplémentaire des tokens existants.
