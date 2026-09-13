# Design : claude-site-starter

**Date** : 2026-04-21
**Statut** : validé, prêt pour planification d'implémentation
**Auteur** : Jessy Martin, co-conçu avec Claude
**Dossier cible** : `/Users/ADMIN/claude-projets/jessem/claude-site-starter/`
**Destination** : repo GitHub public (à créer), licence MIT

---

## 1. Objectif

Produire un starter open source qui permet à n'importe quel utilisateur de lancer ou de reprendre un site web marketing en appliquant la même méthodologie que celle utilisée sur `jessem.fr` : site statique HTML/CSS/JS, hébergement SFTP, pilotage via Claude Code, pas de CMS, pas de framework, pas de bundler. Le starter embarque les bonnes pratiques (sécurité, SEO, perfs), les workflows CI (staging + prod via GitHub Actions), les slash commands Claude qui pilotent la création et la maintenance, et les modules optionnels (blog, podcast, illustrations IA, CRM, booking, analytics).

## 2. Philosophie et parti pris

- **Static-first.** HTML + CSS + JS vanilla. Aucun framework, aucun bundler, aucun build Node nécessaire pour servir le site.
- **CMS-free.** Le starter est incompatible avec l'approche CMS. Pour les utilisateurs sur WordPress/Webflow/Squarespace, on propose une migration assistée vers le static.
- **Brand-first.** Le starter ne produit pas un beau site tout seul. Il produit un squelette fonctionnel. Un site qualitatif nécessite un univers de marque préexistant (typo, couleurs, logo, assets, textes, direction éditoriale). Cet avertissement est en tête de README.
- **Claude Code-native.** Le repo est conçu pour un travail en paire humain + Claude. Slash commands, skills, conventions, design tokens, et `docs/brand/` centralisent la vérité que Claude relit à chaque session.
- **SFTP + PHP 8+.** Hébergement mutualisé à 3-5 € / mois. Déploiement par GitHub Actions via `lftp`.
- **Sécurité par défaut.** Tout ce qui est décrit en section 9 est activé dès le premier `git push`, non optionnel.

## 3. Scope

### Inclus dans la v1

- Squelette de site statique (home, blog, projects, about, legal, 404).
- Design tokens CSS (palette, typo, espacements).
- Stack d'intégrations par défaut : Cal.com (booking), Brevo (CRM/mailing via PHP proxy env-safe), Gemini (illustrations et podcast 2 voix), tarteaucitron (cookies), GA4/Plausible/Umami (analytics).
- Workflows GitHub Actions `deploy-staging.yml` et `deploy-production.yml` avec déploiement SFTP via `lftp`.
- `.htaccess` durci (HSTS, CSP dynamique, X-Frame-Options, Referrer-Policy, Permissions-Policy, COOP, clean URLs, cache, compression, WebP MIME).
- `.htaccess-staging` + génération automatique du `.htpasswd` pour protection staging.
- Slash commands : `/start-new-site`, `/adopt-existing-site`, `/new-page`, `/new-section`, `/brand-setup`, `/new-blog-article`, `/deploy`, `/audit-brand`, `/setup-integration`, `/setup-staging-auth`.
- Skill Claude Code `starter-setup` qui pilote la checklist et les analyses.
- Scripts utilitaires (`generate-image.py`, `generate-podcast.py`, `optimize-image.sh`, `sitemap-update.py`, `htpasswd-gen.sh`).
- Documentation `docs/brand/` (brand.md, tone-of-voice.md, illustration-prompt.md, toolbelt.md).
- `README.md` complet (anglais) avec disclaimer brand-first, section sécurité, section Lighthouse, exemple `jessem.fr`.
- `CONTRIBUTING.md`, `LICENSE` (MIT), `SETUP.md` (fallback manuel si l'utilisateur veut tout comprendre à la main).

### Exclus explicitement

- Supabase (auth, magic link, edge functions, migrations SQL).
- Tout CMS, ou pont vers un CMS.
- Tout framework ou bundler (Next, Astro, Vite, Webpack, Tailwind config node).
- Tout backend autre que PHP procédural simple.
- Paiement, e-commerce, checkout.
- Comptes utilisateurs, dashboards privés.
- Modules que l'on ajoutera en v2 et au-delà selon la demande (ne font pas partie du plan d'implémentation initial).

## 4. Audience et langue

- Audience : consultants, freelances, studios, PME francophones et internationales qui veulent un site marketing qualitatif sans se faire piéger par un CMS et qui adoptent Claude Code.
- Langue du repo, du code, des commentaires, de la doc : **anglais**.
- Langue du site généré : configurable au setup (FR par défaut dans le prompt de `/start-new-site`, EN et autres disponibles). Les noms de dossiers dans le site généré suivent la langue choisie (`about` ou `a-propos`, `projects` ou `projets`, etc.) via un dictionnaire de renommage exécuté par le setup.
- Langue de cette spec et des docs internes `docs/superpowers/*` : français (usage interne, pas déployé).

## 5. Architecture du repo

```
claude-site-starter/
├── .claude/
│   ├── settings.json                   # permissions safe par défaut
│   ├── commands/
│   │   ├── start-new-site.md
│   │   ├── adopt-existing-site.md
│   │   ├── new-page.md
│   │   ├── new-section.md
│   │   ├── brand-setup.md
│   │   ├── new-blog-article.md
│   │   ├── deploy.md
│   │   ├── audit-brand.md
│   │   ├── setup-integration.md
│   │   └── setup-staging-auth.md
│   └── skills/
│       └── starter-setup/
│           └── SKILL.md
├── .github/
│   └── workflows/
│       ├── deploy-staging.yml
│       └── deploy-production.yml
├── api/
│   ├── _env.php                         # loader .env (getenv safe)
│   ├── brevo.php.example
│   └── webhook.php.example
├── assets/
│   ├── css/
│   │   ├── tokens.css                   # palette, fonts, spacings, radii
│   │   ├── main.css                     # reset, utilitaires, nav, footer
│   │   ├── home.css
│   │   ├── blog.css
│   │   ├── projects.css
│   │   ├── legal.css
│   │   ├── cookie-consent.css
│   │   └── 404.css
│   ├── js/
│   │   ├── shared.js
│   │   └── cookie-consent.js
│   ├── fonts/                           # README.md expliquant comment poser les WOFF/WOFF2
│   ├── photos/                          # README.md
│   ├── icons/                           # README.md
│   └── illustrations-blog/              # README.md + illustration-prompt.md dupliqué en référence
├── blog/
│   ├── index.html                       # template liste
│   └── _template-article.html           # template article vide avec composants catalogués
├── projects/
│   ├── index.html                       # template liste projets
│   └── _template-project.html           # template page projet détail
├── about/
│   └── index.html
├── legal/
│   ├── privacy/index.html
│   ├── terms/index.html
│   └── cookies/index.html               # optionnel, redirigé depuis privacy si module cookies off
├── scripts/
│   ├── generate-image.py
│   ├── generate-podcast.py
│   ├── optimize-image.sh
│   ├── sitemap-update.py
│   └── htpasswd-gen.sh
├── docs/
│   ├── README.md                        # "docs/ est exclu du deploy sauf PDFs publics"
│   ├── brand/
│   │   ├── brand.md                     # source of truth lue par Claude à chaque session
│   │   ├── tone-of-voice.md
│   │   ├── illustration-prompt.md       # prompt Gemini paramétré par les brand assets
│   │   └── toolbelt.md                  # log des MCP et skills installés
│   ├── components.md                    # catalogue des composants HTML/CSS réutilisables
│   ├── inspirations/                    # images de référence (moodboard)
│   ├── content/                         # textes bruts, briefs, retranscriptions
│   ├── drafts/                          # brouillons d'articles et de pages
│   ├── migration/                       # si adopt-existing-site scénario CMS
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── .env.example
├── .gitignore
├── .htaccess
├── .htaccess-staging
├── 404.html
├── index.html                           # home placeholder
├── robots.txt
├── robots-staging.txt
├── sitemap.xml
├── site.webmanifest
├── logo-principal.svg                   # placeholder
├── SETUP.md                             # fallback manuel complet
├── README.md                            # vitrine open source
├── CONTRIBUTING.md
└── LICENSE
```

## 6. Slash commands

Toutes les commandes vivent dans `.claude/commands/<nom>.md`. Chaque fichier contient le prompt qui pilote Claude pour l'étape concernée. Elles partagent la skill `starter-setup` pour la logique commune (lecture de `docs/brand/brand.md`, gestion des modules, maj du sitemap, maj de `components.md`).

### 6.1 `/start-new-site`

Wizard complet pour un nouveau site. Une étape = un message Claude qui attend une réponse avant de continuer. Jamais d'options silencieuses.

Étapes :
1. **Disclaimer brand-first** : Claude affiche l'avertissement et demande si l'utilisateur a déjà logo, palette, typo, photos, textes clés. Si non → propose `/brand-setup` ou continue quand même en mode "je génère, tu refineras".
2. **Projet** : nom du site, tagline, domaine prod, domaine staging, langue du site (FR/EN/autre → ajuste les noms de dossiers et les textes UI des placeholders).
3. **Brand** : couleurs (hex × N), fonts (display + body + sources), logo (chemin local, URL, ou génération via la skill `design`), favicon.
4. **Structure** : quelles pages racine ? Home obligatoire, puis Y/N pour about, projects, blog, contact, pages custom nommées.
5. **Modules** : pour chaque module, Y/N et sous-choix :
   - Booking : Cal.com / Calendly / custom / aucun
   - CRM : Brevo / Mailchimp / webhook générique / aucun
   - Analytics : GA4 / Plausible / Umami / aucun
   - Cookie consent : tarteaucitron / aucun
   - Blog : oui / non
   - Podcast auto (requiert blog) : oui / non
   - Illustrations IA : oui / non
6. **Outillage Claude** : pour chaque outil, installer / skip / rappeler plus tard :
   - Superpowers (`/plugin install superpowers@claude-plugins-official`)
   - UI/UX Pro Max (clone de skill + ajout au path Claude)
   - 21st.dev (MCP add) ou mode manuel documenté
   - MCP Canva / Gmail / Notion / Drive (mention optionnelle, pas forcée)
7. **Hébergement** : SFTP (OVH / o2switch / autre). Demande host, username, password, chemins prod/staging. Renseigne les GitHub Actions secrets via `gh secret set` (en local, l'utilisateur doit être logué `gh auth login`).
8. **Staging auth** : génère les credentials staging (user + mot de passe), crée `.htpasswd-staging` via `scripts/htpasswd-gen.sh`, les affiche à l'utilisateur (une seule fois) avec rappel de stocker dans un gestionnaire de mots de passe.
9. **Git/GitHub** : `git init`, premier commit, `gh repo create` (choix public ou privé), push, création branche `staging`, push staging.
10. **Premier déploiement** : déclenche le workflow staging, attend la complétion, renvoie l'URL staging avec les credentials htpasswd.
11. **Checklist finale humain** : DNS à configurer, Brevo list ID à créer, Cal.com event slug à valider, `.env` serveur à créer manuellement côté SFTP (Claude ne peut pas l'écrire à distance), premier test visuel sur staging.

Outputs attendus : repo complet, GitHub repo créé, branches `main` et `staging` poussées, staging déployé et accessible, CTAs pour le prochain pas (`/new-page`, `/new-blog-article`).

### 6.2 `/adopt-existing-site`

Adaptation à un site existant. Trois scénarios selon la stack détectée.

Étape 1 — Collecte. Claude demande : URL live ? Chemin du repo local ? Les deux ?

Étape 2 — Détection. Claude examine :
- Présence de `.git` → repo local.
- `wp-config.php`, `wp-content/`, `/wp-json/` exposé, générateur `<meta name="generator" content="WordPress">` → WordPress.
- `package.json` avec Next/Astro/Gatsby/Eleventy/Vite → framework SSG/SSR.
- HTML + CSS sans framework → static (cas principal).
- Pas de repo, juste une URL → analyse du live via WebFetch, sitemap, view-source, robots.txt.

Étape 3 — Branchement.

**Scénario A : site statique existant**
- Analyse du design system : Claude lit les CSS, extrait les valeurs récurrentes (couleurs, fonts, espacements, rayons), propose `assets/css/tokens.css` qui formalise ces valeurs sans casser l'existant.
- Analyse du contenu : liste des pages, composants récurrents (nav, footer, card, hero, CTA).
- Plan d'injection : Claude propose un diff ("j'ajoute `.claude/`, `.github/workflows/deploy-*.yml`, `docs/superpowers/`, `docs/brand/brand.md`, je respecte ta structure CSS existante sous `styles/` au lieu d'imposer `assets/css/`, j'adapte le `.htaccess` existant en conservant tes règles et en ajoutant les headers manquants").
- Validation utilisateur étape par étape. Aucune modification silencieuse du code existant.

**Scénario B : framework moderne**
- Pas de migration. Superposition de la méthodologie uniquement : `.claude/`, `docs/superpowers/`, `docs/brand/`, skills. Le starter coexiste avec le framework.
- Workflows de déploiement non injectés par défaut (le framework a les siens). On propose d'ajouter `deploy-staging.yml` uniquement si l'utilisateur veut un second pipeline.
- Valeur principale : la méthodo de travail avec Claude, pas la stack.

**Scénario C : CMS (WordPress, Webflow, Squarespace, Shopify vitrine, Wix)**
- Claude propose explicitement une migration vers static (pas une adaptation).
- Sous-flow :
  1. Scanne `domain/sitemap.xml` (ou `/wp-sitemap.xml`) pour lister toutes les URLs.
  2. Pour chaque URL, WebFetch le HTML rendu. Extrait contenu textuel, meta tags, images (download local), slugs.
  3. Dépose le contenu dans `docs/migration/<slug>.md` (un fichier par page).
  4. Génère `docs/migration/url-mapping.md` (ancienne URL → nouvelle URL).
  5. Reconstruit les pages en HTML static dans la structure du starter, **une par une, avec validation utilisateur**, en utilisant les tokens et composants. Jamais de batch aveugle.
  6. Génère les règles de redirection dans `.htaccess` pour préserver le SEO.
  7. Documente dans `docs/migration/gaps.md` les fonctionnalités dynamiques non reproductibles (plugins, form avancé, e-commerce) avec alternatives static-friendly proposées (Brevo pour form, Cal.com pour booking, Snipcart/LemonSqueezy pour paiement léger).
- Ce sous-flow peut durer plusieurs sessions. Il est conçu pour être repris.

Output attendu : repo existant enrichi de la méthodologie Claude Code, sans régression visuelle ni SEO.

### 6.3 `/new-page`

Création d'une page qui respecte la marque, le design system, et réutilise les composants existants.

Flow :
1. Claude lit `docs/brand/brand.md`, `docs/brand/tone-of-voice.md`, `assets/css/tokens.css`, et `docs/components.md`.
2. Claude scanne les pages existantes pour confirmer l'inventaire des composants disponibles (hero, logo cloud, feature grid, card, CTA inline, FAQ, testimonials, pricing, etc.).
3. L'utilisateur décrit en langage naturel ce qu'il veut : "page Services avec hero, trois offres en cards, témoignages, FAQ, CTA final".
4. Claude propose un outline :
   - Structure (sections dans l'ordre).
   - Composants à réutiliser (référencés par classe CSS).
   - Nouveaux composants à créer si besoin (avec ajout prévu dans `components.md` et un CSS dédié dans `assets/css/<page>.css`).
   - Meta SEO proposés (title, description, canonical, OG, schema.org applicable).
   - Entrée dans la nav et dans `sitemap.xml`.
5. Validation utilisateur (invoque éventuellement `brainstorming` skill si l'outline est ambigu).
6. Claude écrit la page HTML, éventuellement le CSS associé, met à jour la nav, `sitemap.xml`, et `components.md` si nouveau composant.
7. Claude exécute `/audit-brand` sur la nouvelle page et affiche le résultat (règles éditoriales, alt text des images, tokens respectés, tailles d'images présentes, pas de `.html` dans les liens).

### 6.4 `/new-section`

Variante de `/new-page` pour ajouter une section à une page existante (ex : "ajouter une section témoignages à la home"). Même logique, portée réduite.

### 6.5 `/brand-setup`

Définition ou refine de l'univers de marque. Deux modes.

**Mode "j'ai tout"**
- L'utilisateur fournit palette hex, fonts, logo, photos, ton.
- Claude écrit `docs/brand/brand.md` + `tone-of-voice.md` + `illustration-prompt.md`.

**Mode "aide-moi"**
- L'utilisateur dépose 5 à 10 inspirations dans `docs/inspirations/` et/ou décrit son activité et ses valeurs.
- Claude propose, via la skill `design` (ou `brand` si installée), une palette (3 à 5 couleurs avec rôles), un pairing de fonts, un ton éditorial (3 à 5 adjectifs + do/don't), et un prompt d'illustration dérivé.
- Validation utilisateur. Itère si besoin.
- Écrit les mêmes fichiers.

Le prompt d'illustration (`illustration-prompt.md`) est **généré à partir des brand assets** (logo, palette, typo) et pas depuis les inspirations. Il suit la structure suivante :

```
[Base style adjective, e.g. "elegant hand-drawn sketch"] illustration on a flat
[dark/light] background color [primary bg hex from palette]. Thin [warm/cool]
brush strokes in [accent hex] and [secondary hex]. [Subject description
placeholder — to be replaced per illustration]. Editorial illustration feel.
No text, no words. Wide 16:9. Minimal composition.
```

`{{subject_description}}` est le seul placeholder rempli par `/new-blog-article` ou `/new-page` quand ils appellent `generate-image.py`.

### 6.6 `/new-blog-article`

Pipeline complet pour un article.

1. L'utilisateur donne un titre ou un sujet.
2. Claude lit les règles (`tone-of-voice.md`), consulte les derniers articles pour le style, propose un outline (H2, H3, angle, arguments, citations, CTA inline, FAQ finale).
3. Validation utilisateur → `brainstorming` skill si besoin.
4. Claude rédige l'article dans `blog/<slug>.html` à partir de `_template-article.html`.
5. Claude appelle `scripts/generate-image.py` avec un `subject_description` dérivé de l'article, génère l'illustration cover, convertit en WebP, corrige le fond à la couleur bg de la palette.
6. Si module podcast activé : appelle `scripts/generate-podcast.py`, génère un script dialogue 2 voix (style NotebookLM, explicité dans le prompt Gemini), synthétise en audio via Gemini TTS, convertit en MP3, intègre le lecteur dans l'article.
7. Met à jour `blog/index.html` avec la nouvelle carte.
8. Met à jour `sitemap.xml`.
9. Exécute `/audit-brand`.
10. Commit staging, push, laisse l'utilisateur vérifier sur staging avant de merge.

### 6.7 `/deploy`

Helper pour la discipline staging → prod.

- Vérifie la branche courante.
- Si `staging` : propose `git add -A`, commit (demande message), push.
- Si `main` : propose de merger `staging` dans `main` seulement si `staging` est validé (Claude demande "as-tu testé sur staging ?").
- Rappelle les credentials staging si demandé.
- Ne push jamais directement sur `main` sans validation explicite.

### 6.8 `/audit-brand`

Check automatique sur une page ou tout le site.

Vérifications :
- Tokens CSS respectés (pas de couleurs hardcodées hors `:root`).
- Règles éditoriales respectées (pas d'emojis si interdits par `tone-of-voice.md`, pas de tirets longs si interdits, pas de termes bannis).
- Meta tags présents (title, description, canonical, OG).
- Images avec `alt`, `width`, `height`, `loading="lazy"` (sauf hero critique avec `loading="eager"`).
- Liens internes sans `.html`.
- Schema.org applicable présent.
- Pas de secrets dans le diff.
- CSP cohérente avec les scripts externes présents dans le HTML.

Renvoie un rapport markdown avec les violations.

### 6.9 `/setup-integration`

Ajoute un module après coup (ex : activer Brevo sur un site qui ne l'avait pas). Sous-commande : `/setup-integration brevo`, `/setup-integration cal`, etc.

Flow : lit l'état actuel, ajoute les fichiers manquants, met à jour la CSP, ajoute les entrées `.env.example`, guide pour les secrets.

### 6.10 `/setup-staging-auth`

Rotation ou initialisation des credentials staging (user + password htpasswd).

Flow : génère nouvelles credentials via `scripts/htpasswd-gen.sh`, remplace `.htpasswd-staging`, commit push staging, affiche les credentials à l'utilisateur avec rappel stockage coffre.

## 7. Skill `starter-setup`

Skill locale au repo, dans `.claude/skills/starter-setup/SKILL.md`. Contient la logique partagée par les slash commands :

- Lecture cachée de `docs/brand/brand.md` et `tokens.css` avant toute action.
- Gestion du registre de modules (liste, état actif / inactif, dépendances).
- Génération de la CSP dynamique.
- Mise à jour automatique de `docs/components.md` quand une nouvelle classe CSS réutilisable est créée.
- Mise à jour automatique de `sitemap.xml` quand une page est ajoutée/supprimée/renommée.
- Vérification que les env vars nécessaires sont présentes avant d'invoquer un script.
- Pattern safe pour PHP : toujours passer par `api/_env.php`, jamais de clé en dur.

La skill est auto-chargée quand l'utilisateur invoque une slash command du starter. Elle ne se déclenche pas pour une conversation banale.

## 8. Modules

### 8.1 Module "contenu et création"

| Module | API / Service | Fichiers livrés | Dépendances système |
|---|---|---|---|
| Blog | — | `blog/index.html`, `blog/_template-article.html`, `assets/css/blog.css`, composants catalogués dans `docs/components.md` | — |
| Illustrations IA | Gemini Image API | `scripts/generate-image.py`, `docs/brand/illustration-prompt.md` | `GEMINI_API_KEY`, `cwebp`, Python `Pillow` |
| Podcast auto | Gemini TTS | `scripts/generate-podcast.py`, lecteur HTML+CSS+JS dans le template article | `GEMINI_API_KEY`, `ffmpeg` |
| Cover projets | Gemini Image API | Appelé par `/new-page` si type=project | idem illustrations |

Le podcast est explicitement 2 voix dialogue, style Google NotebookLM. Le prompt de génération du script mentionne cette référence pour que Gemini calibre le ton.

### 8.2 Module "interactions"

| Module | Alternatives au setup |
|---|---|
| Booking | Cal.com (embed script + data attributes) / Calendly / custom / aucun |
| CRM / forms | Brevo (`api/brevo.php` via PHP proxy) / Mailchimp (même pattern) / webhook générique / aucun |
| Analytics | GA4 / Plausible / Umami / aucun |
| Cookie consent | tarteaucitron (pinned + SRI) / aucun |
| Chat | Crisp / Tawk / aucun |

Tous les modules côté serveur passent par `api/_env.php` → `getenv()`. Jamais de clé API dans le repo, même dans un fichier de config.

### 8.3 Module "outillage Claude Code"

Proposés au setup, statut `install now / skip / remind later` :
- Superpowers (plugin Claude Code officiel)
- UI/UX Pro Max (skill locale externe)
- 21st.dev (MCP server : `claude mcp add 21st-dev`) ou mode manuel documenté (visite de 21st.dev/mcp, copy prompt, colle dans Claude)
- MCP Canva, Gmail, Notion, Drive : mention optionnelle dans la doc, pas poussé au setup.

Les choix sont loggés dans `docs/brand/toolbelt.md`.

### 8.4 Module "SEO et perf" (inclus par défaut, non optionnel)

- `sitemap.xml` auto-maintenu par la skill.
- `robots.txt` + `robots-staging.txt` distincts.
- Schema.org JSON-LD : Organization (home), Article (blog), BreadcrumbList (toutes pages non-root), FAQPage (si FAQ), WebSite (global). Ajouté automatiquement par `/new-page` selon le type.
- OG / Twitter cards templates.
- `.htaccess` : compression deflate, cache long sur assets (1 an), cache court sur HTML (1 h), WebP MIME type, clean URLs.
- Preload des fonts critiques.
- `loading="lazy"` et `width/height` obligatoires sur toutes les images (règle auditée).

### 8.5 Module "staging safety" (inclus par défaut, non optionnel)

Workflow `deploy-staging.yml` :
- Copie `robots-staging.txt` → `robots.txt`.
- Injecte `<meta name="robots" content="noindex, nofollow">` dans tous les HTML.
- Supprime `sitemap.xml` du payload déployé.
- Strip les blocs GA entre `<!-- GA_START -->` et `<!-- GA_END -->`.
- Copie `.htaccess-staging` → `.htaccess`, `.htpasswd-staging` → `.htpasswd`.
- Nettoie `.git`, `docs/` (sauf PDFs), `.claude/`, `.htpasswd-staging`, `.htaccess-staging`, `robots-staging.txt` avant upload.

Workflow `deploy-production.yml` :
- Nettoie `.git`, `.claude`, `.htaccess-staging`, `.htpasswd-staging`, `robots-staging.txt`, `docs/` sauf PDFs.
- Upload vers SFTP prod.

## 9. Sécurité par défaut

Aucun point n'est optionnel. Tout est activé dès le setup.

### 9.1 Infrastructure (`.htaccess`)

- HTTPS forcé (301).
- Non-www canonique (301).
- HSTS 1 an `includeSubDomains`.
- `X-Frame-Options: SAMEORIGIN`.
- `X-Content-Type-Options: nosniff`.
- `Referrer-Policy: strict-origin-when-cross-origin`.
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()`.
- `Cross-Origin-Opener-Policy: same-origin-allow-popups`.
- CSP stricte générée à partir des modules actifs (`script-src`, `style-src`, `font-src`, `img-src`, `connect-src`, `frame-src` whitelistés explicitement).
- `Options -Indexes` (pas de directory listing).
- `ErrorDocument 403/404` → `/404.html`.
- `X-Robots-Tag: noindex, nofollow` sur les PDFs.

### 9.2 Secrets

- `.env` jamais commité, `.env.example` versionné avec placeholders documentés.
- Loader PHP dédié `api/_env.php` qui parse `.env` et expose via `getenv()`.
- Secrets SFTP (`OVH_HOST`, `OVH_USERNAME`, `OVH_PASSWORD`, `OVH_PROD_DIR`, `OVH_STAGING_DIR`) dans GitHub Actions Secrets, set via `gh secret set` pendant le setup.
- Secrets API (Brevo, Gemini) dans `.env` serveur sur l'hébergement, créé manuellement côté SFTP (Claude affiche les instructions et les valeurs).
- Pre-commit hook optionnel (proposé au setup) : grep naïf pour `key|token|password|secret` dans le diff, refus du commit si match.

### 9.3 API PHP

- `Access-Control-Allow-Origin` whitelisté sur le domaine prod uniquement.
- `OPTIONS` preflight géré (204).
- Méthodes restreintes (POST uniquement quand pertinent).
- Validation stricte des inputs (`email`, `source`, types attendus).
- Réponses d'erreur non bavardes (pas de stack trace, pas de PATH, pas de détails internes).

### 9.4 Staging

- Obligatoirement `.htpasswd`-protégé.
- `noindex, nofollow` injecté par le workflow.
- GA stripped.
- `sitemap.xml` absent du payload staging.
- Credentials générés par `/setup-staging-auth`, stockés chez l'utilisateur dans un gestionnaire de mots de passe, jamais dans le repo.

### 9.5 Dépendances tierces

- CDN scripts (Lucide, tarteaucitron, Cal.com, Brevo SDK) épinglés à une version précise.
- SRI hash obligatoire sur les `<script src="https://…">`.
- Pas de `latest` ni `@next`.
- Avant d'ajouter un nouveau script externe, la CSP doit être mise à jour et le SRI hash calculé. La skill `starter-setup` gère ça dans `/setup-integration`.

### 9.6 Git / GitHub

- `.gitignore` complet (`.env`, `.env.*`, `.DS_Store`, `node_modules/`, `.vscode/`, `.idea/`, `docs/` sauf `*.pdf`, `.superpowers/`).
- Recommandation activée au setup : GitHub Secret Scanning + Dependabot + Branch Protection sur `main` (require PR, require staging deploy success).

### 9.7 Pitfalls AI-specific à documenter

Dans la section Security du README :
- Ne jamais coller une vraie clé dans un message à Claude. Utiliser `.env`.
- Toujours relire les diffs de Claude avant commit, surtout `api/`, `.env*`, `.github/workflows/`, `.htaccess`, `.claude/settings*.json`.
- `grep -iE "key|token|password|secret"` sur le diff avant push.
- Pruner `.claude/settings.local.json` périodiquement.
- Ne pas accorder `Bash(rm:*)`, `Bash(git push --force:*)`, ou `WebFetch(*)` global.
- Refuser les fixes CSP paresseux (`unsafe-eval`, `*`) que Claude propose parfois.
- Ne pas partager publiquement des transcripts Claude contenant URLs internes, chemins, snippets de clés.
- Claude peut halluciner noms de package, signatures. Vérifier.
- Lire le code des skills/MCP avant de leur donner des permissions larges.

## 10. Workflow Lighthouse documenté

Le README inclut une section "Improving your site" qui explique le boucle rapide :

1. Push sur staging.
2. Ouvrir Chrome DevTools → Lighthouse → Analyze (ou pagespeed.web.dev si le staging est rendu accessible temporairement).
3. Copier les sections Opportunities + Diagnostics (Performance, SEO, Accessibility, Best Practices).
4. Coller à Claude avec le prompt suggéré :
   `Here are Lighthouse findings for my staging URL. Fix the ones that apply to our starter conventions and don't break anything else. Propose changes before applying.`
5. Claude propose un plan, l'utilisateur valide, Claude implémente.
6. Re-test sur staging.
7. Quand Lighthouse est satisfaisant, merge `staging` → `main`.

## 11. Documentation

### 11.1 `README.md` (anglais)

Sections dans l'ordre :
- Titre + one-line hook.
- Philosophy (static-first, brand-first, Claude Code-native, SFTP, AI-assisted).
- Disclaimer brand-first en bloc mis en évidence.
- Quickstart new site.
- Quickstart adopt existing.
- What you get (liste des modules).
- Creating new pages later.
- Example (lien vers jessem.fr comme référence vivante).
- Stack.
- Requirements (SFTP + PHP 8+, GitHub, Claude Code, **Claude Max recommandé**).
- Security (section complète avec pitfalls AI-specific).
- Improving your site (workflow Lighthouse).
- License.

### 11.2 `SETUP.md` (anglais, fallback manuel)

Pas-à-pas complet pour quelqu'un qui veut tout faire à la main sans Claude. Sert aussi de référence pour comprendre ce que Claude fait en coulisse.

### 11.3 `CONTRIBUTING.md` (anglais)

- Comment forker et proposer un nouveau module.
- Convention : un module = un dossier `modules/<nom>/` avec `README.md`, templates HTML/CSS/JS, `*.php.example`, `install.md` (ce que le setup fait pour l'activer).
- Tests : checklist manuelle de création d'un site from scratch avec le module avant PR.

### 11.4 `docs/brand/brand.md`

Source de vérité de la marque. Lue par Claude à chaque session. Structure :
- Identity : nom, tagline, positioning.
- Palette : couleurs avec hex, rôles, usage.
- Typography : fonts, usage, weights, fallbacks.
- Logo : variantes, minimum size, clear space.
- Photography : style, sources, retouche.
- Iconography : style (outline / filled / custom).
- Do / Don't visuel.

### 11.5 `docs/brand/tone-of-voice.md`

Direction éditoriale. Structure :
- Audience.
- Pronouns (je/nous/vous/tu).
- Adjectifs de ton (3 à 5).
- Règles : interdits (emojis, tirets longs, anglicismes…), imposés (stats sourcées, citations en blockquote…).
- Do / Don't rédactionnel avec exemples.

### 11.6 `docs/brand/illustration-prompt.md`

Gabarit du prompt Gemini avec placeholder `{{subject_description}}`. Paramétré par les couleurs de la palette.

### 11.7 `docs/brand/toolbelt.md`

Log des outils Claude Code installés (Superpowers, UI/UX Pro Max, 21st.dev, MCP divers), dates d'ajout.

### 11.8 `docs/components.md`

Catalogue vivant des composants HTML/CSS réutilisables. Mis à jour automatiquement par la skill quand un nouveau composant est créé.

## 12. Licence et publication

- Licence : MIT.
- Repo GitHub : `github.com/<user>/claude-site-starter` (nom exact à confirmer côté Jessy avant création).
- Visibilité : public.
- Template repo GitHub activé (pour que les utilisateurs puissent cliquer "Use this template").
- README avec captures d'écran et GIF de démo de `/start-new-site`.
- Pas de releases versionnées avant validation d'usage interne (dogfood sur au moins un site neuf et un site adopté).

## 13. Plan de déploiement interne (non-goals de ce spec)

La mise en production passe par, dans l'ordre :
1. Plan d'implémentation détaillé (skill `writing-plans`).
2. Implémentation par chantiers indépendants.
3. Dogfood : création d'un site neuf via `/start-new-site` dans un dossier temporaire, déploiement staging, validation.
4. Dogfood : adoption sur une copie de `/site`, vérification que rien ne casse.
5. Publication sur GitHub, README finalisé avec captures.

Ces étapes sortent du scope de ce spec. Elles seront détaillées dans le plan.

## 14. Non-goals (pour mémoire)

- Pas de panneau admin.
- Pas d'auth utilisateur frontale.
- Pas de base de données.
- Pas de fonction édito en ligne (pas de Forestry / Decap).
- Pas d'e-commerce natif.
- Pas de build step.
- Pas d'interopérabilité active avec un CMS (migration one-way uniquement).

## 15. Questions ouvertes résiduelles

- Nom exact du repo GitHub public : `claude-site-starter` confirmé, à valider au moment du `gh repo create`.
- Listing éventuel sur awesome-lists (awesome-claude-code, awesome-static-site-generators) : à faire après publication.
- Version française du README : à décider après retours des premiers utilisateurs (si la demande FR est forte).

---

**Fin du design.**
