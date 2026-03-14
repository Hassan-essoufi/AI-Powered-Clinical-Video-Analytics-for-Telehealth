from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """
    WebSocket endpoint for real-time vitals & wound metrics.
    Streams BPM, respiration, wound updates to frontend.
    """
    await websocket.accept()
    try:
        while True:
            # TODO: push real data from vitals_service & wound_service
            await websocket.send_json({
                "bpm": None,
                "rpm": None,
                "wound_area": None,
                "status": "waiting for AI modules"
            })
    except WebSocketDisconnect:
        print("Client disconnected") 