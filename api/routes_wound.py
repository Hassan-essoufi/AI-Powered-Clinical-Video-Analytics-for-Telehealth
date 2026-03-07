from fastapi import APIRouter, UploadFile, File
from services.wound_service import WoundService

router = APIRouter(prefix="/wound", tags=["Wound"])
wound_service = WoundService()

@router.post("/analyze")
async def analyze_wound(file: UploadFile = File(...)):
    """
    Analyze a wound from a video frame.
    Returns area in cm² and infection risk.
    """
    # TODO: connect to wound_segmenter.py (Person B)
    return {
        "area_cm2": None,
        "infection_risk": None,
        "color_composition": None,
        "status": "not implemented"
    }

@router.get("/history")
async def get_wound_history():
    """Retrieve past wound analysis results."""
    return {"records": [], "status": "not implemented"}
