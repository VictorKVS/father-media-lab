"""Typed creative brief and fail-closed validation for the prototype."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


class BriefValidationError(ValueError):
    """Raised when a blocking brief criterion is invalid."""


@dataclass(frozen=True)
class CreativeBrief:
    brief_id: str
    product_type: str
    purpose: str
    audience: str
    style: str
    width: int
    height: int
    palette: tuple[str, ...]
    required_elements: tuple[str, ...]
    forbidden_elements: tuple[str, ...]
    text: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreativeBrief":
        required = (
            "brief_id",
            "product_type",
            "purpose",
            "audience",
            "style",
            "width",
            "height",
            "palette",
            "required_elements",
            "forbidden_elements",
        )
        missing = [key for key in required if key not in data]
        if missing:
            raise BriefValidationError(f"missing required fields: {', '.join(missing)}")

        brief = cls(
            brief_id=str(data["brief_id"]).strip(),
            product_type=str(data["product_type"]).strip(),
            purpose=str(data["purpose"]).strip(),
            audience=str(data["audience"]).strip(),
            style=str(data["style"]).strip(),
            width=int(data["width"]),
            height=int(data["height"]),
            palette=tuple(str(item) for item in data["palette"]),
            required_elements=tuple(str(item).strip() for item in data["required_elements"]),
            forbidden_elements=tuple(str(item).strip() for item in data["forbidden_elements"]),
            text=str(data.get("text", "")).strip(),
        )
        brief.validate()
        return brief

    def validate(self) -> None:
        empty = [
            name
            for name, value in (
                ("brief_id", self.brief_id),
                ("product_type", self.product_type),
                ("purpose", self.purpose),
                ("audience", self.audience),
                ("style", self.style),
            )
            if not value
        ]
        if empty:
            raise BriefValidationError(f"empty blocking fields: {', '.join(empty)}")
        if not (256 <= self.width <= 4096 and 256 <= self.height <= 4096):
            raise BriefValidationError("width and height must be between 256 and 4096")
        if not 1 <= len(self.palette) <= 8:
            raise BriefValidationError("palette must contain between 1 and 8 colors")
        invalid_colors = [color for color in self.palette if not HEX_COLOR.fullmatch(color)]
        if invalid_colors:
            raise BriefValidationError(f"invalid hex colors: {', '.join(invalid_colors)}")
        overlap = set(map(str.casefold, self.required_elements)) & set(
            map(str.casefold, self.forbidden_elements)
        )
        if overlap:
            raise BriefValidationError(
                f"elements cannot be both required and forbidden: {', '.join(sorted(overlap))}"
            )

    def canonical_json(self) -> str:
        return json.dumps(
            {
                "audience": self.audience,
                "brief_id": self.brief_id,
                "forbidden_elements": list(self.forbidden_elements),
                "height": self.height,
                "palette": list(self.palette),
                "product_type": self.product_type,
                "purpose": self.purpose,
                "required_elements": list(self.required_elements),
                "style": self.style,
                "text": self.text,
                "width": self.width,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def load_brief(path: str | Path) -> CreativeBrief:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BriefValidationError("brief root must be a JSON object")
    return CreativeBrief.from_dict(data)
