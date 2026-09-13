# Brevo integration

## Steps

1. Copy `api/brevo.php.example` to `api/brevo.php` and customize the `$LISTS` map with your Brevo list IDs.
2. Set in server `.env`:
   ```
   BREVO_API_KEY=xkeysib-...
   BREVO_LIST_DEFAULT=<list-id>
   ```
3. Add a form that posts JSON to `/api/brevo.php`.

## Minimal form

```html
<form id="newsletter-form" class="newsletter-form">
    <label for="email" class="sr-only">Email</label>
    <input id="email" type="email" name="email" placeholder="you@example.com" required>
    <button type="submit" class="btn-primary">Subscribe</button>
    <p class="form-status" aria-live="polite"></p>
</form>

<script>
(function () {
    const form = document.getElementById('newsletter-form');
    const status = form.querySelector('.form-status');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        status.textContent = 'Sending…';
        try {
            const res = await fetch('/api/brevo.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email: form.email.value, source: 'newsletter' })
            });
            const data = await res.json();
            status.textContent = data.success ? 'Thanks — check your inbox.' : (data.error || 'Something went wrong.');
            if (data.success) form.reset();
        } catch (err) {
            status.textContent = 'Network error. Try again.';
        }
    });
})();
</script>
```

## CSP delta

```
script-src 'self' 'unsafe-inline' https://cdn.brevo.com https://sibautomation.com;
connect-src 'self' https://*.brevo.com https://sibautomation.com;
```

(Only required if you load the Brevo tracking SDK in the browser; the PHP proxy alone needs no CSP changes.)
