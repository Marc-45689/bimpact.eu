# docs/

Internal documentation. Not deployed to production (the GitHub Actions workflow strips this folder before SFTP upload, except `docs/**/*.pdf` which are whitelisted).

## Structure

- `brand/` — source of truth for the brand. Claude reads `brand.md` at the start of every working session.
- `components.md` — catalog of reusable HTML/CSS components. Auto-updated by `/new-page` and `/new-section`.
- `inspirations/` — moodboard images (gitignored by default).
- `content/` — raw texts, briefs, transcripts (gitignored).
- `drafts/` — draft ideas (gitignored).
- `superpowers/specs/` — design documents per feature. Kept in git.
- `superpowers/plans/` — implementation plans per feature. Kept in git.
- `migration/` — dump of a CMS site being migrated (gitignored, created by `/adopt-existing-site` in CMS scenario).
