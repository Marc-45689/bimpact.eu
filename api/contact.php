<?php
/**
 * ═══════════════════════════════════════
 * CONTACT FORM ENDPOINT
 * Receives the site's contact form and emails the submission via PHP
 * mail() to the address in CONTACT_TO_EMAIL (server .env — never
 * hardcode the recipient here, this file is public on GitHub). Anti-spam
 * is a honeypot field (company_website, must stay empty) plus a minimum
 * fill time — no captcha, no third-party service.
 * ═══════════════════════════════════════
 */

require_once __DIR__ . '/_env.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: ' . (getenv('SITE_URL') ?: 'https://bimpact.eu'));
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST')     { http_response_code(405); echo json_encode(['error' => 'method not allowed']); exit; }

$TO = getenv('CONTACT_TO_EMAIL') ?: '';
if ($TO === '') {
    http_response_code(500);
    echo json_encode(['error' => 'server misconfigured']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid payload']);
    exit;
}

// Honeypot: real visitors never fill this hidden field. Bots that do get
// a fake success so they don't retry.
if (!empty($input['company_website'])) {
    echo json_encode(['success' => true]);
    exit;
}

// Filled in under 3 seconds of the page loading = almost certainly
// scripted, not a human reading three form fields.
$elapsed = isset($input['elapsed']) ? (int) $input['elapsed'] : 0;
if ($elapsed > 0 && $elapsed < 3000) {
    echo json_encode(['success' => true]);
    exit;
}

$name    = trim((string) ($input['name'] ?? ''));
$email   = trim((string) ($input['email'] ?? ''));
$phone   = trim((string) ($input['phone'] ?? ''));
$message = trim((string) ($input['message'] ?? ''));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid input']);
    exit;
}
if (mb_strlen($name) > 200 || mb_strlen($phone) > 40 || mb_strlen($message) > 5000) {
    http_response_code(400);
    echo json_encode(['error' => 'input too long']);
    exit;
}

// Header injection guard: strip CR/LF before these values ever reach a
// mail header (body-only fields don't need this, headers do).
$name  = str_replace(["\r", "\n"], '', $name);
$email = str_replace(["\r", "\n"], '', $email);
$phone = str_replace(["\r", "\n"], '', $phone);

$locale = in_array($input['locale'] ?? '', ['fr', 'en', 'es'], true) ? $input['locale'] : 'fr';

$subjects = [
    'fr' => 'Nouveau message via bimpact.eu',
    'en' => 'New message via bimpact.eu',
    'es' => 'Nuevo mensaje via bimpact.eu',
];
$subject = '=?UTF-8?B?' . base64_encode($subjects[$locale]) . '?=';

$phoneLine = $phone !== '' ? "Téléphone : $phone\n" : '';
$body = "Nom : $name\nEmail : $email\n{$phoneLine}\n$message\n";

$headers = implode("\r\n", [
    'From: BIMpact <no-reply@bimpact.eu>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=UTF-8',
]);

if (!mail($TO, $subject, $body, $headers)) {
    http_response_code(502);
    echo json_encode(['error' => 'send failed']);
    exit;
}

echo json_encode(['success' => true]);
