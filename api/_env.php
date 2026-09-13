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
 * Create it manually on the host via SFTP at the
 * site root.
 * ═══════════════════════════════════════
 */

(function () {
    $envPath = realpath(__DIR__ . '/../.env');
    if ($envPath === false || !is_readable($envPath)) {
        return;
    }

    $lines = @file($envPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if ($lines === false) return;

    foreach ($lines as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#')) continue;

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
