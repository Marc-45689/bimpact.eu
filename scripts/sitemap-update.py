#!/usr/bin/env python3
"""
═══════════════════════════════════════
SITEMAP UPDATE
Regenerates sitemap.xml from the HTML files found in the repo root.
Discovers every index.html under top-level directories and each blog
article, for both locale roots (French at the site root, English
under /en/ — see CLAUDE.md, "Languages").

Reads the base URL from SITE_URL env var or defaults to https://example.com.

Usage:
    python3 scripts/sitemap-update.py
    SITE_URL=https://example.com python3 scripts/sitemap-update.py
═══════════════════════════════════════
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"

SITE_URL = os.getenv("SITE_URL", "https://example.com").rstrip("/")

# One entry per locale root: (prefix, category dir name -> kind).
# "kind" drives priority/changefreq and whether/how a category recurses
# one level deeper (blog articles, legal sub-pages, project pages).
LOCALES = [
    ("", {"a-propos": "generic", "blog": "blog", "mentions-legales": "legal"}),
    ("en", {"about": "generic", "blog": "blog", "legal": "legal"}),
]

CATEGORY_PRIORITY = {"generic": "0.8", "blog": "0.8", "legal": "0.3"}
CATEGORY_CHANGEFREQ = {"generic": "monthly", "blog": "weekly", "legal": "yearly"}
SUBPAGE_PRIORITY = {"blog": "0.7", "legal": "0.3"}
SUBPAGE_CHANGEFREQ = {"blog": "monthly", "legal": "yearly"}

HOME_PRIORITY = {"": "1.0", "en": "0.7"}
HOME_CHANGEFREQ = {"": "weekly", "en": "monthly"}

SKIP_TOP_LEVEL = {"assets", "api", "scripts", "docs", "node_modules", "en"}


def discover() -> list[tuple[str, str, str]]:
    """Return [(loc, priority, changefreq)] for all HTML pages, across every locale root."""
    entries: list[tuple[str, str, str]] = []

    for prefix, categories in LOCALES:
        locale_root = ROOT / prefix if prefix else ROOT
        if not locale_root.is_dir():
            continue

        # Home for this locale
        if (locale_root / "index.html").exists():
            base = f"{SITE_URL}/{prefix}/" if prefix else f"{SITE_URL}/"
            entries.append((base, HOME_PRIORITY[prefix], HOME_CHANGEFREQ[prefix]))

        for dirname, kind in categories.items():
            category_dir = locale_root / dirname
            if not category_dir.is_dir():
                continue
            if (category_dir / "index.html").exists():
                loc = f"{SITE_URL}/{prefix}/{dirname}/" if prefix else f"{SITE_URL}/{dirname}/"
                entries.append((loc, CATEGORY_PRIORITY[kind], CATEGORY_CHANGEFREQ[kind]))
            if kind == "generic":
                continue
            # Recurse one level for blog/<slug>, legal/<slug>
            # (legal has an extra nesting level today only because its
            # sub-pages already live one level under mentions-legales/legal —
            # same depth as blog, just named differently.)
            for sub in sorted(p for p in category_dir.iterdir() if p.is_dir()):
                if (sub / "index.html").exists() and not sub.name.startswith("_"):
                    loc = f"{SITE_URL}/{prefix}/{dirname}/{sub.name}/" if prefix else f"{SITE_URL}/{dirname}/{sub.name}/"
                    entries.append((loc, SUBPAGE_PRIORITY[kind], SUBPAGE_CHANGEFREQ[kind]))

        # Any other top-level directory under this locale root that isn't a
        # known category still gets a generic fallback entry, matching the
        # starter's previous behavior for unlisted directories.
        known = set(categories) | {"_"}
        for sub in sorted(p for p in locale_root.iterdir() if p.is_dir()):
            if sub.name.startswith(".") or sub.name in SKIP_TOP_LEVEL or sub.name in known:
                continue
            if prefix == "" and sub.name == "en":
                continue
            if (sub / "index.html").exists():
                loc = f"{SITE_URL}/{prefix}/{sub.name}/" if prefix else f"{SITE_URL}/{sub.name}/"
                entries.append((loc, "0.7", "monthly"))

    return entries


def render(entries: list[tuple[str, str, str]]) -> str:
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, changefreq in entries:
        parts.extend([
            "    <url>",
            f"        <loc>{loc}</loc>",
            f"        <priority>{priority}</priority>",
            f"        <changefreq>{changefreq}</changefreq>",
            "    </url>",
        ])
    parts.append("</urlset>")
    return "\n".join(parts) + "\n"


def main() -> None:
    entries = discover()
    if not entries:
        sys.exit("No pages discovered. Check that HTML files exist at the expected locations.")
    SITEMAP.write_text(render(entries), encoding="utf-8")
    print(f"✓ sitemap.xml updated — {len(entries)} URLs")


if __name__ == "__main__":
    main()
