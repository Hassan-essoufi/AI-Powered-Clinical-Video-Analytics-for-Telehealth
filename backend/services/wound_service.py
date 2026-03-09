class WoundService:
    """
    Handles wound metrics & prepares WebSocket data.
    Interfaces with: wound_segmenter.py, wound_measurement.py (Person B)
    """

    def __init__(self):
        # TODO: load segmentation model from Person B
        self.segmenter = None

    def analyze(self, image_frame) -> dict:
        """
        Run wound segmentation and measurement.
        Args:
            image_frame: raw image frame from video stream
        Returns:
            dict: area_cm2, infection_risk, color_composition
        """
        # TODO: call wound_segmenter.py then wound_measurement.py
        raise NotImplementedError("Waiting for wound module from Person B")

    def prepare_ws_payload(self, result: dict) -> dict:
        """Format wound result for WebSocket broadcast."""
        return {
            "wound_area_cm2": result.get("area_cm2"),
            "infection_risk": result.get("infection_risk"),
            "color": result.get("color_composition")
        }
