from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api.routes_stream import router as stream_router
from backend.api.routes_vitals import router as vitals_router
from backend.api.routes_wound import router as wound_router
from backend.api.routes_ws import router as ws_router
from backend.api.routes_evm import router as evm_router

app = FastAPI(title='Biostream IA backend ')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'message': 'backend running'}

app.include_router(stream_router)
app.include_router(vitals_router)
app.include_router(wound_router)
app.include_router(ws_router)
app.include_router(evm_router)

frontend_dist_dir = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dist_dir), html=True), name="frontend")

