"""
evm_processor.py
----------------
Sprint 1 : Skeleton — Eulerian Video Magnification processor.
Sprint 2 : Will amplify micro-movements (pulse, tremors) in real-time video.
"""

import numpy as np


class EVMProcessor:
    """
    Eulerian Video Magnification (EVM).

    Amplifies micro-movements in video that are invisible to the naked eye,
    such as the patient's pulse or muscle tremors.

    The doctor can toggle "Magnify" mode to activate amplification.

    Pipeline (Sprint 2):
        1. Decompose frame into Laplacian pyramid
        2. Apply temporal bandpass filter across frame buffer
        3. Amplify target frequency band by factor alpha
        4. Reconstruct and return the magnified frame

    Target latency: < 100ms on 720p/1080p video
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
            alpha      : amplification factor (e.g. 20x for pulse visibility)
            freq_min   : lower bound of bandpass filter in Hz
            freq_max   : upper bound of bandpass filter in Hz
            fps        : frames per second of the stream
            pyr_levels : number of levels in the Laplacian pyramid
        """
        self.alpha      = alpha
        self.freq_min   = freq_min
        self.freq_max   = freq_max
        self.fps        = fps
        self.pyr_levels = pyr_levels

        self.enabled      = False   # toggled by doctor via API
        self.frame_buffer = []      # stores recent frames for temporal filtering
        self.buffer_size  = 32      # number of frames for temporal analysis

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Main method — receives a video frame, returns the (possibly) magnified frame.

        Args:
            frame: numpy array (H, W, 3) in BGR format

        Returns:
            Magnified frame if enabled, otherwise original frame unchanged.
        """
        self.frame_buffer.append(frame.copy())
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

        if not self.enabled:
            return frame  # pass-through when magnification is off

        if len(self.frame_buffer) < self.buffer_size:
            return frame  # not enough frames yet to apply temporal filter

        # Sprint 1 : placeholder — returns original frame
        # Sprint 2 : real EVM pipeline below
        magnified = self._apply_evm(frame)
        return magnified

    def _apply_evm(self, frame: np.ndarray) -> np.ndarray:
        """
        Full EVM pipeline.

        Sprint 1 : returns frame unchanged (placeholder).
        Sprint 2 : implement steps:

            Step 1 — Build Laplacian pyramid for each frame in buffer:
                pyramid = self._build_laplacian_pyramid(frame)

            Step 2 — Temporal bandpass filter across buffer at each level:
                from scipy.signal import butter, filtfilt
                b, a = butter(4, [low, high], btype='band', fs=self.fps)
                filtered = filtfilt(b, a, buffer_stack, axis=0)

            Step 3 — Amplify:
                amplified = filtered * self.alpha

            Step 4 — Reconstruct from pyramid:
                result = self._reconstruct_from_pyramid(amplified)
                return np.clip(frame + result, 0, 255).astype(np.uint8)
        """
        # TODO Sprint 2 : implement full EVM pipeline
        return frame  # placeholder

    def _build_laplacian_pyramid(self, frame: np.ndarray) -> list:
        """
        Builds a Laplacian pyramid from a single frame.

        Sprint 2 : implement with cv2.pyrDown / cv2.pyrUp
        """
        # TODO Sprint 2
        # import cv2
        # pyramid = []
        # current = frame.astype(np.float32)
        # for _ in range(self.pyr_levels):
        #     down = cv2.pyrDown(current)
        #     up   = cv2.pyrUp(down, dstsize=current.shape[1::-1])
        #     pyramid.append(current - up)
        #     current = down
        # pyramid.append(current)
        # return pyramid
        return [frame]  # placeholder

    def _reconstruct_from_pyramid(self, pyramid: list) -> np.ndarray:
        """
        Reconstructs a frame from its Laplacian pyramid.

        Sprint 2 : implement with iterative cv2.pyrUp
        """
        # TODO Sprint 2
        return pyramid[0]  # placeholder

    def enable(self):
        """Doctor activates magnification mode."""
        self.enabled = True

    def disable(self):
        """Doctor deactivates magnification mode."""
        self.enabled = False

    def set_alpha(self, alpha: float):
        """Adjust amplification factor at runtime."""
        self.alpha = alpha

    def set_frequency_range(self, freq_min: float, freq_max: float):
        """Adjust target frequency band at runtime."""
        self.freq_min = freq_min
        self.freq_max = freq_max
