"""
wound_segmenter.py
------------------
Sprint 1 : Skeleton — YOLO segmentation of wound area.
Sprint 2 : Will use YOLOv11-seg or SAM (Segment Anything Model).
"""

import numpy as np


class WoundSegmenter:
    """
    Detects and segments the wound region from a video frame.

    The doctor clicks on the wound in the video → this class
    produces a binary mask of the wound area.

    Sprint 2 options:
        - YOLOv11-seg : fast, real-time capable
        - SAM (Segment Anything Model) : more accurate, click-based
    """

    def __init__(self, model_type: str = "yolov11"):
        """
        Args:
            model_type: 'yolov11' or 'sam'
        """
        self.model_type = model_type
        self.model      = None   # loaded in Sprint 2

        # Sprint 2 : load model here
        # if model_type == "yolov11":
        #     from ultralytics import YOLO
        #     self.model = YOLO("yolov11-seg.pt")
        # elif model_type == "sam":
        #     from segment_anything import SamPredictor
        #     self.model = SamPredictor(...)

    def segment(self, frame: np.ndarray, click_point: tuple) -> dict:
        """
        Segments the wound region based on a click point from the doctor.

        Args:
            frame      : numpy array (H, W, 3) — BGR video frame
            click_point: (x, y) pixel coordinates where doctor clicked

        Returns:
            dict with binary mask and bounding box
        """
        # Sprint 1 : placeholder mask (small square around click point)
        # Sprint 2 : run YOLOv11-seg or SAM inference
        mask = self._placeholder_mask(frame, click_point)

        return {
            "mask"       : mask,              # binary numpy array (H, W)
            "bbox"       : self._get_bbox(mask),
            "click_point": click_point,
            "status"     : "placeholder_output"  # Sprint 1 marker
        }

    def _placeholder_mask(self, frame: np.ndarray, click_point: tuple) -> np.ndarray:
        """
        Creates a small square binary mask around the click point.
        Used as placeholder until real segmentation is implemented.
        """
        h, w   = frame.shape[:2]
        mask   = np.zeros((h, w), dtype=np.uint8)
        cx, cy = click_point
        size   = 50  # placeholder square of 50x50 pixels

        x1 = max(0, cx - size)
        x2 = min(w, cx + size)
        y1 = max(0, cy - size)
        y2 = min(h, cy + size)

        mask[y1:y2, x1:x2] = 1
        return mask

    def _get_bbox(self, mask: np.ndarray) -> tuple:
        """
        Returns bounding box (x1, y1, x2, y2) of the mask.
        """
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)

        if not rows.any():
            return (0, 0, 0, 0)

        y1, y2 = np.where(rows)[0][[0, -1]]
        x1, x2 = np.where(cols)[0][[0, -1]]
        return (int(x1), int(y1), int(x2), int(y2))
