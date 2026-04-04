import uuid
import asyncio
from fastapi import APIRouter, HTTPException
from backend.streaming.video_track import VideoTracker
from backend.streaming.frame_queue import FrameQueue
from backend.services.video_processor import VideoProcessor
from backend.services import vitals_service, wound_service

ACTIVE_SESSIONS = {}

router = APIRouter(prefix="/stream", tags=["Stream"])

@router.get("/status")
async def stream_status():
    """Check if the video stream endpoint is active."""
    return {"status": "stream endpoint ready"}

@router.post("/start")
async def start_stream():
    """Start a new WebRTC video stream session."""

    session_id = str(uuid.uuid4())
    frame_queue = FrameQueue()
    result_queue = FrameQueue()
    tracker = VideoTracker(track=None, frame_queue=frame_queue)
    processor = VideoProcessor(frame_queue, result_queue, vitals_service, wound_service)

    asyncio.create_task(processor.start())
    ACTIVE_SESSIONS[session_id] = {
        "tracker": tracker,
        "queue": frame_queue,
        "processor": processor
    }

    return {"session_id": session_id}


@router.post("/stop")
async def stop_stream(session_id: str):
    """Stop an active stream session."""
    
    if session_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = ACTIVE_SESSIONS[session_id]

    try:
        # Stopping processor
        processor = session.get("processor")
        if processor:
            await processor.stop()

        # Stopping tracker
        tracker = session.get("tracker")
        if tracker:
            await tracker.stop()

        session.pop("frame_queue", None)
        session.pop("result_queue", None)

        del ACTIVE_SESSIONS[session_id]
        return {
            "status": "stopped",
            "session_id": session_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
