# Getting to Know the Atmosphere

A PIXIE field guide by Loptr Lab. Intended public home: https://atmosphere.loptrlab.com/ .

The maintained guide source lives in [PIXIE Device Stewardship](https://github.com/ibloud/pixie-device-stewardship/tree/main/tools/atmosphere-guide). This repository provides its independent GitHub Pages deployment so the PIXIE research site retains its own address.

## Deploy

Push a deployment change here or run **Deploy Atmosphere guide** from Actions. The workflow builds the current PIXIE guide source, copies its original Made Sick icon and repaired orbit image, applies the guide's canonical/social metadata, and deploys only static assets. No login, analytics or publishing integration is added.

Changes to the upstream source require a fresh manual workflow run here. The build records the upstream commit in source-version.json.

## Atmosphere Independence Kit — November 23, 2026

The maintained source now includes a free starter kit for artist-owned PDS identities and carefully planned migrations from another PDS: [PDS kit source](https://github.com/ibloud/pixie-device-stewardship/tree/main/tools/atmosphere-guide/pds-kit). It includes deployment and provider-selection documentation, migration safety gates, a read-only server preflight, a pinned official installer download with checksum, and a separate execution wrapper requiring explicit confirmation. Account/DID/PLC migration is not automated; use the official migration guidance and rehearse with a disposable account. After source changes merge, run **Deploy Atmosphere guide** to publish the refreshed guide.

## Field Note 012 — Your Infrastructure Is a Business Decision

The maintained guide now includes an essay on creative independence, ownership, network effects, platform dependency, and the economics of running your own infrastructure. It is published in the guide as an in-page **Field Note 012** and is also maintained as source in [PIXIE Device Stewardship](https://github.com/ibloud/pixie-device-stewardship/blob/main/tools/atmosphere-guide/field-notes/your-infrastructure-is-a-business-decision.md).

The article emphasizes informed choices rather than blanket self-hosting: convenience, distribution, expertise, ownership, control, and exit options all have costs and value. No PDS or hosting provider sponsorship, affiliate, referral commission, or promotional obligation is involved.

## Infrastructure Architecture — November 23, 2026

The new [Infrastructure Architecture working note](https://github.com/ibloud/pixie-device-stewardship/blob/main/docs/INFRASTRUCTURE-ARCHITECTURE.md) separates PDS identity/records, game runtime, static delivery, object storage, private Creator OS data, and realtime game services. It proposes a hybrid owned-node/VPS/object-storage strategy, procurement and operating-cost gates, and a staged proof for Atmosphere game distribution. This is a proposal—not a claim of deployment.

## Attribution

Guide curation, creative direction and accessibility approach: Dominique Devereaux / Loptr Lab. Initial resource collection: atblueprints and awesome-atproto contributors, whose CC0 credit and license remain linked from the guide. Individual resources retain their own authorship and licenses. Made Sick uses its supplied icon.

Central project directory: https://ibloud.github.io/ecosystem/ .

The old guide address must remain working until custom-domain DNS and HTTPS have been verified. See MIGRATION.md.

## Navigation repair release — October 21, 2026

Rebuild the existing guide from source commit `7e36d49c2ba47480da2e6e3c5d1421ab9ff03b6a`: remove the circular Create callout, clarify destination labels and resource counts, and repair the moved Bluesky lexicon link. Repository layout and hosting remain unchanged.
