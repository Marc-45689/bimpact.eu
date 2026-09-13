# Local cookie consent (minimal, dependency-free)

Ships with the starter. Activate by including the banner HTML + script in every page that loads analytics.

## Banner HTML (before `</body>`)

```html
<aside id="cookie-consent" role="region" aria-label="Cookie notice">
    <p>We use a single cookie to remember that you dismissed this notice. We only load analytics after you accept.</p>
    <div class="actions">
        <button data-cc-accept>Accept</button>
        <button data-cc-decline>Decline</button>
    </div>
</aside>
<link rel="stylesheet" href="/assets/css/cookie-consent.css">
<script src="/assets/js/cookie-consent.js" defer></script>
```

## Behavior

- Banner appears on first visit.
- On **Accept** → `localStorage.cc:choice:v1 = 'accept'` and window event `cookies:accepted` is dispatched.
- On **Decline** → stored and window event `cookies:declined` is dispatched.
- Analytics scripts should listen for `cookies:accepted` before initializing (see `analytics-ga4.md`).

## CSP delta

None. Everything is self-hosted.
