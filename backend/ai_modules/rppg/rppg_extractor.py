import numpy as np
from collections import deque
from backend.utils.image_utils import extract_roi


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
        self.frame_buffer = deque(maxlen=buffer_size)       # stores raw frames
        self.signal_buffer = deque(maxlen=buffer_size)      # stores extracted RGB mean signals

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

        raw_signal = self._extract_roi_signal(frame)
        self.signal_buffer.append(raw_signal)

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

        """
        if frame is None or not isinstance(frame, np.ndarray) or frame.ndim != 3:
            return np.array([0.0, 0.0, 0.0], dtype=np.float32)

        roi_frame = extract_roi(frame)
        if roi_frame is None or not isinstance(roi_frame, np.ndarray) or roi_frame.size == 0:
            roi_frame = frame

        return np.mean(roi_frame, axis=(0, 1)).astype(np.float32)

    def get_signal_buffer(self) -> np.ndarray:
        """
        Returns the accumulated signal buffer as a numpy array.
        Used by signal_filter.py for temporal filtering.
        """
        if len(self.signal_buffer) == 0:
            return np.array([])
        return np.array(list(self.signal_buffer))  # shape: (N, 3)