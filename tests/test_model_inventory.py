import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from father_media_lab.model_inventory import inventory_models, write_inventory


class ModelInventoryTests(unittest.TestCase):
    def test_inventory_hashes_weights_and_skips_environment(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "models" / "checkpoints" / "demo-sdxl.safetensors"
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_bytes(b"checkpoint-fixture")
            environment = root / ".venv" / "Lib" / "ignored.gguf"
            environment.parent.mkdir(parents=True)
            environment.write_bytes(b"not-a-project-model")

            result = inventory_models(root)

            self.assertEqual(result["summary"]["total"], 1)
            self.assertEqual(result["artifacts"][0]["role_inferred"], "checkpoint")
            self.assertEqual(result["artifacts"][0]["family_inferred"], "sdxl")
            self.assertFalse(result["safety"]["model_contents_loaded"])
            self.assertNotIn(str(root), json.dumps(result))

    def test_lora_and_gguf_are_classified_fail_closed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            lora = root / "models" / "loras" / "portrait.safetensors"
            llm = root / "data" / "models" / "Qwen-demo.gguf"
            lora.parent.mkdir(parents=True)
            llm.parent.mkdir(parents=True)
            lora.write_bytes(b"lora")
            llm.write_bytes(b"llm")

            result = inventory_models(root)

            self.assertEqual(result["summary"]["by_role"]["lora"], 1)
            self.assertEqual(result["summary"]["by_role"]["language_or_embedding"], 1)
            self.assertTrue(
                all(item["license_status"] == "UNVERIFIED" for item in result["artifacts"])
            )

    def test_report_and_passport_are_stable(self):
        with TemporaryDirectory() as directory:
            root = Path(directory) / "models"
            root.mkdir()
            (root / "model.gguf").write_bytes(b"stable")
            first, first_passport = write_inventory(root, Path(directory) / "first.json")
            second, second_passport = write_inventory(root, Path(directory) / "second.json")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            first_data = json.loads(first_passport.read_text(encoding="utf-8"))
            second_data = json.loads(second_passport.read_text(encoding="utf-8"))
            self.assertEqual(first_data["run_id"], second_data["run_id"])
