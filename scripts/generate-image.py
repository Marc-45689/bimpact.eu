#!/usr/bin/env python3
"""
═══════════════════════════════════════
GENERATE ILLUSTRATION
Uses Gemini Image API to generate a 16:9 illustration for a blog article
or a page. Reads the prompt template from docs/brand/illustration-prompt.md
and fills in the {{subject_description}} placeholder.

Outputs a WebP at 1200×675 with a normalized background color matching the
primary palette token (read from assets/css/tokens.css).

Requires:
    pip3 install google-genai pillow
    brew install webp    # for cwebp

Env:
    GEMINI_API_KEY

Usage:
    python3 scripts/generate-image.py \
        --slug "my-article" \
        --subject "Two marketers collaborating at a whiteboard"
═══════════════════════════════════════
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai not installed. Run: pip3 install google-genai pillow", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip3 install pillow", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = ROOT / "docs" / "brand" / "illustration-prompt.md"
TOKENS_FILE = ROOT / "assets" / "css" / "tokens.css"
OUTPUT_DIR = ROOT / "assets" / "illustrations-blog"


def load_prompt_template() -> str:
    if not PROMPT_FILE.exists():
        sys.exit(f"Prompt template not found: {PROMPT_FILE}")
    text = PROMPT_FILE.read_text(encoding="utf-8")
    # Extract the first ``` block
    m = re.search(r"```\s*\n(.*?)\n```", text, re.DOTALL)
    if not m:
        sys.exit("No prompt code block found in illustration-prompt.md")
    return m.group(1).strip()


def primary_bg_hex() -> str:
    """Read --midnight (or first dark background token) from tokens.css."""
    if not TOKENS_FILE.exists():
        return "#0D1B2A"
    text = TOKENS_FILE.read_text(encoding="utf-8")
    m = re.search(r"--midnight:\s*(#[0-9A-Fa-f]{6})", text)
    return m.group(1) if m else "#0D1B2A"


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def fix_background(image_path: Path, target_hex: str) -> None:
    """Normalize the image background to exactly target_hex."""
    target = hex_to_rgb(target_hex)
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            # Replace near-target dark backgrounds
            if abs(r - target[0]) < 28 and abs(g - target[1]) < 28 and abs(b - target[2]) < 28:
                pixels[x, y] = target
    img.save(image_path, "PNG")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="Article or page slug")
    parser.add_argument("--subject", required=True, help="{{subject_description}} value")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--size", default="2K")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY not set. Add it to your shell env or a .env file and `source` it.")

    template = load_prompt_template()
    bg_hex = primary_bg_hex()
    prompt = template.replace("{{subject_description}}", args.subject.strip())

    print(f"→ Prompt: {prompt[:180]}{'…' if len(prompt) > 180 else ''}")
    print(f"→ Background normalized to: {bg_hex}")

    model = os.getenv("GEMINI_IMAGE_MODEL", "imagen-3.0-generate-002")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=args.aspect_ratio,
        ),
    )
    if not response.generated_images:
        sys.exit("No image returned from Gemini.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUTPUT_DIR / f"{args.slug}.png"
    webp_path = OUTPUT_DIR / f"{args.slug}.webp"

    response.generated_images[0].image.save(str(png_path))
    fix_background(png_path, bg_hex)

    # Convert to WebP via cwebp
    subprocess.run(["cwebp", "-q", "82", str(png_path), "-o", str(webp_path)], check=True)
    png_path.unlink(missing_ok=True)

    print(f"✓ Written: {webp_path}")


if __name__ == "__main__":
    main()
