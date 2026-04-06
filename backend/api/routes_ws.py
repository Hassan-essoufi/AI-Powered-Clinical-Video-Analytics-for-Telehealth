import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from backend.dependencies import get_evm_service
from backend.api.routes_vitals import LATEST_VITALS
from backend.api.routes_wound import LATEST_WOUND

router = APIRouter(tags=["WebSocket"])

METRICS_PUSH_INTERVAL_SECONDS = 0.2

@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """
    WebSocket endpoint for real-time vitals & wound metrics.
    Streams BPM, respiration, wound updates to frontend.
    """
    await websocket.accept()
    try:
        while True:
            if websocket.client_state != WebSocketState.CONNECTED:
                break

            evm_status = get_evm_service().status()

            try:
                await websocket.send_json({
                    "bpm": LATEST_VITALS.get("bpm"),
                    "rpm": LATEST_VITALS.get("rpm"),
                    "wound_area": LATEST_WOUND.get("area_cm2"),
                    "infection_risk": LATEST_WOUND.get("infection_risk"),
                    "wound_color": LATEST_WOUND.get("color_composition"),
                    "wound_status": LATEST_WOUND.get("status"),
                    "evm_enabled": evm_status.get("enabled"),
                    "server_time": datetime.now(timezone.utc).isoformat(),
                    "status": "ok"
                })
            except Exception as exc:
                # Browser refresh/tab close raises normal "going away" close events.
                if exc.__class__.__name__ in {"ConnectionClosedOK", "ConnectionClosedError"}:
                    break
                raise

            await asyncio.sleep(METRICS_PUSH_INTERVAL_SECONDS)
    except WebSocketDisconnect:
        return
