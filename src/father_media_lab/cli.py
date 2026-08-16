"""Command-line interface for FATHER Media Lab."""

from __future__ import annotations

import argparse

from .brief import BriefValidationError, load_brief
from .model_inventory import write_inventory
from .prototype import run_prototype


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="father-media-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)
    prototype = subparsers.add_parser("prototype", help="run the offline criteria prototype")
    prototype.add_argument("--brief", required=True)
    prototype.add_argument("--output", required=True)
    inventory = subparsers.add_parser(
        "inventory-models", help="inventory local model files without loading them"
    )
    inventory.add_argument("--root", required=True)
    inventory.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "inventory-models":
            report, passport = write_inventory(args.root, args.output)
            print(report)
            print(passport)
            return 0
        brief = load_brief(args.brief)
        result = run_prototype(brief, args.output)
    except (BriefValidationError, ValueError) as error:
        print(f"BLOCKED: {error}")
        return 2
    print(result.svg_path)
    print(result.scorecard_path)
    print(result.passport_path)
    return 0
