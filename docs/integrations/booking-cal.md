# Cal.com integration

## Env

```
CAL_USERNAME=your-cal-username
CAL_EVENT_SLUG=15min
```

## Script (at the end of `<body>` on pages with the CTA)

```html
<script src="https://app.cal.com/embed/embed.js" async></script>
<script>
(function (C,A,L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); };})(window, "https://app.cal.com/embed/embed.js", "init");
Cal("init", "15min", {origin:"https://cal.com"});
Cal.ns["15min"]("ui", { theme: "dark", styles: { branding: { brandColor: "#F9DC5C" } } });
</script>
```

## Button

```html
<a href="https://cal.com/{CAL_USERNAME}/{CAL_EVENT_SLUG}"
   class="btn-primary"
   data-cal-link="{CAL_USERNAME}/{CAL_EVENT_SLUG}"
   data-cal-namespace="15min"
   data-cal-config='{"layout":"month_view","useSlotsViewOnSmallScreen":"true","theme":"dark"}'>
    Book a call
</a>
```

## CSP delta

```
script-src 'self' 'unsafe-inline' https://cdn.cal.com https://app.cal.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.cal.com;
connect-src 'self' https://app.cal.com https://*.cal.com;
frame-src 'self' https://app.cal.com;
```
