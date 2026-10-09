<?php
/**
 * ═══════════════════════════════════════
 * ENV LOADER
 * Reads .env at the site root and exposes values
 * via getenv(). Include this at the top of every
 * PHP endpoint in api/:
 *
 *     require_once __DIR__ . '/_env.php';
 *     $key = getenv('BREVO_API_KEY') ?: '';
 *
 * The .env file must NEVER be committed to git.
 * Preferred location: OUTSIDE the docroot, in the
 * home directory (/home/<account>/.env-bimpact),
 * shared by staging and production. There it can
 * neither be served over the web nor be wiped by
 * the `rsync --delete` of the cPanel deploy. A
 * legacy .env at the site root is still read as a
 * fallback.
 * Written for PHP 7.2+ (no PHP 8-only functions).
 * ═══════════════════════════════════════
 */

(function () {
    $envPath = false;
    foreach ([dirname(__DIR__, 2) . '/.env-bimpact', __DIR__ . '/../.env'] as $candidate) {
        $resolved = realpath($candidate);
        if ($resolved !== false && is_readable($resolved)) {
            $envPath = $resolved;
            break;
        }
    }
    if ($envPath === false) {
        return;
    }

    $lines = @file($envPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if ($lines === false) return;

    foreach ($lines as $line) {
        $line = trim($line);
        if ($line === '' || $line[0] === '#') continue;

        $eq = strpos($line, '=');
        if ($eq === false) continue;

        $name  = trim(substr($line, 0, $eq));
        $value = trim(substr($line, $eq + 1));

        if (strlen($value) >= 2) {
            $first = $value[0];
            $last  = $value[strlen($value) - 1];
            if (($first === '"' && $last === '"') || ($first === "'" && $last === "'")) {
                $value = substr($value, 1, -1);
            }
        }

        if ($name !== '' && getenv($name) === false) {
            putenv("$name=$value");
        }
    }
})();
