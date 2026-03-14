"""
heart_rate.py
-------------
Sprint 1 : Skeleton — placeholders 72 BPM et 16 breaths/min.
Sprint 2 : Vrai calcul via FFT sur le canal vert du signal filtré.
"""

import numpy as np


class HeartRateCalculator:
    """
    Prend le signal rPPG filtré et calcule :
    - Fréquence cardiaque en BPM (battements par minute)
    - Fréquence respiratoire en respirations/min

    Méthode : FFT (Fast Fourier Transform) sur le canal vert
    qui porte le signal de pouls le plus fort.
    """

    def __init__(self, fps: int = 30):
        """
        Args:
            fps: frames par seconde — nécessaire pour convertir la fréquence FFT en BPM
        """
        self.fps = fps

        # Plages de fréquences
        self.hr_freq_low  = 0.7   # Hz → 42 BPM
        self.hr_freq_high = 4.0   # Hz → 240 BPM
        self.rr_freq_low  = 0.1   # Hz → 6 respirations/min
        self.rr_freq_high = 0.5   # Hz → 30 respirations/min

    def calculate(self, filtered_signal: np.ndarray) -> dict:
        """
        Méthode principale — calcule la fréquence cardiaque et respiratoire.

        Args:
            filtered_signal: numpy array (N, 3) depuis SignalFilter

        Returns:
            dict avec BPM, fréquence respiratoire et qualité du signal
        """
        if filtered_signal is None or len(filtered_signal) < 30:
            return self._insufficient_output("not_enough_data")

        heart_rate_bpm   = self._compute_heart_rate(filtered_signal)
        respiration_rate = self._compute_respiration_rate(filtered_signal)
        signal_quality   = self._assess_quality(filtered_signal)

        return {
            "heart_rate_bpm"  : heart_rate_bpm,
            "respiration_rate": respiration_rate,
            "signal_quality"  : signal_quality,
            "status"          : "live"
        }

    def _compute_heart_rate(self, signal: np.ndarray) -> float:
        """
        FFT sur le canal vert pour trouver la fréquence dominante du pouls.

        Étapes :
        1. Extraire le canal vert (le plus sensible au pouls)
        2. Calculer la FFT → obtenir les fréquences et leurs puissances
        3. Masquer uniquement la plage du pouls (0.7 – 4 Hz)
        4. Trouver le pic dominant → convertir en BPM
        """
        green = signal[:, 1]                                          # canal vert
        freqs = np.fft.rfftfreq(len(green), d=1/self.fps)            # fréquences en Hz
        power = np.abs(np.fft.rfft(green))                           # puissance de chaque fréquence

        # garder uniquement la plage du pouls
        mask  = (freqs >= self.hr_freq_low) & (freqs <= self.hr_freq_high)

        if not mask.any():
            return 0.0

        peak_freq = freqs[mask][np.argmax(power[mask])]              # fréquence dominante
        return round(peak_freq * 60, 1)                              # Hz → BPM

    def _compute_respiration_rate(self, signal: np.ndarray) -> float:
        """
        FFT sur le canal vert pour trouver la fréquence respiratoire.
        Même logique que heart rate mais sur une plage plus basse (0.1 – 0.5 Hz).
        """
        green = signal[:, 1]
        freqs = np.fft.rfftfreq(len(green), d=1/self.fps)
        power = np.abs(np.fft.rfft(green))

        mask  = (freqs >= self.rr_freq_low) & (freqs <= self.rr_freq_high)

        if not mask.any():
            return 0.0

        peak_freq = freqs[mask][np.argmax(power[mask])]
        return round(peak_freq * 60, 1)                              # Hz → respirations/min

    def _assess_quality(self, signal: np.ndarray) -> str:
        """
        Évalue la qualité du signal via le rapport signal/bruit (SNR).
        Un signal bruité (mouvement du patient) donnera une mauvaise qualité.
        """
        green     = signal[:, 1]
        freqs     = np.fft.rfftfreq(len(green), d=1/self.fps)
        power     = np.abs(np.fft.rfft(green))

        # puissance dans la plage du pouls vs puissance totale
        mask      = (freqs >= self.hr_freq_low) & (freqs <= self.hr_freq_high)
        signal_p  = np.sum(power[mask])
        total_p   = np.sum(power)

        if total_p == 0:
            return "insufficient_data"

        snr = signal_p / total_p

        if snr > 0.6:
            return "good"
        elif snr > 0.3:
            return "medium"
        else:
            return "poor"

    def _insufficient_output(self, reason: str) -> dict:
        return {
            "heart_rate_bpm"  : 0.0,
            "respiration_rate": 0.0,
            "signal_quality"  : "insufficient_data",
            "status"          : reason
        }
