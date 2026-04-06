import uuid
import asyncio
from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from backend.streaming.video_track import VideoTracker
from backend.streaming.frame_queue import FrameQueue
from backend.services.video_processor import VideoProcessor
from backend.dependencies import (
    get_frame_queue,
    get_vitals_service,
    get_wound_service,
    get_evm_service,
)

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
    frame_queue = get_frame_queue()
    result_queue = FrameQueue()
    tracker = VideoTracker(track=None, frame_queue=frame_queue)
    processor = VideoProcessor(
        frame_queue,
        result_queue,
        get_vitals_service(),
        get_wound_service(),
        get_evm_service(),
    )

    asyncio.create_task(processor.start())
    ACTIVE_SESSIONS[session_id] = {
        "tracker": tracker,
        "frame_queue": frame_queue,
        "result_queue": result_queue,
        "processor": processor
    }

    return {"session_id": session_id}


@router.websocket("/ws/frame-stream/{session_id}")
async def stream_frame_websocket(websocket: WebSocket, session_id: str):
    """Receive live encoded frames (jpg/png) and process each through VideoTracker."""
    await websocket.accept()

    if session_id not in ACTIVE_SESSIONS:
        await websocket.send_json({"error": "Session not found"})
        await websocket.close(code=1008)
        return

    tracker = ACTIVE_SESSIONS[session_id].get("tracker")
    if tracker is None:
        await websocket.send_json({"error": "Tracker unavailable"})
        await websocket.close(code=1011)
        return

    try:
        await websocket.send_json({"status": "ready", "session_id": session_id})

        while True:
            payload = await websocket.receive_bytes()
            ok = await tracker.process_encoded_frame(payload)

            if not ok:
                await websocket.send_json({"status": "skipped", "reason": "invalid_frame"})
    except WebSocketDisconnect:
        return


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

        
