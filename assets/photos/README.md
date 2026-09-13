# Photos

Hero photos, team photos, testimonial avatars, project screenshots.

Optimize before committing:

    bash scripts/optimize-image.sh path/to/photo.jpg

Outputs `.webp` at quality 82, roughly halving file size.

Always set `width` and `height` attributes on `<img>` to prevent layout shift.
Always set `loading="lazy"` unless the image is above the fold.
