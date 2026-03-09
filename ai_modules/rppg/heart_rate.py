"""
heart_rate.py
-------------
Sprint 1 : Skeleton — Calculate BPM and respiration rate from filtered signal.
Sprint 2 : Will apply FFT to extract dominant frequency peaks.
"""

import numpy as np


class HeartRateCalculator:
    """
    Takes the filtered rPPG signal and computes:
    - Heart Rate in BPM (beats per minute)
    - Respiration Rate in breaths/min

    Method : FFT (Fast Fourier Transform) on the green channel
    which carries the strongest pulse signal.
    """

    def __init__(self, fps: int = 30):
        """
        Args:
            fps: frames per second — needed to convert FFT frequency to BPM
        """
        self.fps = fps

        # Frequency ranges
        self.hr_freq_low  = 0.7   # Hz → 42 BPM
        self.hr_freq_high = 4.0   # Hz → 240 BPM
        self.rr_freq_low  = 0.1   # Hz → 6 breaths/min
        self.rr_freq_high = 0.5   # Hz → 30 breaths/min

    def calculate(self, filtered_signal: np.ndarray) -> dict:
        """
        Main method — computes heart rate and respiration rate.

        Args:
            filtered_signal: numpy array (N, 3) from SignalFilter

        Returns:
            dict with BPM, respiration rate, and signal quality
        """
        if filtered_signal is None or len(filtered_signal) < 30:
            return self._placeholder_output("not_enough_data")

        heart_rate_bpm    = self._compute_heart_rate(filtered_signal)
        respiration_rate  = self._compute_respiration_rate(filtered_signal)
        signal_quality    = self._assess_quality(filtered_signal)

        return {
            "heart_rate_bpm"   : heart_rate_bpm,
            "respiration_rate" : respiration_rate,
            "signal_quality"   : signal_quality,
            "status"           : "placeholder_output"   # Sprint 1 marker
        }

    def _compute_heart_rate(self, signal: np.ndarray) -> float:
        """
        Uses FFT on the green channel to find dominant pulse frequency.

        Sprint 1 : returns placeholder value of 72 BPM.
        Sprint 2 : implement FFT peak detection:
            green = signal[:, 1]
            freqs = np.fft.rfftfreq(len(green), d=1/self.fps)
            power = np.abs(np.fft.rfft(green))
            # mask to HR range, find peak
        """
        # TODO Sprint 2 : real FFT-based calculation
        return 72.0  # placeholder

    def _compute_respiration_rate(self, signal: np.ndarray) -> float:
        """
        Uses FFT on the signal to find dominant respiration frequency.

        Sprint 1 : returns placeholder value of 16 breaths/min.
        Sprint 2 : same as heart rate but with lower frequency range.
        """
        # TODO Sprint 2 : real FFT-based calculation
        return 16.0  # placeholder

    def _assess_quality(self, signal: np.ndarray) -> str:
        """
        Assesses the quality of the signal (motion artifacts, lighting).

        Sprint 1 : always returns 'good' as placeholder.
        Sprint 2 : compute SNR or variance-based quality score.
        """
        # TODO Sprint 2 : real quality assessment
        return "good"  # placeholder

    def _placeholder_output(self, reason: str) -> dict:
        return {
            "heart_rate_bpm"   : 0.0,
            "respiration_rate" : 0.0,
            "signal_quality"   : "insufficient_data",
            "status"           : reason
        }
