import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from father_media_lab.brief import CreativeBrief
from father_media_lab.prototype import run_prototype
from test_brief import VALID


class PrototypeTests(unittest.TestCase):
    def test_run_creates_deterministic_evidence(self):
        brief = CreativeBrief.from_dict(VALID)
        with TemporaryDirectory() as first_dir, TemporaryDirectory() as second_dir:
            first = run_prototype(brief, first_dir)
            second = run_prototype(brief, second_dir)
            self.assertEqual(first.svg_path.read_bytes(), second.svg_path.read_bytes())
            first_passport = json.loads(first.passport_path.read_text(encoding="utf-8"))
            second_passport = json.loads(second.passport_path.read_text(encoding="utf-8"))
            self.assertEqual(first_passport, second_passport)
            self.assertFalse(first_passport["safety"]["network_used"])
            self.assertIn("SDXL integration", first_passport["not_proved"])

    def test_svg_escapes_user_text(self):
        brief = CreativeBrief.from_dict({**VALID, "text": "<script>alert(1)</script>"})
        with TemporaryDirectory() as directory:
            result = run_prototype(brief, directory)
            svg = result.svg_path.read_text(encoding="utf-8")
            self.assertNotIn("<script>", svg)
            self.assertIn("&lt;script&gt;", svg)
