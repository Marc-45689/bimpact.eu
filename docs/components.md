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
| Mobile drawer | `.nav-links.open` | Hamburger-triggered side drawer under 860px |

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
    </div>
</a>
```

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

## Projects-specific

| Component | Class | Purpose |
|---|---|---|
| Project card | `.project-card` | Grid card for the projects index |
| Project grid | `.projects-grid` | Responsive grid (auto-fill minmax 320px) |
