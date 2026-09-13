# Umami Analytics

Self-hostable, privacy-friendly, cookie-free.

## Env

```
UMAMI_HOST=https://analytics.example.com
UMAMI_WEBSITE_ID=00000000-0000-0000-0000-000000000000
```

## Snippet in `<head>`

```html
<script defer src="https://analytics.example.com/script.js" data-website-id="00000000-0000-0000-0000-000000000000"></script>
```

Replace values with your Umami instance host and website UUID.

## CSP delta

```
script-src 'self' 'unsafe-inline' https://analytics.example.com;
connect-src 'self' https://analytics.example.com;
```

(Whatever host you use for Umami, whitelist it in both directives.)
