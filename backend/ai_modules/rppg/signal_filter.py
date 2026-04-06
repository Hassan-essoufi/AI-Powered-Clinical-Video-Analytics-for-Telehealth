import numpy as np
from scipy.signal import butter, filtfilt


class SignalFilter:
    """
    Filtre le signal RGB brut extrait par RPPGExtractor.
    Supprime le bruit causé par les mouvements et les changements de lumière.
    Applique un filtre passe-bande pour isoler la fréquence du pouls (0.7–4 Hz).
    """

    def __init__(self, fps: int = 30, freq_low: float = 0.7, freq_high: float = 4.0):
        """
        Args:
            fps       : frames par seconde du stream vidéo
            freq_low  : borne inférieure du filtre en Hz (pouls ~0.7Hz = 42 BPM)
            freq_high : borne supérieure du filtre en Hz (pouls ~4Hz  = 240 BPM)
        """
        self.fps       = fps
        self.freq_low  = freq_low
        self.freq_high = freq_high

    def filter(self, signal: np.ndarray) -> np.ndarray:
        """
        Applique le filtre passe-bande sur le buffer de signal RGB.

        Args:
            signal: numpy array de shape (N, 3) — N frames, canaux RGB

        Returns:
            signal filtré de même shape (N, 3)
        """
        if signal is None:
            return None

        signal = np.asarray(signal, dtype=np.float32)
        if signal.ndim != 2 or signal.shape[1] < 3 or signal.shape[0] < 10:
            return signal

        detrended = self.detrend(signal)
        # filtfilt requires enough samples for the filter order; fallback safely when too short.
        if detrended.shape[0] < 30:
            return detrended

        filtered  = self._apply_bandpass(detrended)
        return filtered

    def _apply_bandpass(self, signal: np.ndarray) -> np.ndarray:
        """
        Filtre Butterworth passe-bande sur chaque canal RGB.

        La fréquence de Nyquist est fps/2 — fréquence max détectable.
        On normalise freq_low et freq_high entre 0 et 1 par rapport à Nyquist.
        """
        nyquist = self.fps / 2
        low     = self.freq_low  / nyquist
        high    = self.freq_high / nyquist

        b, a = butter(N=4, Wn=[low, high], btype='bandpass')
        return filtfilt(b, a, signal, axis=0)

    def detrend(self, signal: np.ndarray) -> np.ndarray:
        """
        Supprime les tendances lentes du signal.
        Ex : variation progressive de la lumière dans la pièce.
        """
        from scipy.signal import detrend
        return detrend(signal, axis=0)