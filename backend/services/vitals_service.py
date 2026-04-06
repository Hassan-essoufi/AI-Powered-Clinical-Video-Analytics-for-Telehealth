from backend.ai_modules.rppg import rppg_extractor, heart_rate, signal_filter
import numpy as np
from collections import deque
import time

BUFFER_SIZE = 150
DEFAULT_FPS = 30.0
MIN_FPS = 5.0
MAX_FPS = 60.0

class VitalsService:
    """
    Vitals services
    """

    def __init__(self):
        
        self.rppg_ext = rppg_extractor.RPPGExtractor()
        self.h_rate = heart_rate.HeartRateCalculator()
        self.hr_filter = signal_filter.SignalFilter(freq_low=0.7, freq_high=4.0)
        self.rr_filter = signal_filter.SignalFilter(freq_low=0.1, freq_high=0.5)
        self.model = None
        self.frame_buffer = deque(maxlen=BUFFER_SIZE)
        self.timestamp_buffer = deque(maxlen=BUFFER_SIZE)
        self.current_fps = DEFAULT_FPS

    def _append_frames_with_timestamps(self, frames: list):
        if not frames:
            return

        now = time.perf_counter()
        count = len(frames)

        if count == 1:
            self.frame_buffer.append(frames[0])
            self.timestamp_buffer.append(now)
            return

        # If many frames arrive at once, spread their timestamps with the last known FPS.
        dt = 1.0 / max(self.current_fps, MIN_FPS)
        start = now - (count - 1) * dt

        for index, frame in enumerate(frames):
            self.frame_buffer.append(frame)
            self.timestamp_buffer.append(start + index * dt)

    def _estimate_fps(self) -> float:
        if len(self.timestamp_buffer) < 2:
            return self.current_fps

        duration = self.timestamp_buffer[-1] - self.timestamp_buffer[0]
        if duration <= 0:
            return self.current_fps

        fps = (len(self.timestamp_buffer) - 1) / duration
        fps = float(np.clip(fps, MIN_FPS, MAX_FPS))
        return fps

    def _sync_processing_fps(self, fps: float):
        self.current_fps = fps
        self.h_rate.fps = fps
        self.hr_filter.fps = fps
        self.rr_filter.fps = fps

    def _build_signal(self, frames: list) -> np.ndarray:
        if not frames:
            return None

        self._append_frames_with_timestamps(frames)

        signal = []
        for frame in self.frame_buffer:
            value = self.rppg_ext.extract(frame)
            if isinstance(value, dict):
                signal.append([
                    float(value.get("r_mean", 0.0)),
                    float(value.get("g_mean", 0.0)),
                    float(value.get("b_mean", 0.0)),
                ])

        if len(signal) < 10:
            return None

        return np.asarray(signal, dtype=np.float32)

    def estimate_vitals(self, frames: list) -> dict:
        """Compute BPM and RPM from the same signal snapshot."""
        signal = self._build_signal(frames)
        if signal is None:
            return {"bpm": None, "rpm": None}

        dynamic_fps = self._estimate_fps()
        self._sync_processing_fps(dynamic_fps)

        hr_signal = self.hr_filter.filter(signal)
        rr_signal = self.rr_filter.filter(signal)

        bpm = None
        rpm = None

        if hr_signal is not None and len(hr_signal) >= 10:
            bpm = self.h_rate._compute_heart_rate(hr_signal)

        if rr_signal is not None and len(rr_signal) >= 10:
            rpm = self.h_rate._compute_respiration_rate(rr_signal)

        return {
            "bpm": bpm,
            "rpm": rpm,
        }

    def estimate_heart_rate(self, frames: list) -> float:
        """
        Process video frames → return BPM.
        Args:
            frames: list of VideoFrame from frame_queue.py
        Returns:
            float: heart rate in BPM
        """
        try:
            return self.estimate_vitals(frames).get("bpm")
        except Exception as e:
            raise Exception(f"[ERROR]: {e}")
        

    def estimate_respiration(self, frames: list) -> float:
        """
        Process video frames → return respiration rate.
        Returns:
            float: breaths per minute
        """
        try:
            return self.estimate_vitals(frames).get("rpm")
        except Exception as e :
            raise Exception(f"[ERROR]: {e}")

    def clear_buffer(self):
        """Reset the frame buffer."""
        self.frame_buffer.clear()
        self.timestamp_buffer.clear()
