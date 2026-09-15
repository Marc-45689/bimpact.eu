# Brand

> Source of truth. Claude reads this at the start of every session. Keep it short, decisive, and up to date.

## Identity

- **Name:** BIMpact
- **Tagline:** Études techniques BIM pour vos lots CFO-CFA.
- **Positioning:** Chargé d'études techniques indépendant, spécialisé en modélisation BIM des lots courants forts et courants faibles (CFO-CFA), au service des bureaux d'études, entreprises BTP et maîtrises d'ouvrage.

## Palette

Direction: "Bleu technique / blueprint" — **palette officielle sourcée directement du logo réel** (`logo-principal.svg`, dessiné par l'utilisateur — lockup complet dans `docs/inspirations/LOGO BIMpact.svg`). Les 4 couleurs du logo sont prises littéralement ; les 4 autres tokens sont dérivés par interpolation linéaire entre elles (formule documentée pour rester auditable).

| Token | Hex | Role | Source |
|---|---|---|---|
| `--midnight` | `#16283E` | Background primary (bleu marine du logo) | Logo (fond) |
| `--deep-blue` | `#2F5679` | Alt background, structure | Logo (facette) |
| `--accent` | `#FF6A39` | Accent / CTAs / highlights | Logo (facette) |
| `--off-white` | `#EEF2F6` | Text on dark / background clair | Logo (facette) |
| `--midnight-light` | `#1F3853` | Background dark hover/panels | Dérivé : mix(midnight, deep-blue, 35%) |
| `--soft-blue` | `#7B94AB` | Secondary text | Dérivé : mix(deep-blue, off-white, 40%) |
| `--light-blue` | `#BECBD7` | Borders, dividers | Dérivé : mix(deep-blue, off-white, 75%) |
| `--cream` | `#DFE6EC` | Card background, subtle highlight surface | Dérivé : mix(off-white, deep-blue, 8%) |

Keep the palette small (5-7 tokens). Every hex in the site should map to a token. No ad-hoc colors. Palette précédente (avant le logo réel) archivée dans `docs/inspirations/design.md`.

## Typography

- **Display:** IBM Plex Sans (weights 500-700) — titres, hero, emphase.
- **Body:** IBM Plex Sans (weights 400-500) — texte courant.
- **Mono (`--font-mono`):** IBM Plex Mono — labels techniques courts, métadonnées, tags (ex. "CFO / CFA"), pas pour le corps de texte.

Where to get them:
- All three: Google Fonts (preconnect + preload), pas de fichier local à héberger.
- URL family param: `IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500`

## Logo

- Icon mark: `logo-principal.svg` — recadrage carré (120×120) de la marque "Tower", sans le texte, pour les emplacements 40px (nav, favicon, `site.webmanifest`).
- Lockup complet (icône + wordmark "BIMpact"): `docs/inspirations/LOGO BIMpact.svg` — badge carré à fond plein, pensé pour les grands formats (footer, hero, documents), pas pour la nav. Pas encore intégré ailleurs sur le site.
- Wordmark typeface (dans le lockup): Space Grotesk — distinct de la police du site (IBM Plex Sans/Mono), traité comme un élément de logo figé, pas une police d'interface.
- Nav wordmark (`.nav-wordmark`, `assets/css/main.css`): "BIM<em>pact</em>" affiché en texte HTML à côté de l'icône, **en `--font-display` (IBM Plex Sans), pas en Space Grotesk** — écart assumé par rapport à la règle ci-dessus, pour garantir un rendu net/accessible dans la nav sans dépendre d'un embed de police dans le SVG. Reprend le bicolore du logo (off-white / accent).
- Minimum size: 40px.
- Clear space: equivalent to the height of the "o" around the mark.

## Photography

- Style: pas de photographie de manière générale — le site privilégie l'illustration technique/schématique (esprit plan, schéma de principe, ligne fine) plutôt que la photo, cohérent avec l'univers BIM.
- Exception: un portrait de Marc Forner sur `/qui-suis-je/` (et son twin `/en/about/`), en noir et blanc pour rester cohérent avec la palette du site — seul emplacement autorisé pour une photo.
- Sources: illustrations générées ou dessinées ad hoc, voir `docs/brand/illustration-prompt.md`.
- Retouch: portrait en niveaux de gris, pas d'autre retouche.

## Iconography

- Style: outline, trait fin, cohérent avec l'esthétique blueprint.
- Library: Lucide (voir `assets/icons/README.md`), pinned version, chargé en local avec SRI.

## Do / Don't

- **Do:** Réserver l'orange accent (`--accent`) aux CTA et points clés — un ou deux par écran maximum.
- **Don't:** Introduire une couleur hors palette (vert, rouge, violet) pour des états ad hoc — dériver toute nuance supplémentaire des tokens existants.
