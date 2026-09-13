# Mailchimp integration

Mirror of `crm-brevo.md` using a Mailchimp PHP proxy. Create `api/mailchimp.php` by copying `api/brevo.php.example` and substituting the Mailchimp Members endpoint.

## Env

```
MAILCHIMP_API_KEY=...-us21
MAILCHIMP_AUDIENCE_ID=...
MAILCHIMP_SERVER_PREFIX=us21
```

## PHP proxy (sketch)

```php
require_once __DIR__ . '/_env.php';
header('Content-Type: application/json');
// ... same method/CORS gate as brevo.php.example ...

$API_KEY  = getenv('MAILCHIMP_API_KEY') ?: '';
$AUDIENCE = getenv('MAILCHIMP_AUDIENCE_ID') ?: '';
$DC       = getenv('MAILCHIMP_SERVER_PREFIX') ?: '';
if ($API_KEY === '' || $AUDIENCE === '' || $DC === '') { http_response_code(500); echo json_encode(['error' => 'server misconfigured']); exit; }

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input) || empty($input['email']) || !filter_var($input['email'], FILTER_VALIDATE_EMAIL)) {
    http_response_code(400); echo json_encode(['error' => 'invalid email']); exit;
}

$payload = [
    'email_address' => $input['email'],
    'status'        => 'pending', // double opt-in
    'merge_fields'  => array_filter([
        'FNAME' => $input['name'] ?? null,
    ]),
];

$ch = curl_init("https://{$DC}.api.mailchimp.com/3.0/lists/{$AUDIENCE}/members");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_USERPWD        => "anystring:{$API_KEY}",
    CURLOPT_POSTFIELDS     => json_encode($payload),
    CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
    CURLOPT_TIMEOUT        => 10,
]);
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

echo ($httpCode >= 200 && $httpCode < 300)
    ? json_encode(['success' => true])
    : json_encode(['error' => 'mailchimp error', 'status' => $httpCode]);
```

## CSP delta

None required if using server-side proxy only.
