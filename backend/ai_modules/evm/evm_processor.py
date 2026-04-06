import numpy as np
import cv2
from scipy.signal import butter, filtfilt
from collections import deque


class EVMProcessor:
    """
    Eulerian Video Magnification (EVM).

    Amplifie les micro-mouvements dans la vidéo invisibles à l'œil nu,
    comme le pouls ou les tremblements musculaires du patient.

    Le médecin peut activer/désactiver le mode "Magnify" via l'API.

    Pipeline complet (Sprint 2) :
        1. Décomposer chaque frame en pyramide Laplacienne
        2. Appliquer un filtre passe-bande temporel sur le buffer de frames
        3. Amplifier la bande de fréquences cible par le facteur alpha
        4. Reconstruire et retourner la frame amplifiée

    Latence cible : < 100ms sur vidéo 720p/1080p
    """

    def __init__(
        self,
        alpha     : float = 20.0,
        freq_min  : float = 0.4,
        freq_max  : float = 3.0,
        fps       : int   = 30,
        pyr_levels: int   = 4
    ):
        """
        Args:
            alpha      : facteur d'amplification (ex: 20x pour le pouls)
            freq_min   : borne inférieure du filtre en Hz
            freq_max   : borne supérieure du filtre en Hz
            fps        : frames par seconde du stream
            pyr_levels : nombre de niveaux dans la pyramide Laplacienne
        """
        self.alpha      = alpha
        self.freq_min   = freq_min
        self.freq_max   = freq_max
        self.fps        = fps
        self.pyr_levels = pyr_levels

        self.enabled      = False
        self.buffer_size  = 32
        self.frame_buffer = deque(maxlen=self.buffer_size)

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Méthode principale — reçoit une frame, retourne la frame (amplifiée ou non).

        Args:
            frame: numpy array (H, W, 3) en format BGR

        Returns:
            Frame amplifiée si activé, sinon frame originale.
        """
        self.frame_buffer.append(frame.copy())

        if not self.enabled:
            return frame

        if len(self.frame_buffer) < self.buffer_size:
            return frame  # pas assez de frames pour filtrer

        return self._apply_evm(frame)

    def _apply_evm(self, frame: np.ndarray) -> np.ndarray:
        """
        Pipeline EVM complet :
        1. Construire pyramide Laplacienne pour chaque frame du buffer
        2. Filtrer temporellement à chaque niveau de la pyramide
        3. Amplifier
        4. Reconstruire la frame finale
        """
        # Étape 1 : pyramide pour chaque frame du buffer
        buffer_pyramids = [
            self._build_laplacian_pyramid(f) for f in self.frame_buffer
        ]

        # Étape 2 : filtre temporel sur chaque niveau
        filtered_pyramid = self._temporal_filter(buffer_pyramids)

        # Étape 3 : amplifier chaque niveau
        amplified = [level * self.alpha for level in filtered_pyramid]

        # Étape 4 : reconstruire à partir de la dernière frame amplifiée
        last_frame_pyramid = [amplified[l][-1] for l in range(self.pyr_levels)]
        last_frame_pyramid.append(
            buffer_pyramids[-1][self.pyr_levels].astype(np.float32)
        )
        result = self._reconstruct_from_pyramid(last_frame_pyramid)

        # Étape 5 : ajouter à la frame originale et clipper entre 0 et 255
        output = frame.astype(np.float32) + result
        return np.clip(output, 0, 255).astype(np.uint8)

    def _build_laplacian_pyramid(self, frame: np.ndarray) -> list:
        """
        Construit une pyramide Laplacienne depuis une frame.

        Chaque niveau = différence entre la frame et sa version floutée/réduite.
        → Capture les détails à différentes échelles spatiales.
        """
        pyramid = []
        current = frame.astype(np.float32)

        for _ in range(self.pyr_levels):
            down = cv2.pyrDown(current)
            up   = cv2.pyrUp(down, dstsize=(current.shape[1], current.shape[0]))
            pyramid.append(current - up)   # détails de ce niveau
            current = down

        pyramid.append(current)            # dernière couche (image réduite)
        return pyramid

    def _temporal_filter(self, buffer_pyramids: list) -> list:
        """
        Applique un filtre passe-bande temporel sur chaque niveau de la pyramide.

        Pour chaque niveau, on empile toutes les frames du buffer → on filtre
        dans le temps pour garder uniquement les oscillations à freq_min–freq_max Hz.
        """
        nyquist = self.fps / 2
        low     = self.freq_min / nyquist
        high    = self.freq_max / nyquist
        b, a    = butter(1, [low, high], btype='bandpass')

        filtered_pyramid = []
        for level in range(self.pyr_levels):
            # stack toutes les frames pour ce niveau → shape: (N, H, W, 3)
            stack    = np.array([
                buffer_pyramids[i][level] for i in range(len(buffer_pyramids))
            ])
            filtered = filtfilt(b, a, stack, axis=0)
            filtered_pyramid.append(filtered)

        return filtered_pyramid

    def _reconstruct_from_pyramid(self, pyramid: list) -> np.ndarray:
        """
        Reconstruit une frame depuis sa pyramide Laplacienne.
        Remonte les niveaux en appliquant pyrUp à chaque fois.
        """
        current = pyramid[-1]

        for i in range(len(pyramid) - 2, -1, -1):
            current = cv2.pyrUp(
                current,
                dstsize=(pyramid[i].shape[1], pyramid[i].shape[0])
            )
            current = current + pyramid[i]

        return current

    def enable(self):
        """Le médecin active le mode magnification."""
        self.enabled = True

    def disable(self):
        """Le médecin désactive le mode magnification."""
        self.enabled = False

    def set_alpha(self, alpha: float):
        """Ajuster le facteur d'amplification en temps réel."""
        self.alpha = alpha

    def set_frequency_range(self, freq_min: float, freq_max: float):
        """Ajuster la plage de fréquences cible en temps réel."""
        self.freq_min = freq_min
        self.freq_max = freq_max