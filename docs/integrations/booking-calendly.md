# Calendly integration

## Env

```
CALENDLY_URL=https://calendly.com/your-account/15min
```

## Script (at the end of `<body>`)

```html
<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
<script src="https://assets.calendly.com/assets/external/widget.js" async></script>
```

## Inline embed

```html
<div class="calendly-inline-widget" data-url="{CALENDLY_URL}" style="min-width:320px;height:700px;"></div>
```

## Popup button

```html
<a href="#" onclick="Calendly.initPopupWidget({url:'{CALENDLY_URL}'});return false;" class="btn-primary">Book a call</a>
```

## CSP delta

```
script-src 'self' 'unsafe-inline' https://assets.calendly.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://assets.calendly.com;
connect-src 'self' https://calendly.com;
frame-src 'self' https://calendly.com;
```
