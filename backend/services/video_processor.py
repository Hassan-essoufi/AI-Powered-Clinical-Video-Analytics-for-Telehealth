import asyncio
import cv2
import numpy as np
from backend.api.routes_vitals import LATEST_VITALS
from backend.api.routes_wound import LATEST_WOUND

class VideoProcessor:
    """
    Feeds frames from frame_queue.py to AI modules.
    """

    def __init__(self, frame_queue, result_queue,  vitals_service, wound_service, evm_service=None):
        self.frame_queue = frame_queue  
        self.result_queue = result_queue    
        self.vitals_service = vitals_service
        self.wound_service = wound_service
        self.evm_service = evm_service
        self.running = False

    async def start(self):
        """Start consuming frames from the queue."""
        self.running = True
        await self._process_loop()

    async def _process_loop(self):
        while self.running:
            try:
                frame = await asyncio.wait_for(self.frame_queue.get(), timeout=5)

                if frame is None:
                    break

                processed_frame = frame
                evm_status = None

                if self.evm_service is not None:
                    evm_status = self.evm_service.status()
                    if evm_status.get("enabled"):
                        evm_input = self._prepare_evm_input(frame)
                        evm_output = self.evm_service.process_frame(evm_input)
                        processed_frame = self._restore_analysis_frame(evm_output, frame)

                vitals_task = asyncio.to_thread(
                    self.vitals_service.estimate_vitals, [processed_frame]
                )

                wound_task = asyncio.to_thread(
                    self.wound_service.analyze, processed_frame
                )

                vitals_result, wound_result = await asyncio.gather(
                    vitals_task, wound_task
                )

                bpm = vitals_result.get("bpm") if isinstance(vitals_result, dict) else None
                rpm = vitals_result.get("rpm") if isinstance(vitals_result, dict) else None

                result = {
                    "vitals": {
                        "bpm": bpm,
                        "rpm": rpm,
                    },
                    "wound": wound_result,
                    "evm": evm_status
                }

                LATEST_VITALS["bpm"] = result["vitals"].get("bpm")
                LATEST_VITALS["rpm"] = result["vitals"].get("rpm")

                LATEST_WOUND["area_cm2"] = result["wound"].get("area_cm2")
                LATEST_WOUND["infection_risk"] = result["wound"].get("infection_risk")
                LATEST_WOUND["color_composition"] = result["wound"].get("color_composition")
                LATEST_WOUND["status"] = result["wound"].get("status")

                await self.result_queue.put(result)
            except asyncio.TimeoutError:
                continue
            
            except Exception as e:
                print(f"Error processing frame: {e}")

    async def stop(self):
        self.running = False
        await self.frame_queue.put(None)

    def _prepare_evm_input(self, frame):
        if frame is None:
            return None

        frame_array = np.asarray(frame)
        if frame_array.dtype.kind == "f":
            frame_array = np.clip(frame_array * 255.0, 0, 255).astype(np.uint8)
        else:
            frame_array = np.clip(frame_array, 0, 255).astype(np.uint8)

        return cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)

    def _restore_analysis_frame(self, frame, fallback_frame):
        if frame is None:
            return fallback_frame

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgb_frame.astype(np.float32) / 255.0
