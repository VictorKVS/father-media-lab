# Security policy

## Public/private boundary

This repository is public. Treat every committed byte as permanently disclosed, including deleted history.

Allowed: source code, specifications, synthetic fixtures, small licensed showcase media, hashes, non-sensitive run metadata and model manifests.

Forbidden: secrets, credentials, personal data, client inputs, confidential prompts, model weights, unlicensed assets, raw production logs and bulk generated output.

## Local workspace

Private artifacts are kept outside Git in `G:\1\father-media-lab`. A local disk alone is not a security control. Use operating-system access controls, encryption where appropriate, offline backup and a second verified copy.

## Before every commit

1. Inspect `git status` and the staged diff.
2. Scan staged content and history for secrets.
3. Confirm licenses and provenance for every media asset.
4. Confirm model files are represented only by manifests and SHA-256.
5. Remove metadata containing names, coordinates, device identifiers or client information.
6. Never rewrite or delete negative experiment evidence merely to improve the showcase.

## Incident response

If a secret is committed, remove it from use immediately, rotate/revoke it at the provider, document the incident and clean Git history only after rotation. Deleting the file in a later commit is not sufficient.

## Model and media risks

A successful generation does not prove originality, factual accuracy, identity consent, trademark safety or commercial-use rights. These are blocking review gates, not warning labels.
