"""Offline inventory of local model artifacts without loading model contents."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ALLOWED_SUFFIXES = {
    ".ckpt",
    ".gguf",
    ".h5",
    ".keras",
    ".onnx",
    ".pt",
    ".pth",
    ".safetensors",
    ".tflite",
}
SKIP_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "site-packages",
    "venv",
}


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def infer_role(relative_path: Path) -> str:
    parts = {part.casefold() for part in relative_path.parts}
    if parts & {"lora", "loras", "lycoris"}:
        return "lora"
    if parts & {"vae", "vae_approx"}:
        return "vae"
    if parts & {"checkpoints", "checkpoint"}:
        return "checkpoint"
    if relative_path.suffix.casefold() == ".gguf":
        return "language_or_embedding"
    if parts & {"upscale_models", "upscalers"}:
        return "upscaler"
    return "unclassified_weight"


def infer_family(filename: str) -> str:
    name = filename.casefold()
    if any(value in name for value in ("sdxl", "dreamshaperxl", "juggernautxl", "realvisxl")):
        return "sdxl"
    if "v1-5" in name or "sd15" in name:
        return "sd15"
    if "flux" in name:
        return "flux"
    if "bge" in name:
        return "embedding"
    if any(value in name for value in ("gigachat", "qwen", "deepseek", "llama")):
        return "llm"
    if "taesdxl" in name:
        return "sdxl_preview"
    if "taesd3" in name:
        return "sd3_preview"
    if "taesd" in name:
        return "sd_preview"
    return "unknown"


def _eligible(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part.casefold() in SKIP_PARTS for part in relative.parts):
        return False
    suffix = path.suffix.casefold()
    if suffix not in ALLOWED_SUFFIXES:
        return False
    if suffix in {".pt", ".pth"}:
        role = infer_role(relative)
        return role in {"checkpoint", "lora", "vae", "upscaler"}
    return True


def inventory_models(root: str | Path) -> dict:
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError(f"inventory root is not a directory: {root}")

    records = []
    for path in sorted(root_path.rglob("*"), key=lambda value: str(value).casefold()):
        if path.is_symlink() or not path.is_file() or not _eligible(path, root_path):
            continue
        relative = path.relative_to(root_path)
        digest = sha256_file(path)
        records.append(
            {
                "artifact_id": f"FML-MODEL-{digest[:12].upper()}",
                "family_inferred": infer_family(path.name),
                "filename": path.name,
                "license_status": "UNVERIFIED",
                "relative_path": relative.as_posix(),
                "role_inferred": infer_role(relative),
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "status": "BLOCKED_UNTIL_PROVENANCE_AND_LICENSE_VERIFIED",
            }
        )

    by_role: dict[str, int] = {}
    for record in records:
        role = record["role_inferred"]
        by_role[role] = by_role.get(role, 0) + 1
    return {
        "artifacts": records,
        "root_disclosure": "RELATIVE_PATHS_ONLY",
        "safety": {
            "files_executed": False,
            "model_contents_loaded": False,
            "network_used": False,
            "symlinks_followed": False,
        },
        "schema_version": "1.0",
        "summary": {"by_role": dict(sorted(by_role.items())), "total": len(records)},
    }


def write_inventory(root: str | Path, output_path: str | Path) -> tuple[Path, Path]:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    report = inventory_models(root)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_sha = sha256_file(output)
    passport_path = output.with_suffix(".passport.json")
    passport = {
        "artifact_type": "local_model_inventory",
        "decision": "REVIEW_REQUIRED",
        "not_proved": [
            "model integrity against publisher hash",
            "model compatibility",
            "license and commercial-use rights",
            "generation quality",
        ],
        "report": {"path": output.name, "sha256": report_sha},
        "run_id": f"FML-INVENTORY-{report_sha[:12].upper()}",
        "safety": report["safety"],
        "schema_version": "1.0",
    }
    passport_path.write_text(
        json.dumps(passport, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output, passport_path
