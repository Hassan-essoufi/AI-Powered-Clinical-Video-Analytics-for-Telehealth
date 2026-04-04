from backend.ai_modules.wound import wound_measurement as wm , wound_segmenter as ws

class WoundService:
    """
    Handles wound metrics & prepares WebSocket data.
    Interfaces with: wound_segmenter.py, wound_measurement.py (Person B)
    """

    def __init__(self):
        self.segmenter = ws.WoundSegmenter()

    def analyze(self, frame) -> dict:
        """
        Run wound segmentation and measurement.
        Args:
            frame: raw image frame from video stream
        Returns:
            dict: area_cm2, infection_risk, color_composition
        """
        if frame is None:
            return None
        
        segmented_mask = self.segmenter.segment(frame)
        metrics = wm.WoundMeasurement.measure(frame, segmented_mask)

        return metrics
        

    def prepare_ws_payload(self, result: dict) -> dict:
        """Format wound result for WebSocket broadcast."""
        return {
            "wound_area_cm2": result.get("area_cm2"),
            "infection_risk": result.get("infection_risk"),
            "color": result.get("color_composition")
        }
