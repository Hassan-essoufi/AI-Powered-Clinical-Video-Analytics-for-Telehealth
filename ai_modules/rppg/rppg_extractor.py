"""
rppg_extractor.py
-----------------
Sprint 1 : Skeleton — Extract raw RGB skin signals from video frames.
Sprint 2 : Will apply spatial averaging on detected face ROI.
"""

import numpy as np


class RPPGExtractor:
    """
    Extracts raw skin color signals from incoming video frames.
    These raw signals are then passed to signal_filter.py for processing.
    """

    def __init__(self, buffer_size: int = 150):
        """
        Args:
            buffer_size: Number of frames to keep in buffer (~5s at 30fps)
        """
        self.buffer_size = buffer_size
        self.frame_buffer = []       # stores raw frames
        self.signal_buffer = []      # stores extracted RGB mean signals

    def extract(self, frame: np.ndarray) -> dict:
        """
        Main method — receives a video frame and extracts
        the average RGB values from the skin region (ROI).

        Args:
            frame: numpy array of shape (H, W, 3) — BGR format from OpenCV

        Returns:
            dict with raw RGB signal values
        """
        self.frame_buffer.append(frame)

        # Keep buffer at fixed size
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

        # Sprint 1 : placeholder — average entire frame instead of face ROI
        # Sprint 2 : detect face with MediaPipe/OpenCV, extract ROI only
        raw_signal = self._extract_roi_signal(frame)
        self.signal_buffer.append(raw_signal)

        if len(self.signal_buffer) > self.buffer_size:
            self.signal_buffer.pop(0)

        return {
            "r_mean": raw_signal[0],
            "g_mean": raw_signal[1],
            "b_mean": raw_signal[2],
            "frame_count": len(self.frame_buffer),
            "status": "placeholder_output"  # Sprint 1 marker
        }

    def _extract_roi_signal(self, frame: np.ndarray) -> np.ndarray:
        """
        Extracts mean RGB values from the skin Region Of Interest.

        Sprint 1 : uses full frame average as placeholder.
        Sprint 2 : will use face detection bounding box.
        """
        # TODO Sprint 2 : replace with face ROI detection
        # roi = detect_face_roi(frame)
        # return np.mean(frame[roi], axis=(0, 1))
        return np.mean(frame, axis=(0, 1))  # placeholder

    def get_signal_buffer(self) -> np.ndarray:
        """
        Returns the accumulated signal buffer as a numpy array.
        Used by signal_filter.py for temporal filtering.
        """
        if len(self.signal_buffer) == 0:
            return np.array([])
        return np.array(self.signal_buffer)  # shape: (N, 3)
