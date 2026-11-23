# Getting to Know the Atmosphere

A PIXIE field guide by Loptr Lab. Intended public home: https://atmosphere.loptrlab.com/ .

The maintained guide source lives in [PIXIE Device Stewardship](https://github.com/ibloud/pixie-device-stewardship/tree/main/tools/atmosphere-guide). This repository provides its independent GitHub Pages deployment so the PIXIE research site retains its own address.

## Deploy

Push a deployment change here or run **Deploy Atmosphere guide** from Actions. The workflow builds the current PIXIE guide source, copies its original Made Sick icon and repaired orbit image, applies the guide's canonical/social metadata, and deploys only static assets. No login, analytics or publishing integration is added.

Changes to the upstream source require a fresh manual workflow run here. The build records the upstream commit in source-version.json.

## Atmosphere Independence Kit — November 23, 2026

The maintained source now includes a free starter kit for artist-owned PDS identities and carefully planned migrations from another PDS: [PDS kit source](https://github.com/ibloud/pixie-device-stewardship/tree/main/tools/atmosphere-guide/pds-kit). It includes deployment and provider-selection documentation, migration safety gates, a read-only server preflight, and a script that downloads the official installer for review without executing it. Account/DID/PLC migration is not automated; use the official migration guidance and rehearse with a disposable account. After source changes merge, run **Deploy Atmosphere guide** to publish the refreshed guide.

## Attribution

Guide curation, creative direction and accessibility approach: Dominique Devereaux / Loptr Lab. Initial resource collection: atblueprints and awesome-atproto contributors, whose CC0 credit and license remain linked from the guide. Individual resources retain their own authorship and licenses. Made Sick uses its supplied icon.

Central project directory: https://ibloud.github.io/ecosystem/ .

The old guide address must remain working until custom-domain DNS and HTTPS have been verified. See MIGRATION.md.

## Navigation repair release — October 21, 2026

Rebuild the existing guide from source commit `7e36d49c2ba47480da2e6e3c5d1421ab9ff03b6a`: remove the circular Create callout, clarify destination labels and resource counts, and repair the moved Bluesky lexicon link. Repository layout and hosting remain unchanged.
