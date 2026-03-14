class VitalsService:
    def __init__(self):
        self.latest = {"bpm": 0.0, "rpm": 0.0}
        self.frame_buffer = []

    def get_latest_vitals(self) -> dict:
        """Return the last computed vitals."""
        return self.latest

    def update_vitals(self, bpm: float, rpm: float):
        """Called by video_processor after rPPG computation."""
        self.latest = {"bpm": round(bpm, 1), "rpm": round(rpm, 1)}

    def estimate_heart_rate(self, frames: list) -> float:
        # TODO: appeler heart_rate.py de Person B
        raise NotImplementedError("Waiting for rPPG module from Person B")

    def estimate_respiration(self, frames: list) -> float:
        # TODO: appeler heart_rate.py de Person B
        raise NotImplementedError("Waiting for rPPG module from Person B")

    def clear_buffer(self):
        self.frame_buffer = []