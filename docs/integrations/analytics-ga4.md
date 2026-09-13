# Google Analytics 4

## Env

```
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
```

## Snippet — inject into `<head>` of every page, gated by the GA markers so the staging workflow strips it:

```html
<!-- GA_START -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    // Only track after consent if cookie module is active.
    window.addEventListener('cookies:accepted', () => {
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    });
    // No consent module? Uncomment to run immediately:
    // gtag('js', new Date()); gtag('config', 'G-XXXXXXXXXX');
</script>
<!-- GA_END -->
```

Replace `G-XXXXXXXXXX` with the actual `GA4_MEASUREMENT_ID`.

## CSP delta

```
script-src 'self' 'unsafe-inline' https://www.googletagmanager.com;
connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com;
```
