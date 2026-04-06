import numpy as np
import cv2

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False


class WoundSegmenter:
    """
    Détecte et segmente la zone de plaie depuis une frame vidéo.

    Le médecin clique sur la plaie → cette classe produit
    un masque binaire de la zone de la plaie.

    Sprint 2 : YOLOv8-seg — rapide, compatible temps réel.
    """

    def __init__(self, model_type: str = "yolov8"):
        """
        Args:
            model_type: 'yolov8' (défaut) ou 'sam'
        """
        self.model_type = model_type
        self.model      = None

        if YOLO_AVAILABLE:
            # Téléchargement automatique du modèle au premier lancement
            self.model = YOLO("yolov8n.pt")
        else:
            print("[WoundSegmenter] ultralytics non installé — mode placeholder actif")

    def segment(self, frame: np.ndarray, click_point: tuple) -> dict:
        """
        Segmente la zone de plaie à partir du point cliqué par le médecin.

        Args:
            frame      : numpy array (H, W, 3) — frame BGR
            click_point: (x, y) coordonnées pixel du clic

        Returns:
            dict avec masque binaire et bounding box
        """
        if self.model is not None:
            mask   = self._yolo_segment(frame, click_point)
            status = "yolo_output"
        else:
            mask   = self._placeholder_mask(frame, click_point)
            status = "placeholder_output"

        return {
            "mask"       : mask,
            "bbox"       : self._get_bbox(mask),
            "click_point": click_point,
            "status"     : status
        }

    def _yolo_segment(self, frame: np.ndarray, click_point: tuple) -> np.ndarray:
        """
        Lance l'inférence YOLOv8-seg et retourne le masque
        correspondant au point cliqué par le médecin.
        """
        results = self.model(frame, verbose=False)
        cx, cy  = click_point
        h, w    = frame.shape[:2]

        if results[0].masks is None:
            # YOLO n'a rien détecté → fallback placeholder
            return self._placeholder_mask(frame, click_point)

        masks = results[0].masks.data.cpu().numpy()

        for mask in masks:
            mask_resized = cv2.resize(mask, (w, h))
            # vérifier si le point cliqué est dans ce masque
            if mask_resized[cy, cx] > 0.5:
                return (mask_resized > 0.5).astype(np.uint8)

        # aucun masque ne contient le point → fallback placeholder
        return self._placeholder_mask(frame, click_point)

    def _placeholder_mask(self, frame: np.ndarray, click_point: tuple) -> np.ndarray:
        """
        Masque carré de 50x50 pixels autour du clic.
        Utilisé quand YOLO n'est pas disponible ou ne détecte rien.
        """
        h, w   = frame.shape[:2]
        mask   = np.zeros((h, w), dtype=np.uint8)
        cx, cy = click_point
        size   = 50

        x1 = max(0, cx - size)
        x2 = min(w, cx + size)
        y1 = max(0, cy - size)
        y2 = min(h, cy + size)

        mask[y1:y2, x1:x2] = 1
        return mask

    def _get_bbox(self, mask: np.ndarray) -> tuple:
        """
        Retourne la bounding box (x1, y1, x2, y2) du masque.
        """
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)

        if not rows.any():
            return (0, 0, 0, 0)

        y1, y2 = np.where(rows)[0][[0, -1]]
        x1, x2 = np.where(cols)[0][[0, -1]]
        return (int(x1), int(y1), int(x2), int(y2))