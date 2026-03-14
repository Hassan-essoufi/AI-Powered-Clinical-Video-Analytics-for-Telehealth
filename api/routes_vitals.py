from fastapi import APIRouter
from services.vitals_service import VitalsService

router = APIRouter(prefix="/vitals", tags=["Vitals"])
vitals_service = VitalsService()

@router.get("/heartrate")
async def get_heart_rate():
    """Get estimated heart rate (BPM) from rPPG module."""
    try:
        result = vitals_service.get_latest_vitals()
        return {"bpm": result["bpm"], "status": "ok"}
    except Exception as e:
        return {"bpm": None, "status": str(e)}

@router.get("/respiration")
async def get_respiration_rate():
    """Get estimated respiration rate."""
    try:
        result = vitals_service.get_latest_vitals()
        return {"rpm": result["rpm"], "status": "ok"}
    except Exception as e:
        return {"rpm": None, "status": str(e)}

@router.get("/all")
async def get_all_vitals():
    """Return all vital signs at once."""
    try:
        result = vitals_service.get_latest_vitals()
        return {"bpm": result["bpm"], "rpm": result["rpm"], "status": "ok"}
    except Exception as e:
        return {"bpm": None, "rpm": None, "status": str(e)}