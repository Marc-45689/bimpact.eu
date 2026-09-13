# Integration snippets

Reference snippets used by `/setup-integration`. Each file shows the HTML/JS/PHP and the CSP delta that activates the module. `/setup-integration` reads these when wiring an existing site after `/start-new-site` has already run.

Keep these terse and copy-pastable — `/setup-integration` reads the snippet, asks the user for the variant (e.g. Cal.com vs Calendly), then inserts it.

## Files

- `booking-cal.md`
- `booking-calendly.md`
- `crm-brevo.md`
- `crm-mailchimp.md`
- `analytics-ga4.md`
- `analytics-plausible.md`
- `analytics-umami.md`
- `cookies-local.md`
- `cookies-tarteaucitron.md`
