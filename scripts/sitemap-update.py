#!/usr/bin/env python3
"""
═══════════════════════════════════════
SITEMAP UPDATE
Regenerates sitemap.xml from the HTML files found in the repo root.
Discovers every index.html under top-level directories and each blog article.

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

PRIORITY = {
    "": "1.0",
    "about": "0.8",
    "projects": "0.8",
    "blog": "0.8",
    "legal": "0.3",
}
CHANGEFREQ = {
    "": "weekly",
    "about": "monthly",
    "projects": "monthly",
    "blog": "weekly",
    "legal": "yearly",
}

DEFAULT_ARTICLE_PRIORITY = "0.7"
DEFAULT_ARTICLE_CHANGEFREQ = "monthly"


def discover() -> list[tuple[str, str, str]]:
    """Return [(loc, priority, changefreq)] for all HTML pages."""
    entries: list[tuple[str, str, str]] = []

    # Home
    if (ROOT / "index.html").exists():
        entries.append((f"{SITE_URL}/", PRIORITY[""], CHANGEFREQ[""]))

    # Top-level directories with index.html
    for sub in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if sub.name.startswith(".") or sub.name in {"assets", "api", "scripts", "docs", "node_modules"}:
            continue
        if (sub / "index.html").exists():
            key = sub.name
            entries.append((f"{SITE_URL}/{key}/", PRIORITY.get(key, "0.7"), CHANGEFREQ.get(key, "monthly")))
        # Recurse one level for blog/<slug>/index.html, projects/<slug>/index.html, legal/<slug>/index.html
        for sub2 in sorted(p for p in sub.iterdir() if p.is_dir()):
            if (sub2 / "index.html").exists() and not sub2.name.startswith("_"):
                if sub.name == "blog":
                    entries.append((f"{SITE_URL}/blog/{sub2.name}/", DEFAULT_ARTICLE_PRIORITY, DEFAULT_ARTICLE_CHANGEFREQ))
                elif sub.name == "legal":
                    entries.append((f"{SITE_URL}/legal/{sub2.name}/", "0.3", "yearly"))
                elif sub.name == "projects":
                    entries.append((f"{SITE_URL}/projects/{sub2.name}/", "0.7", "monthly"))
                else:
                    entries.append((f"{SITE_URL}/{sub.name}/{sub2.name}/", "0.6", "monthly"))
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
