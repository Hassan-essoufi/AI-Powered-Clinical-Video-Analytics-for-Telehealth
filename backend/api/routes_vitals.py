from fastapi import APIRouter, Depends
from backend.dependencies import get_frame_queue, get_vitals_service
from backend.services.vitals_service import VitalsService

router = APIRouter(prefix="/vitals", tags=["Vitals"])

LATEST_VITALS = {
    "bpm": None,
    "rpm": None
}


@router.get("/heartrate")
async def get_heart_rate(
    frame_queue = Depends(get_frame_queue),
    vitals_service: VitalsService = Depends(get_vitals_service)
):
    try:
        frames = []

        # Get available frames from queue
        while not frame_queue.empty():
            frames.append(await frame_queue.get())

        bpm = vitals_service.estimate_heart_rate(frames)

        LATEST_VITALS["bpm"] = bpm

        return {
            "bpm": bpm,
            "status": "ok"
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("/respiration")
async def get_respiration_rate(
    frame_queue = Depends(get_frame_queue),
    vitals_service: VitalsService = Depends(get_vitals_service)
):
    try:
        frames = []

        while not frame_queue.empty():
            frames.append(await frame_queue.get())

        rpm = vitals_service.estimate_respiration(frames)

        LATEST_VITALS["rpm"] = rpm

        return {
            "rpm": rpm,
            "confidence": 0.9,
            "status": "ok"
        }

    except Exception as e:
        return {"error": str(e)}


@router.get("/all")
async def get_all_vitals(
    frame_queue = Depends(get_frame_queue),
    vitals_service: VitalsService = Depends(get_vitals_service)
):
    try:
        frames = []

        while not frame_queue.empty():
            frames.append(await frame_queue.get())

        bpm = vitals_service.estimate_heart_rate(frames)
        rpm = vitals_service.estimate_respiration(frames)

        LATEST_VITALS["bpm"] = bpm
        LATEST_VITALS["rpm"] = rpm

        return {
            "bpm": bpm,
            "rpm": rpm,
            "status": "ok"
        }

    except Exception as e:
        return {"error": str(e)}