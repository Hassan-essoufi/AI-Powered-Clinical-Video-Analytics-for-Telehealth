from fastapi import APIRouter, UploadFile, File
from services.wound_service import WoundService
import numpy as np
import cv2

router = APIRouter(prefix="/wound", tags=["Wound"])
wound_service = WoundService()

@router.post("/analyze")
async def analyze_wound(file: UploadFile = File(...)):
    """Analyze a wound from an uploaded image frame."""
    try:
        # Lire l'image uploadée
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Appeler le service
        result = wound_service.analyze(frame)
        return {"status": "ok", **result}
    except Exception as e:
        return {"status": str(e), "area_cm2": None}

@router.get("/history")
async def get_wound_history():
    """Retrieve past wound analysis results."""
    history = wound_service.get_history()
    return {"records": history, "status": "ok"}