import unittest

import numpy as np

from backend.ai_modules.rppg.heart_rate import HeartRateCalculator


class TestHeartRateCalculator(unittest.TestCase):
    def setUp(self):
        self.fps = 30
        self.calc = HeartRateCalculator(fps=self.fps)

    def test_compute_heart_rate_from_sine(self):
        seconds = 10
        n = self.fps * seconds
        t = np.arange(n) / self.fps

        freq_hz = 1.2  # 72 BPM
        green = np.sin(2 * np.pi * freq_hz * t)
        signal = np.stack([green, green, green], axis=1)

        bpm = self.calc._compute_heart_rate(signal)
        self.assertAlmostEqual(bpm, 72.0, delta=0.2)

    def test_compute_respiration_rate_from_sine(self):
        seconds = 20
        n = self.fps * seconds
        t = np.arange(n) / self.fps

        freq_hz = 0.25  # 15 RPM
        green = np.sin(2 * np.pi * freq_hz * t)
        signal = np.stack([green, green, green], axis=1)

        rpm = self.calc._compute_respiration_rate(signal)
        self.assertAlmostEqual(rpm, 15.0, delta=0.2)

    def test_calculate_insufficient_data(self):
        short_signal = np.zeros((10, 3), dtype=np.float32)
        out = self.calc.calculate(short_signal)

        self.assertEqual(out["status"], "not_enough_data")
        self.assertEqual(out["heart_rate_bpm"], 0.0)
        self.assertEqual(out["respiration_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
