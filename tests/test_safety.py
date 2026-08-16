import unittest

import father_media_lab


class SafetyBoundaryTests(unittest.TestCase):
    def test_public_repository_rejects_model_weights(self):
        self.assertTrue(father_media_lab.PUBLIC_REPOSITORY)
        self.assertFalse(father_media_lab.MODEL_WEIGHTS_ALLOWED_IN_GIT)

    def test_remote_and_video_claims_start_closed(self):
        self.assertFalse(father_media_lab.REMOTE_GENERATION_ENABLED)
        self.assertFalse(father_media_lab.VIDEO_GENERATION_PROVEN)


if __name__ == "__main__":
    unittest.main()
