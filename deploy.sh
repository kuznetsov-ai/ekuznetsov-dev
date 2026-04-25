#!/bin/bash
# Deploy ekuznetsov.dev to Firebase Hosting.
# Prerequisite: firebase-tools installed and logged in (firebase login).

set -e

cd "$(dirname "$0")"

echo "→ Deploying to Firebase Hosting (project: $(jq -r .projects.default .firebaserc 2>/dev/null || echo 'default from .firebaserc'))"
echo ""

firebase deploy --only hosting

echo ""
echo "Done. Live at: https://ekuznetsov.dev"
