# Components catalog

Reusable HTML/CSS patterns. `/new-page` and `/new-section` read this to pick existing patterns before inventing new ones. Keep entries compact.

## Layout

| Component | Class | Where | Purpose |
|---|---|---|---|
| Page container | `.container` | `main.css` | Centered max-width wrapper, responsive padding |
| Section defaults | `section` | `main.css` | Vertical rhythm + overflow clip |

## Navigation

| Component | Class | Purpose |
|---|---|---|
| Fixed nav | `nav` / `nav.scrolled` | Header with scroll-triggered glass blur |
| Nav wordmark | `.nav-wordmark` | "BIM<em>pact</em>" text set next to the icon mark in `.nav-logo`; two-tone (off-white / accent) matching `logo-principal.svg`. Rendered in `--font-display` (IBM Plex Sans), not the logo's Space Grotesk — see `docs/brand/brand.md` Logo section. |
| Mobile drawer | `.nav-links.open` | Hamburger-triggered side drawer under 860px |
| Language switcher | `.nav-lang` | FR/EN/ES links pointing at the current page's exact counterpart (see `CLAUDE.md` — Languages); `.active` marks the current language |
| Cookie consent banner | `.cookie-banner` / `.cookie-banner-inner` / `.cookie-banner-actions` | Fixed bottom bar on every page, gates `assets/js/analytics.js` (GA4) behind an accept/refuse choice via `assets/js/cookie-consent.js`; reopened from the footer's `.footer-cookie-link` button. `hidden` attribute toggles visibility. |

## Forms

| Component | Class | Purpose |
|---|---|---|
| Contact form | `.contact-form` / `.form-field` / `.form-status` | Name/email/phone (optional)/message form on `#contact` (home, about, blog — every locale), posts JSON to `api/contact.php` via `assets/js/contact-form.js`. No raw `mailto:` link anywhere on the site — the form is the only contact channel, to keep the address off bot-scraped pages; legal pages link to it instead (nav `.nav-cta` + a `.btn-primary` in their own "Contact" section). Anti-spam: `.form-honeypot` hidden field (`company_website`, must stay empty) plus a server-side minimum fill time — no captcha, no third-party script, no CSP change. Success/error text comes from `data-success`/`data-error` on the `<form>` so each locale sets its own copy. Fires a `contact_form_submit` GA4 event on success (only if consent already granted). |

## CTAs

| Component | Class | Purpose |
|---|---|---|
| Primary button | `.btn-primary` | Filled accent, pill |
| Secondary button | `.btn-secondary` | Outlined, pill |

## Motion

| Component | Class | Purpose |
|---|---|---|
| Reveal on scroll | `.reveal` / `.reveal.visible` | IntersectionObserver fade-up |
| Scroll progress | `#scrollProgress` | Bottom-fixed progress bar |
| Back to top | `#scrollTop` | Fixed button appearing after 600px scroll |

## Utilities

| Class | Purpose |
|---|---|
| `.script` | Apply display font |
| `.accent` | Accent color |
| `.soft` | Secondary text color |
| `.sr-only` | Visually hidden, screen-reader accessible |
| `.lead` | Section intro paragraph, `--fs-md`, `--soft-blue`, capped at 60ch |
| `.tag-row` / `.tag` | Row of small pill tags (tools, keywords), mono font, outlined |
| Contact info | `.contact-info` (`main.css`) | `<dl>` of direct contact info (email, phone) — no form, direct channels only. Reused in the `#contact` section on the homepage, `/a-propos/`, `/blog/`, and every blog article including `_template-article.html` (and their `/en/` twins) — new articles get it automatically from the template. Tagline: first sentence, then `<br>`, then the "Marc Forner - BIMpact - ..." signature line, both hardcoded per language (not a token). |

## Home-specific

| Component | Class | Purpose |
|---|---|---|
| Expertise cards | `.expertise-grid` / `.expertise-card` | 3-up card grid (tools / deliverables / audience), nested inside the merged hero/expertise `<header>` on the homepage |
| Contact background illustration | `#contact::before` | Decorative BIM wireframe backdrop (`assets/illustrations/hero-background.svg`), grayscale, faded on the left via a `var(--off-white)` gradient layer so contact text stays readable; positioned top-right at 49.5% width, `opacity: 0.275`. Purely decorative — no `<img>`, no alt text needed. Homepage-only (defined in `home.css`); other pages' `#contact` section has a plain background. |
| Hero/expertise background illustration | `.hero::before` | Same decorative-backdrop technique as the contact illustration above, reusing a different plate from the same generative set (`assets/illustrations/expertise-background.svg`, portrait 620×1040 — sized by height via `background-size: auto 90%` rather than width, since it's a tall plate, not a wide one). Same grayscale/gradient/opacity treatment. |

## About-specific

| Component | Class | Purpose |
|---|---|---|
| Hero grid | `.about-hero-grid` | Two-column layout (text / portrait) on `/a-propos/` and `/en/about/`, stacks on mobile (`≤860px`) |
| Portrait | `.about-photo` | Square headshot, `object-fit: cover`, `--radius-lg` corners, `--light-blue` ring border — matches the squared-off technical/blueprint language used elsewhere (icon logo crop, `.expertise-card`), rather than a circular crop. Only exception to the "no photography" brand rule — see `docs/brand/brand.md` § Photography |
| Experience timeline | `.about-timeline` / `.about-timeline-item` | Stacked list of past roles, left border rule, mono accent-colored date, reuses `.tag-row`/`.tag` for sector tags. Optional `.about-timeline-desc` paragraph for a brief role description. |

## Blog-specific

| Component | Class / tag | Purpose |
|---|---|---|
| Breadcrumb | `.article-breadcrumb` | Home / Blog / Title navigation, also expresses schema.org |
| Blockquote | `<blockquote>` + `<cite>` | Third-party quotes with decorative curly quote |
| Callout | `.article-callout` | Author insights, highlighted accent box |
| Code block | `.article-code-block` | Monospace block with copy button |
| Table wrapper | `.table-wrapper` → `<table>` | Horizontal scroll on mobile |
| Image left | `.article-img-left` | Image + text side by side, collapses on mobile |
| Image right | `.article-img-right` | Mirror of above |
| Image centered | `<figure class="article-img-center">` | Full-width image with caption |
| CTA inline | `.article-cta-inline` | Mid-article call to action with corner pluses |
| FAQ | `.article-faq` + `.article-faq-item.open` | Accordion with SEO FAQPage schema |
| Podcast player | `.article-podcast` | 2-voice NotebookLM-style player |

### Blog — card (index)

```html
<a href="/blog/<slug>/" class="blog-card">
    <img src="/assets/illustrations-blog/<slug>.webp" alt="<alt>" width="640" height="360" loading="lazy">
    <div class="blog-card-body">
        <h2 class="blog-card-title"><title></h2>
        <p class="blog-card-meta"><YYYY-MM-DD> · <N> min read</p>
        <p class="blog-card-excerpt"><first paragraph of the article, verbatim></p>
        <span class="blog-card-more">Lire plus / Read more</span>
    </div>
</a>
```

`.blog-card-excerpt` clips to 6 lines (`max-height`) and fades out the last 3 via a `mask-image` gradient rather than a hard cutoff; `.blog-card-more` is a plain accent-colored label, not a separate link (the whole card is already the `<a>`).

### Blog — FAQ item

```html
<div class="article-faq-item">
    <button class="article-faq-question">
        <question>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14"/><path d="M5 12h14"/></svg>
    </button>
    <div class="article-faq-answer">
        <div class="article-faq-answer-inner"><answer></div>
    </div>
</div>
```

Accordion JS (inline per article):

```javascript
document.querySelectorAll('.article-faq-question').forEach(q => {
    q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
});
```

### Blog — podcast player

```html
<div class="article-podcast" id="podcastPlayer">
    <button class="podcast-play" id="podcastPlayBtn" aria-label="Play podcast">
        <svg viewBox="0 0 24 24" id="podcastPlayIcon"><polygon points="6,3 20,12 6,21"/></svg>
    </button>
    <div class="podcast-info">
        <p class="podcast-label">Audio podcast</p>
        <p class="podcast-title"><short title></p>
    </div>
    <div class="podcast-progress">
        <div class="podcast-bar" id="podcastBar"><div class="podcast-bar-fill" id="podcastFill"></div></div>
        <span class="podcast-time" id="podcastTime">0:00 / 0:00</span>
    </div>
    <audio id="podcastAudio" preload="none" src="/assets/audio-blog/<slug>.mp3"></audio>
</div>
```

Player JS (inline per article):

```javascript
(function() {
    const audio = document.getElementById('podcastAudio');
    const playBtn = document.getElementById('podcastPlayBtn');
    const playIcon = document.getElementById('podcastPlayIcon');
    const fill = document.getElementById('podcastFill');
    const bar = document.getElementById('podcastBar');
    const timeEl = document.getElementById('podcastTime');
    if (!audio || !playBtn) return;
    const fmt = s => { const m = Math.floor(s/60); const sec = Math.floor(s%60); return m+':'+(sec<10?'0':'')+sec; };
    playBtn.addEventListener('click', () => {
        if (audio.paused) { audio.play(); playIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>'; }
        else { audio.pause(); playIcon.innerHTML = '<polygon points="6,3 20,12 6,21"/>'; }
    });
    audio.addEventListener('timeupdate', () => { if (audio.duration) { fill.style.width = (audio.currentTime/audio.duration*100)+'%'; timeEl.textContent = fmt(audio.currentTime)+' / '+fmt(audio.duration); } });
    bar.addEventListener('click', e => { const r = bar.getBoundingClientRect(); audio.currentTime = (e.clientX-r.left)/r.width*audio.duration; });
    audio.addEventListener('ended', () => { playIcon.innerHTML = '<polygon points="6,3 20,12 6,21"/>'; fill.style.width = '0%'; });
})();
```

