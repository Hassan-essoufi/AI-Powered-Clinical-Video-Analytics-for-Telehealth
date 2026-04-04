# AI-Powered Clinical Video Analytics for Telehealth

## Overview
This project is a telehealth backend prototype that analyzes live clinical video streams to extract useful bedside indicators for remote care.

The system is designed around three AI capabilities:
- Remote vital-sign estimation from facial video (rPPG)
- Eulerian Video Magnification (EVM) for subtle pulse and micro-motion visualization
- Wound segmentation and measurement from video/image frames

The implementation currently focuses on the Python backend processing pipeline, with frontend files scaffolded for future integration.

## Project Goals
- Support remote patient monitoring through camera-based analysis
- Reduce manual workload for clinicians by automating measurements
- Provide a modular architecture that can evolve into real-time production workflows

## Core Functionalities

### 1. Streaming and Frame Processing
- Creates a stream session and allocates asynchronous frame queues
- Receives video frames through a custom video track wrapper
- Applies preprocessing (ROI extraction, color conversion, resize, normalization)
- Dispatches frames to analysis services in parallel

Current status: partially implemented in backend services.

### 2. Vital Signs Estimation (rPPG)
- Extracts raw RGB signals from a facial region of interest
- Applies detrending and Butterworth bandpass filtering
- Computes:
	- Heart rate (BPM)
	- Respiration rate (breaths/min)
- Estimates signal quality from frequency-domain energy ratio

Current status: implemented at algorithm/service level; route integration is placeholder.

### 3. Eulerian Video Magnification (EVM)
- Maintains a temporal frame buffer
- Builds Laplacian pyramids
- Applies temporal bandpass filtering to amplify subtle physiological motion
- Reconstructs amplified output frame
- Allows dynamic enable/disable and runtime parameter tuning

Current status: implemented as a standalone module and ready for pipeline/API wiring.

### 4. Wound Segmentation and Measurement
- Attempts wound segmentation with Ultralytics YOLO segmentation model
- Falls back to a placeholder click-centered mask when detection is unavailable
- Computes:
	- Pixel area
	- Area in cm^2 (when calibrated)
	- RGB color composition
	- Infection risk heuristic

Current status: core logic exists; API endpoint currently returns placeholder response.

### 5. Real-Time Metrics Transport
- Includes a WebSocket endpoint scaffold for live metrics streaming
- Intended payload: heart rate, respiration, wound measurements

Current status: endpoint exists and sends placeholder values.

## High-Level Architecture
1. Browser captures camera stream.
2. Stream is sent to backend.
3. Video frames are queued asynchronously.
4. AI modules process frames in parallel.
5. Results are exposed via REST and WebSocket APIs.
6. Frontend dashboard displays live analytics.

## Repository Structure
```
backend/
	main.py                      # FastAPI app entry
	config.py                    # Global video/queue settings
	dependencies.py              # Shared dependency container (currently empty)
	api/
		routes_stream.py           # Stream session endpoints
		routes_vitals.py           # Vitals endpoints (placeholder responses)
		routes_wound.py            # Wound endpoints (placeholder responses)
		routes_ws.py               # WebSocket metrics endpoint (placeholder payload)
	streaming/
		video_track.py             # Frame capture + preprocessing
		frame_queue.py             # Async queue with drop counter
	services/
		video_processor.py         # Frame consumer, parallel service invocation
		vitals_service.py          # rPPG-based vitals extraction service
		wound_service.py           # Wound segmentation/measurement service adapter
	ai_modules/
		rppg/
			rppg_extractor.py
			signal_filter.py
			heart_rate.py
		evm/
			evm_processor.py
		wound/
			wound_segmenter.py
			wound_measurement.py
	utils/
		image_utils.py             # ROI extraction and image preprocessing helpers
		logger.py                  # Logger factory

frontend/
	index.html                   # UI scaffold (currently empty)
	app.js                       # Frontend logic scaffold (currently empty)
	webrtc_client.js             # WebRTC client scaffold (currently empty)
	style.css                    # UI styles scaffold (currently empty)

tests/
	test_queue.py                # Async queue test script
```

## Tech Stack
- Python 3.10+
- FastAPI
- asyncio
- aiortc (used by streaming track abstraction)
- OpenCV, NumPy, SciPy
- PyTorch ecosystem (torch, torchvision, torchaudio)
- Ultralytics (YOLO segmentation)
- WebSockets

## Installation

### 1. Clone and enter project
```powershell
git clone <your-repository-url>
cd AI-Powered_Clinical_Video_Analytics_for_Telehealth
```

### 2. Create and activate virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Backend
```powershell
uvicorn backend.main:app --reload
```

Default root endpoint:
- GET /
- Response: {"message": "backend running"}

## API Endpoints (Current Code)

### Stream Routes
- GET /stream/status
- POST /stream/start
- POST /stream/stop?session_id=<id>

### Vitals Routes
- GET /vitals/heartrate
- GET /vitals/respiration
- GET /vitals/all

### Wound Routes
- POST /wound/analyze
- GET /wound/history

### WebSocket
- WS /ws/metrics

Note: Route files are present, but router inclusion in the FastAPI app must be completed in main.py for all endpoints to be active.

## Testing
Run the queue test script:
```powershell
python tests/test_queue.py
```

This validates asynchronous enqueue/dequeue behavior with a synthetic frame.

## Current Implementation Status

Implemented:
- Frame queueing and frame preprocessing
- rPPG extraction/filtering/FFT-based calculations
- EVM processing class
- Wound segmentation and measurement logic
- Stream session start/stop scaffolding

In progress / to complete:
- Register all API routers in backend.main
- Fix service wiring and import consistency across routes/services
- Connect live frame flow to vitals and wound endpoints
- Broadcast real metrics over WebSocket
- Build frontend dashboard UI and WebRTC signaling workflow
- Add robust unit and integration tests

## Known Technical Notes
- Some modules contain placeholder markers and TODOs.
- Several route handlers currently return "not implemented" payloads.
- frontend/ files are currently empty scaffolds.
- dependencies.py is currently empty.
- A referenced utility file (math_utils.py) is not present in the current tree.

## Future Roadmap
- Full WebRTC ingest and browser dashboard
- Session persistence and patient history storage
- Clinical calibration workflow for wound cm^2 measurement
- Confidence scoring and trend visualization
- Containerization and deployment guides

## Disclaimer
This repository is a research/prototyping codebase and is not certified as a medical device. It must not be used alone for diagnosis or treatment decisions.
