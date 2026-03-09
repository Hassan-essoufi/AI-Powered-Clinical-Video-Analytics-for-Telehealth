from fastapi import APIRouter

router = APIRouter(prefix="/stream", tags=["Stream"])

@router.get("/status")
async def stream_status():
    """Check if the video stream endpoint is active."""
    return {"status": "stream endpoint ready"}

@router.post("/start")
async def start_stream():
    """Start a new WebRTC video stream session."""
    # TODO: initialize WebRTC session with video_track.py (Person A)
    return {"session_id": None, "status": "not implemented"}

@router.post("/stop")
async def stop_stream():
    """Stop an active stream session."""
    # TODO: close WebRTC session
    return {"status": "not implemented"}
