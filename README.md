# FATHER Media Lab

Evidence-driven laboratory for reproducible image and video generation, model comparison and the **FATHER Creative Factory** business track.

> Status: `L0 — inventory and governance`. No model or business claim is accepted without evidence.

## Mission

Turn a creative request into a measurable and reproducible production chain:

`BRIEF → CRITERIA → DESIGN → GENERATE → CHECK → CRITIQUE → REVISE → ACCEPT → PACKAGE`

The first technical milestone is a reproducible SDXL image. Video generation is planned but is **not yet proven working**.

## Product tracks

- image generation from formal criteria;
- characters, mascots and consistent visual series;
- product cards and social-media packs;
- educational illustrations;
- comics, graphic stories and illustrated books;
- game assets and storyboards;
- image-to-video and text-to-video research;
- model-neutral evaluation and public evidence showcase.

## Repository boundary

This public repository contains code, specifications, tests, manifests, small licensed examples and evidence metadata.

It must never contain:

- API keys, tokens, passwords, cookies or `.env` files;
- checkpoints, LoRA, embeddings, VAE, GGUF or other model weights;
- virtual environments, caches, logs or generated bulk output;
- private client inputs, personal data or confidential prompts;
- assets without confirmed publication and commercial-use rights.

Local private workspace on the operator computer: `G:\1\father-media-lab`.
The local path is an operator convention, not a secret-storage guarantee. Sensitive material must additionally be access-controlled and backed up.

## Evidence lifecycle

Every meaningful experiment follows:

`IDEA → SOURCE → HYPOTHESIS → REQUIREMENT → DESIGN → CODE → TEST → RUN → RESULT → CRITIQUE → DECISION → LESSON`

## First gates

- `FML-L0`: legacy inventory, licenses, risks and hashes.
- `FML-L1`: one reproducible SDXL result with seed, config, model manifest, tests and SHA-256.
- `FML-B1`: three demo products — criteria-driven image, product card and short comic — each at MIN/STANDARD/PRO.
- `FML-L4`: first measured image-to-video pipeline. This gate is currently closed.

## Quick start

```powershell
git clone https://github.com/VictorKVS/father-media-lab.git G:\1\father-media-lab
cd G:\1\father-media-lab
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests -v
```

The initial package intentionally performs no model download and no remote generation.

### Inventory local model weights

The scanner hashes model files without executing them, follows no symlinks and
stores relative paths only:

```powershell
python -m father_media_lab inventory-models `
  --root "G:\1\Прежде\1_izobraznie\AI" `
  --output local-runs\model-inventory.json
```

Every discovered model remains blocked until provenance and license are verified.

### Offline criteria prototype

```powershell
python -m father_media_lab prototype `
  --brief examples/briefs/criteria-image-min.json `
  --output local-runs/demo-001
```

The command validates blocking criteria and creates `prototype.svg`,
`scorecard.json` and `passport.json`. The SVG is a deterministic contract proof,
not an AI-generated artwork. `local-runs/` is excluded from Git.

## Documentation

- [Product passport](docs/product-passport.md)
- [Implementation and business plan](docs/implementation-plan.md)
- [Security policy](SECURITY.md)
- [Model manifest example](configs/models.example.yaml)

## Safety

Generated media is not automatically unique, lawful, accurate or commercially usable. Model licenses, source rights, personal data, likeness, trademarks, age restrictions and publication terms require explicit review.
