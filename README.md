# AI-Powered Clinical Video Analytics for Telehealth

A real-time telehealth analytics platform that streams live camera frames to a FastAPI backend, runs AI processing (rPPG, wound analysis, optional EVM), and pushes clinical metrics back to the UI with low latency.

## Executive Summary

This project delivers a backend-centric clinical video pipeline with:
- Live frame ingestion via WebSocket
- Heart rate and respiration estimation from rPPG signals
- Wound segmentation and measurement (area, color profile, infection-risk heuristic)
- Runtime EVM control (enable/disable/config)
- Continuous metrics push via `/ws/metrics`

The architecture is modular, asynchronous, and designed for iterative research and production hardening.

## Core Objectives

- Support remote patient monitoring from standard camera feeds
- Reduce manual clinical measurements through AI-assisted analysis
- Provide a clear API surface for dashboard integration
- Keep end-to-end latency compatible with real-time monitoring

## End-to-End Data Flow

```mermaid
flowchart LR
  FE[Frontend Dashboard\nReact + TypeScript] -->|POST /stream/start| API[FastAPI Routers]
  FE -->|POST /stream/stop| API
  FE -->|POST /evm/enable or /evm/disable| API

  FE -->|WS /stream/ws/frame-stream/{session_id}\nJPEG binary frames| Q[Async Frame Queue]
  Q --> VP[VideoProcessor]

  VP --> VS[VitalsService\nrPPG + filtering + FFT]
  VP --> WSVC[WoundService\nsegmentation + measurement]
  VP --> ES[EVMService\noptional enhancement]

  VS --> LV[LATEST_VITALS]
  WSVC --> LW[LATEST_WOUND]
  ES --> LE[EVM status]

  LV --> MET[WS /ws/metrics publisher]
  LW --> MET
  LE --> MET

  MET -->|JSON metrics every 0.2s| FE
```

## Architecture Overview

### Backend Layer

- FastAPI app entry in `backend/main.py`
- Routers:
  - `backend/api/routes_stream.py`
  - `backend/api/routes_vitals.py`
  - `backend/api/routes_wound.py`
  - `backend/api/routes_ws.py`
  - `backend/api/routes_evm.py`
- Shared service instances in `backend/dependencies.py`

### Processing Layer

- `backend/services/video_processor.py`
  - Consumes queued frames
  - Optionally applies EVM
  - Runs vitals + wound analysis concurrently
  - Updates `LATEST_VITALS` and `LATEST_WOUND`

- `backend/services/vitals_service.py`
  - Builds RGB temporal signal
  - Applies HR and RR filters
  - Computes BPM/RPM from FFT
  - Dynamically adapts to observed FPS

- `backend/services/wound_service.py`
  - Frame preparation (dtype/range/color conversion)
  - Segmentation + measurement orchestration

- `backend/services/evm_service.py`
  - EVM runtime control and frame processing facade

### AI Modules

- rPPG:
  - `backend/ai_modules/rppg/rppg_extractor.py`
  - `backend/ai_modules/rppg/signal_filter.py`
  - `backend/ai_modules/rppg/heart_rate.py`

- Wound:
  - `backend/ai_modules/wound/wound_segmenter.py`
  - `backend/ai_modules/wound/wound_measurement.py`

- EVM:
  - `backend/ai_modules/evm/evm_processor.py`

### Streaming Utilities

- `backend/streaming/frame_queue.py`
- `backend/streaming/video_track.py`
- `backend/utils/image_utils.py`

## API Reference

### Stream API

- `POST /stream/start`
  - Starts a stream session
  - Response includes `session_id`

- `POST /stream/stop?session_id=<id>`
  - Stops the stream session

- `GET /stream/status`
  - Stream route readiness/status

- `WS /stream/ws/frame-stream/{session_id}`
  - Live binary frame ingestion (JPEG bytes)

### Vitals API

- `GET /vitals/heartrate`
- `GET /vitals/respiration`
- `GET /vitals/all`

### Wound API

- `POST /wound/analyze`
- `GET /wound/history`

### EVM API

- `GET /evm/status`
- `POST /evm/enable`
- `POST /evm/disable`
- `PATCH /evm/config`

### Metrics WebSocket

- `WS /ws/metrics`
  - Pushes aggregated live metrics at ~5 Hz

## Live Metrics Payload (Typical)

```json
{
  "bpm": 72.4,
  "rpm": 16.1,
  "wound_area": 0.0,
  "infection_risk": "low",
  "wound_color": {
    "r_mean": 125.1,
    "g_mean": 92.7,
    "b_mean": 88.3
  },
  "wound_status": "live",
  "evm_enabled": true,
  "server_time": "2026-04-06T12:00:00+00:00",
  "status": "ok"
}
```

## Frontend Integration Notes

Frontend app lives in `frontend/src/app/App.tsx` and related components/hooks.

Current integration points:
- Session control via `/stream/start` and `/stream/stop`
- Frame push via `WS /stream/ws/frame-stream/{session_id}`
- Metrics subscription via `WS /ws/metrics`
- EVM toggle via `/evm/enable` and `/evm/disable`

The dashboard displays:
- Session and stream status
- BPM/RPM KPI
- Wound analysis cards
- Live payload viewer and activity log

## Configuration

Key runtime constants in `backend/config.py`:
- `VIDEO_WIDTH`
- `VIDEO_HEIGHT`
- `FRAME_RATE`
- `QUEUE_MAXSIZE`

Vitals and filtering behavior can also be tuned in:
- `backend/services/vitals_service.py`
- `backend/ai_modules/rppg/signal_filter.py`
- `backend/ai_modules/rppg/heart_rate.py`

## Setup and Run

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Backend root check:
- `GET /` -> `{"message": "backend running"}`

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

For production-like serving:

```powershell
cd frontend
npm run build
```



## Current Strengths

- Clear modular backend boundaries (`api`, `services`, `ai_modules`)
- Real-time streaming architecture with async queue and WebSocket push
- Runtime EVM controls without restart
- FPS-adaptive vitals pipeline to reduce fixed-FPS drift

## Known Limitations

- RPM remains sensitive to motion, lighting, and short signal windows
- Wound area in `cm2` requires calibration to be clinically meaningful
- Open CORS policy is permissive for development and should be restricted in production
- Session lifecycle cleanup can be hardened further for long-running deployments


## Repository Map

```text
backend/
  api/
  ai_modules/
  services/
  streaming/
  utils/
frontend/
  src/
tests/
requirements.txt
```

## Disclaimer

This repository is a research/prototyping codebase and is not a certified medical device. It must not be used as the sole basis for diagnosis or treatment decisions.
