from backend.streaming.frame_queue import FrameQueue
from backend.services.vitals_service import VitalsService
from backend.services.wound_service import WoundService
from backend.services.evm_service import EVMService

frame_queue = FrameQueue()
vitals_service = VitalsService()
wound_service = WoundService()
evm_service = EVMService()

def get_frame_queue():
    return frame_queue


def get_vitals_service():
    return vitals_service


def get_wound_service():
    return wound_service


def get_evm_service():
    return evm_service