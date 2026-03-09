"""
signal_filter.py
----------------
Sprint 1 : Skeleton — Filter noise from raw rPPG signals.
Sprint 2 : Will apply Butterworth bandpass filter using SciPy.
"""

import numpy as np


class SignalFilter:
    """
    Filters the raw RGB signal extracted by RPPGExtractor.
    Removes noise caused by movement and lighting changes.
    Applies a bandpass filter to isolate pulse frequency (0.7–4 Hz).
    """

    def __init__(self, fps: int = 30, freq_low: float = 0.7, freq_high: float = 4.0):
        """
        Args:
            fps      : frames per second of the video stream
            freq_low : lower bound of bandpass filter in Hz (pulse ~0.7Hz = 42 BPM)
            freq_high: upper bound of bandpass filter in Hz (pulse ~4Hz  = 240 BPM)
        """
        self.fps = fps
        self.freq_low = freq_low
        self.freq_high = freq_high

    def filter(self, signal: np.ndarray) -> np.ndarray:
        """
        Applies bandpass filter to the raw RGB signal buffer.

        Args:
            signal: numpy array of shape (N, 3) — N frames, RGB channels

        Returns:
            filtered signal of same shape (N, 3)
        """
        if signal is None or len(signal) < 10:
            # Not enough data yet — return as-is
            return signal

        # Sprint 1 : placeholder — returns signal unchanged
        # Sprint 2 : apply scipy.signal.butter + filtfilt here
        filtered = self._apply_bandpass(signal)

        return filtered

    def _apply_bandpass(self, signal: np.ndarray) -> np.ndarray:
        """
        Butterworth bandpass filter on each RGB channel.

        Sprint 1 : returns raw signal as placeholder.
        Sprint 2 : implement with:
            from scipy.signal import butter, filtfilt
            b, a = butter(N=4, Wn=[low, high], btype='bandpass', fs=self.fps)
            return filtfilt(b, a, signal, axis=0)
        """
        # TODO Sprint 2 : replace with real Butterworth filter
        return signal  # placeholder

    def detrend(self, signal: np.ndarray) -> np.ndarray:
        """
        Removes slow trends from the signal (e.g. lighting drift).

        Sprint 1 : placeholder.
        Sprint 2 : use np.detrend or a moving average subtraction.
        """
        # TODO Sprint 2 : np.detrend(signal, axis=0)
        return signal  # placeholder
