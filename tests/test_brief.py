import unittest

from father_media_lab.brief import BriefValidationError, CreativeBrief


VALID = {
    "brief_id": "TEST-001",
    "product_type": "social_card",
    "purpose": "test",
    "audience": "tester",
    "style": "minimal",
    "width": 1024,
    "height": 768,
    "palette": ["#112233", "#AABBCC"],
    "required_elements": ["title"],
    "forbidden_elements": ["logo"],
}


class BriefTests(unittest.TestCase):
    def test_valid_brief_is_canonical(self):
        first = CreativeBrief.from_dict(VALID)
        second = CreativeBrief.from_dict(dict(reversed(list(VALID.items()))))
        self.assertEqual(first.canonical_json(), second.canonical_json())

    def test_invalid_color_fails_closed(self):
        data = {**VALID, "palette": ["blue"]}
        with self.assertRaises(BriefValidationError):
            CreativeBrief.from_dict(data)

    def test_required_forbidden_conflict_fails_closed(self):
        data = {**VALID, "forbidden_elements": ["TITLE"]}
        with self.assertRaises(BriefValidationError):
            CreativeBrief.from_dict(data)
