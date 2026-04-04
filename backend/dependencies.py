from backend.streaming.frame_queue import FrameQueue
from backend.services.vitals_service import VitalsService

frame_queue = FrameQueue(maxsize=100)
vitals_service = VitalsService()

def get_frame_queue():
    return frame_queue


def get_vitals_service():
    return vitals_service