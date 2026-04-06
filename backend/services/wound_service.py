from backend.ai_modules.wound import wound_measurement as wm , wound_segmenter as ws
import cv2
import numpy as np

class WoundService:
    """
    Handles wound metrics & prepares WebSocket data.
    Interfaces with: wound_segmenter.py, wound_measurement.py (Person B)
    """

    def __init__(self):
        self.segmenter = ws.WoundSegmenter()
        self.measurement = wm.WoundMeasurement()

    def _prepare_frame(self, frame):
        if frame is None:
            return None

        frame_array = np.asarray(frame)
        if frame_array.ndim != 3 or frame_array.shape[2] != 3:
            return None

        if frame_array.dtype.kind == "f":
            frame_array = np.clip(frame_array * 255.0, 0, 255).astype(np.uint8)
        else:
            frame_array = np.clip(frame_array, 0, 255).astype(np.uint8)

        # Queue frames are RGB; wound modules expect BGR.
        return cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)

    def analyze(self, frame, click_point: tuple = None) -> dict:
        """
        Run wound segmentation and measurement.
        Args:
            frame: raw image frame from video stream
        Returns:
            dict: area_cm2, infection_risk, color_composition
        """
        prepared_frame = self._prepare_frame(frame)
        if prepared_frame is None:
            return None
        
        height, width = prepared_frame.shape[:2]
        if click_point is None:
            click_point = (width // 2, height // 2)

        segmented_output = self.segmenter.segment(prepared_frame, click_point)
        segmented_mask = segmented_output.get("mask")
        metrics = self.measurement.measure(prepared_frame, segmented_mask)

        metrics["bbox"] = segmented_output.get("bbox")
        metrics["click_point"] = segmented_output.get("click_point")
        metrics["segmentation_status"] = segmented_output.get("status")

        return metrics

    def analyze_frames(self, frames: list, click_point: tuple = None) -> dict:
        """Analyze the latest valid frame from a frame queue batch."""
        if not frames:
            return None

        for frame in reversed(frames):
            result = self.analyze(frame, click_point=click_point)
            if result is not None:
                return result

        return None
        

    def prepare_ws_payload(self, result: dict) -> dict:
        """Format wound result for WebSocket broadcast."""
        return {
            "wound_area_cm2": result.get("area_cm2"),
            "infection_risk": result.get("infection_risk"),
            "color": result.get("color_composition")
        }
