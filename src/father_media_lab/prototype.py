"""Deterministic offline prototype: brief to SVG, scorecard and evidence passport."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from html import escape
import json
from pathlib import Path

from .brief import CreativeBrief


@dataclass(frozen=True)
class PrototypeResult:
    svg_path: Path
    scorecard_path: Path
    passport_path: Path


def _sha256_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render_prototype_svg(brief: CreativeBrief) -> bytes:
    """Render a deterministic criteria proof, not an AI-generated artwork."""
    colors = brief.palette
    band_width = brief.width / len(colors)
    bands = "".join(
        f'<rect x="{index * band_width:.3f}" y="0" width="{band_width + 0.01:.3f}" '
        f'height="{brief.height}" fill="{color}"/>'
        for index, color in enumerate(colors)
    )
    required = ", ".join(brief.required_elements) or "—"
    label = escape(brief.text or brief.product_type)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{brief.width}" '
        f'height="{brief.height}" viewBox="0 0 {brief.width} {brief.height}">'
        f"{bands}"
        f'<rect x="{brief.width * 0.08:.3f}" y="{brief.height * 0.18:.3f}" '
        f'width="{brief.width * 0.84:.3f}" height="{brief.height * 0.64:.3f}" '
        'rx="24" fill="#000000" fill-opacity="0.72"/>'
        f'<text x="{brief.width / 2:.3f}" y="{brief.height * 0.42:.3f}" '
        'text-anchor="middle" fill="#ffffff" font-family="sans-serif" '
        f'font-size="{max(18, brief.width // 22)}">{label}</text>'
        f'<text x="{brief.width / 2:.3f}" y="{brief.height * 0.55:.3f}" '
        'text-anchor="middle" fill="#ffffff" font-family="sans-serif" '
        f'font-size="{max(12, brief.width // 38)}">Style: {escape(brief.style)}</text>'
        f'<text x="{brief.width / 2:.3f}" y="{brief.height * 0.64:.3f}" '
        'text-anchor="middle" fill="#ffffff" font-family="sans-serif" '
        f'font-size="{max(10, brief.width // 48)}">Required: {escape(required)}</text>'
        '<metadata>FATHER Media Lab offline criteria prototype; not generative AI output</metadata>'
        "</svg>\n"
    ).encode("utf-8")


def run_prototype(brief: CreativeBrief, output_dir: str | Path) -> PrototypeResult:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    brief_bytes = brief.canonical_json().encode("utf-8")
    brief_sha = _sha256_bytes(brief_bytes)
    run_id = f"FML-RUN-{brief_sha[:12].upper()}"
    svg_bytes = render_prototype_svg(brief)
    svg_sha = _sha256_bytes(svg_bytes)

    svg_path = output / "prototype.svg"
    scorecard_path = output / "scorecard.json"
    passport_path = output / "passport.json"
    svg_path.write_bytes(svg_bytes)

    scorecard = {
        "blocking_gate": "PASS",
        "brief_id": brief.brief_id,
        "checks": {
            "brief_schema_valid": True,
            "dimensions_valid": True,
            "palette_valid": True,
            "required_forbidden_conflict": False,
            "remote_generation_used": False,
        },
        "limitations": [
            "visual quality is not evaluated",
            "required elements are recorded but not visually detected",
            "output is a deterministic SVG criteria proof, not AI artwork",
        ],
        "run_id": run_id,
    }
    _write_json(scorecard_path, scorecard)

    passport = {
        "artifact_type": "offline_criteria_prototype",
        "brief": {"id": brief.brief_id, "sha256": brief_sha},
        "decision": "ACCEPT_CONTRACT_PROTOTYPE_ONLY",
        "evidence_chain": {
            "code": [
                "src/father_media_lab/brief.py",
                "src/father_media_lab/prototype.py",
            ],
            "design": "docs/specifications/fml-l1-pre-criteria-prototype.md",
            "hypothesis": "A formal brief can fail closed and produce deterministic evidence without a model provider.",
            "idea": "Prove the production contract before connecting SDXL.",
            "lesson": "Criteria validation is separable from aesthetic generation.",
            "requirement": "FML-L1-PRE",
            "test": ["tests/test_brief.py", "tests/test_prototype.py"],
        },
        "not_proved": [
            "SDXL integration",
            "aesthetic quality",
            "commercial suitability",
            "video generation",
        ],
        "output": {"path": "prototype.svg", "sha256": svg_sha},
        "run_id": run_id,
        "safety": {
            "model_weights_loaded": False,
            "network_used": False,
            "personal_data_expected": False,
            "remote_generation_used": False,
        },
        "schema_version": "1.0",
    }
    _write_json(passport_path, passport)
    return PrototypeResult(svg_path, scorecard_path, passport_path)
