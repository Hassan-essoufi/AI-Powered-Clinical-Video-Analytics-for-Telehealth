import unittest
from unittest.mock import patch

import numpy as np

from backend.ai_modules.rppg.rppg_extractor import RPPGExtractor


class TestRPPGExtractor(unittest.TestCase):
    def test_extract_uses_frame_fallback_when_roi_missing(self):
        extractor = RPPGExtractor(buffer_size=5)
        frame = np.ones((4, 4, 3), dtype=np.uint8) * 10

        with patch("backend.ai_modules.rppg.rppg_extractor.extract_roi", return_value=None):
            out = extractor.extract(frame)

        self.assertEqual(out["r_mean"], 10.0)
        self.assertEqual(out["g_mean"], 10.0)
        self.assertEqual(out["b_mean"], 10.0)
        self.assertEqual(out["frame_count"], 1)

    def test_extract_invalid_frame_returns_zero_signal(self):
        extractor = RPPGExtractor(buffer_size=5)
        out = extractor.extract(None)

        self.assertEqual(out["r_mean"], 0.0)
        self.assertEqual(out["g_mean"], 0.0)
        self.assertEqual(out["b_mean"], 0.0)

    def test_signal_buffer_respects_maxlen(self):
        extractor = RPPGExtractor(buffer_size=3)
        frame = np.ones((2, 2, 3), dtype=np.uint8)

        with patch("backend.ai_modules.rppg.rppg_extractor.extract_roi", return_value=frame):
            for _ in range(5):
                extractor.extract(frame)

        self.assertEqual(len(extractor.signal_buffer), 3)
        self.assertEqual(len(extractor.frame_buffer), 3)


if __name__ == "__main__":
    unittest.main()
