#!/usr/bin/env bash
set -euo pipefail

rm -rf upstream .preview/dist
mkdir -p .preview/dist
git clone --depth=1 --single-branch --branch main https://github.com/ibloud/pixie-device-stewardship.git upstream
npm ci --prefix upstream/tools/atmosphere-guide
npm run build --prefix upstream/tools/atmosphere-guide
python3 tools/prepare-guide.py
cp -R upstream/tools/atmosphere-guide/dist/client .preview/dist/client
