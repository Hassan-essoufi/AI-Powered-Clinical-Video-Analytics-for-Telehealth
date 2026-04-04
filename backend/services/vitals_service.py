from backend.ai_modules.rppg import rppg_extractor, heart_rate, signal_filter

BUFFER_SIZE = 150

class VitalsService:
    """
    Vitals services
    """

    def __init__(self):
        
        self.rppg_ext = rppg_extractor.RPPGExtractor()
        self.h_rate = heart_rate.HeartRateCalculator()
        self.s_filter = signal_filter.SignalFilter()
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
        try:
            if not frames:
                return None
            
            self.frame_buffer.extend(frames)
            self.frame_buffer = self.frame_buffer[-BUFFER_SIZE:]
            
            signal =[]
            for frame in self.frame_buffer:
                value = self.rppg_ext.extract(frame)
                signal.append(value)
            if not signal:
                return None
            filtered_signal = self.s_filter.filter(signal)

            # Computing BPM
            bpm = self.h_rate._compute_heart_rate(filtered_signal)

            return bpm
        except Exception as e:
            raise Exception(f"[ERROR]: {e}")
        

    def estimate_respiration(self, frames: list) -> float:
        """
        Process video frames → return respiration rate.
        Returns:
            float: breaths per minute
        """
        try:
            if not frames:
                return None
            
            self.frame_buffer.extend(frames)
            self.frame_buffer = self.frame_buffer[-BUFFER_SIZE:]

            signal = []
            for frame in self.frame_buffer:
                value = self.rppg_ext.extract(frame)
                signal.append(value)
            
            if not signal:
                return None
            
            filtered_signal = self.s_filter.filter(signal)
            
            # Computing respiration rate
            respiration_rate = self.h_rate._compute_respiration_rate(filtered_signal)
            
            return respiration_rate
        except Exception as e :
            raise Exception(f"[ERROR]: {e}")

    def clear_buffer(self):
        """Reset the frame buffer."""
        self.frame_buffer = [] 
