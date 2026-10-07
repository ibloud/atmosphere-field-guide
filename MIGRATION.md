# Atmosphere guide domain migration

Target: https://atmosphere.loptrlab.com/ . Maintained source remains in ibloud/pixie-device-stewardship; deployment lives in ibloud/atmosphere-field-guide.

1. Enable GitHub Pages with GitHub Actions in this repository.
2. Run the deployment workflow and verify its published static guide.
3. Configure atmosphere.loptrlab.com as this repository's Pages custom domain.
4. At the existing DNS provider add CNAME **atmosphere** → **ibloud.github.io**. Do not point a DNS CNAME at a URL path or move the entire PIXIE Device Stewardship site's domain.
5. Complete the Pages DNS check and certificate issuance; enforce HTTPS when available.
6. Only after HTTPS works, merge the prepared legacy-page redirect and navigation changes in PIXIE Device Stewardship. Update directory links to the new guide home while keeping /ecosystem/ as the central project directory.

Rollback: restore the previous atmosphere.html guide if the custom domain fails. Existing links remain working throughout staging; no mail, apex-domain or other subdomain records need changes.
