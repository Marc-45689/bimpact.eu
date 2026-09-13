#!/usr/bin/env bash
# ═══════════════════════════════════════
# IMAGE OPTIMIZER
# Converts JPG/PNG to WebP q=82, keeps original.
# Requires: cwebp (brew install webp / apt install webp)
# ═══════════════════════════════════════

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <image.jpg|png> [quality=82]"
    exit 1
fi

INPUT="$1"
QUALITY="${2:-82}"

if [ ! -f "$INPUT" ]; then
    echo "File not found: $INPUT"
    exit 1
fi

if ! command -v cwebp >/dev/null 2>&1; then
    echo "cwebp not installed. macOS: brew install webp. Debian/Ubuntu: apt-get install webp"
    exit 1
fi

OUTPUT="${INPUT%.*}.webp"
cwebp -q "$QUALITY" "$INPUT" -o "$OUTPUT"

echo "Written: $OUTPUT"
