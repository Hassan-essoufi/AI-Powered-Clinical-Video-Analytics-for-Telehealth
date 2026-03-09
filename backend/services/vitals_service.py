class VitalsService:
    """
    Aggregates rPPG results from ai_modules/rppg/.
    Interfaces with: rppg_extractor.py, signal_filter.py, heart_rate.py (Person B)
    """

    def __init__(self):
        # TODO: import rPPG modules from Person B
        self.model = None
        self.frame_buffer = []

    def estimate_heart_rate(self, frames: list) -> float:
        """
        Process video frames → return BPM.
        Args:
            frames: list of VideoFrame from frame_queue.py
        Returns:
            float: heart rate in BPM
        """
        # TODO: call heart_rate.py from Person B
        raise NotImplementedError("Waiting for rPPG module from Person B")

    def estimate_respiration(self, frames: list) -> float:
        """
        Process video frames → return respiration rate.
        Returns:
            float: breaths per minute
        """
        # TODO: call heart_rate.py from Person B
        raise NotImplementedError("Waiting for rPPG module from Person B")

    def clear_buffer(self):
        """Reset the frame buffer."""
        self.frame_buffer = [] 
