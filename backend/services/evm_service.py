from backend.ai_modules.evm.evm_processor import EVMProcessor


class EVMService:
    """High-level wrapper around the EVM processor used by the API."""

    def __init__(self):
        self.processor = EVMProcessor()

    def status(self) -> dict:
        return {
            "enabled": self.processor.enabled,
            "alpha": self.processor.alpha,
            "freq_min": self.processor.freq_min,
            "freq_max": self.processor.freq_max,
            "fps": self.processor.fps,
            "pyr_levels": self.processor.pyr_levels,
            "buffer_size": self.processor.buffer_size,
            "buffer_length": len(self.processor.frame_buffer),
        }

    def enable(self) -> dict:
        self.processor.enable()
        return self.status()

    def disable(self) -> dict:
        self.processor.disable()
        return self.status()

    def update_config(
        self,
        alpha: float = None,
        freq_min: float = None,
        freq_max: float = None,
        fps: int = None,
        pyr_levels: int = None,
    ) -> dict:
        if alpha is not None:
            self.processor.set_alpha(alpha)

        if freq_min is not None or freq_max is not None:
            new_min = self.processor.freq_min if freq_min is None else freq_min
            new_max = self.processor.freq_max if freq_max is None else freq_max

            if new_min >= new_max:
                raise ValueError("freq_min must be lower than freq_max")

            self.processor.set_frequency_range(new_min, new_max)

        if fps is not None:
            self.processor.fps = fps

        if pyr_levels is not None:
            self.processor.pyr_levels = pyr_levels

        return self.status()

    def process_frame(self, frame):
        return self.processor.process_frame(frame)
