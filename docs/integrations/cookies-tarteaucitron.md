# tarteaucitron.js

French-origin consent manager with extensive service catalog (GA, Cal, Brevo, Hotjar, etc.). Pinned for reliability.

## Download (pinned, committed locally to avoid CSP headaches)

```bash
mkdir -p assets/js/tarteaucitron
curl -sL "https://cdn.jsdelivr.net/npm/tarteaucitronjs@1.17.1/tarteaucitron.min.js" \
  -o assets/js/tarteaucitron/tarteaucitron.min.js
curl -sL "https://cdn.jsdelivr.net/npm/tarteaucitronjs@1.17.1/css/tarteaucitron.css" \
  -o assets/js/tarteaucitron/tarteaucitron.css
curl -sL "https://cdn.jsdelivr.net/npm/tarteaucitronjs@1.17.1/tarteaucitron.services.js" \
  -o assets/js/tarteaucitron/tarteaucitron.services.js
```

## Bootstrap in `<head>` of every page

```html
<link rel="stylesheet" href="/assets/js/tarteaucitron/tarteaucitron.css">
<script src="/assets/js/tarteaucitron/tarteaucitron.min.js"></script>
<script src="/assets/js/tarteaucitron/tarteaucitron.services.js"></script>
<script>
tarteaucitron.init({
    "privacyUrl": "/legal/privacy/",
    "bodyPosition": "bottom",
    "hashtag": "#tarteaucitron",
    "cookieName": "tarteaucitron",
    "orientation": "bottom",
    "groupServices": false,
    "showAlertSmall": false,
    "cookieslist": true,
    "DenyAllCta": true,
    "AcceptAllCta": true,
    "highPrivacy": true,
    "handleBrowserDNTRequest": false,
    "removeCredit": true,
    "moreInfoLink": true,
    "useExternalCss": false
});
// Register your services:
// tarteaucitron.user.gtagUa = "G-XXXXXXXXXX";
// (tarteaucitron.job = tarteaucitron.job || []).push('gtag');
</script>
```

## CSP delta

If serving locally (as recommended): **none**. If loading from jsDelivr:

```
script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net;
```
