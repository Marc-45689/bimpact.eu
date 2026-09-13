# Plausible Analytics

Cookie-free, GDPR-friendly. Recommended default.

## Env

```
PLAUSIBLE_DOMAIN=example.com
```

## Snippet in `<head>`

```html
<script defer data-domain="example.com" src="https://plausible.io/js/script.js"></script>
```

If self-hosting, replace the `src` with your instance. For outbound / file download tracking:

```html
<script defer data-domain="example.com" src="https://plausible.io/js/script.outbound-links.file-downloads.js"></script>
```

## CSP delta

```
script-src 'self' 'unsafe-inline' https://plausible.io;
connect-src 'self' https://plausible.io;
```
