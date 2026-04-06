from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from backend.dependencies import get_frame_queue, get_wound_service
from backend.services.wound_service import WoundService

router = APIRouter(prefix="/wound", tags=["Wound"])

WOUND_HISTORY_LIMIT = 100
WOUND_HISTORY = []
LATEST_WOUND = {
    "area_cm2": None,
    "infection_risk": None,
    "color_composition": None,
    "status": "idle"
}

def _safe_click_point(width: int, height: int, x: int = None, y: int = None):
    if x is None or y is None:
        return (width // 2, height // 2)

    cx = min(max(0, x), width - 1)
    cy = min(max(0, y), height - 1)
    return (cx, cy)

@router.post("/analyze")
async def analyze_wound(
    x: int = Query(default=None, ge=0),
    y: int = Query(default=None, ge=0),
    frame_queue = Depends(get_frame_queue),
    wound_service: WoundService = Depends(get_wound_service),
):
    """
    Analyze wound from frames currently available in the stream queue.
    Returns area in cm² and infection risk.
    """
    frames = []
    while not frame_queue.empty():
        frames.append(await frame_queue.get())

    if not frames:
        raise HTTPException(status_code=400, detail="No frames available in queue")

    frame = frames[-1]
    height, width = frame.shape[:2]
    click_point = _safe_click_point(width, height, x, y)

    try:
        result = wound_service.analyze_frames(frames, click_point=click_point)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Wound analysis failed: {exc}")

    if result is None:
        raise HTTPException(status_code=400, detail="No valid frame found for wound analysis")

    LATEST_WOUND.update(
        {
            "area_cm2": result.get("area_cm2"),
            "infection_risk": result.get("infection_risk"),
            "color_composition": result.get("color_composition"),
            "status": result.get("status")
        }
    )

    history_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "queue",
        "frames_consumed": len(frames),
        "result": result
    }
    WOUND_HISTORY.append(history_entry)

    if len(WOUND_HISTORY) > WOUND_HISTORY_LIMIT:
        del WOUND_HISTORY[0 : len(WOUND_HISTORY) - WOUND_HISTORY_LIMIT]

    return {
        "status": "ok",
        "result": result
    }

@router.get("/history")
async def get_wound_history(limit: int = Query(default=20, ge=1, le=WOUND_HISTORY_LIMIT)):
    """Retrieve past wound analysis results."""
    records = WOUND_HISTORY[-limit:]
    return {
        "status": "ok",
        "count": len(records),
        "records": records
    }
