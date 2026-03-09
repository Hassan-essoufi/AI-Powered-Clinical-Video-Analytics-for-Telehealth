from fastapi import APIRouter, Depends
from services.vitals_service import VitalsService

router = APIRouter(prefix="/vitals", tags=["Vitals"])

@router.get("/heartrate")
async def get_heart_rate():
    """Get estimated heart rate (BPM) from rPPG module."""
    # TODO: get frames from frame_queue.py (Person A)
    return {"bpm": None, "confidence": None, "status": "not implemented"}

@router.get("/respiration")
async def get_respiration_rate():
    """Get estimated respiration rate."""
    return {"rpm": None, "confidence": None, "status": "not implemented"}

@router.get("/all")
async def get_all_vitals():
    """Return all vital signs at once."""
    return {"bpm": None, "rpm": None, "status": "not implemented"}
