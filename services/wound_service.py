import cv2
import numpy as np

class WoundService:
    """
    Handles wound metrics & prepares WebSocket data.
    Integrates with wound_segmenter.py and wound_measurement.py (Person B)
    """

    def __init__(self):
        self.history = []
        # TODO: self.segmenter = WoundSegmenter()  ← Person B

    def analyze(self, image_frame: np.ndarray) -> dict:
        """
        Run wound segmentation and measurement.
        Args:
            image_frame: numpy array (frame from video stream)
        Returns:
            dict: area_cm2, infection_risk, color_composition
        """
        try:
            # TODO: remplacer par le vrai modèle de Person B
            # result = self.segmenter.segment(image_frame)
            # area = wound_measurement.calculate_area(result.mask)

            # Placeholder : détection basique par couleur
            result = self._placeholder_analysis(image_frame)

            # Sauvegarder dans l'historique
            self.history.append(result)
            return result

        except Exception as e:
            return {"area_cm2": None, "infection_risk": None, "error": str(e)}

    def _placeholder_analysis(self, frame: np.ndarray) -> dict:
        """Analyse basique en attendant le modèle YOLO de Person B."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Détecter zones rouges (simulation plaie)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Calculer aire approximative
        pixel_count = cv2.countNonZero(mask)
        area_cm2 = round(pixel_count * 0.0026, 2)  # conversion approximative

        # Évaluer risque infection (basé sur intensité rouge)
        mean_val = cv2.mean(frame, mask=mask)[2]
        infection_risk = "high" if mean_val > 150 else "low"

        return {
            "area_cm2": area_cm2,
            "infection_risk": infection_risk,
            "color_composition": {"red_intensity": round(float(mean_val), 2)}
        }

    def prepare_ws_payload(self, result: dict) -> dict:
        """Format wound result for WebSocket broadcast."""
        return {
            "wound_area_cm2": result.get("area_cm2"),
            "infection_risk": result.get("infection_risk"),
            "color": result.get("color_composition")
        }

    def get_history(self) -> list:
        """Return all past analyses."""
        return self.history