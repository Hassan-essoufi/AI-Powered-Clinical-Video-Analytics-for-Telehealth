import asyncio
from backend.api.routes_vitals import LATEST_VITALS

class VideoProcessor:
    """
    Feeds frames from frame_queue.py to AI modules.
    Bridge between Person A (streaming) and Person B (AI).
    """

    def __init__(self, frame_queue, result_queue,  vitals_service, wound_service):
        self.frame_queue = frame_queue  
        self.result_queue = result_queue    
        self.vitals_service = vitals_service
        self.wound_service = wound_service
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
                vitals_task = asyncio.to_thread(
                    self.vitals_service.estimate_heart_rate, [frame]
                )

                wound_task = asyncio.to_thread(
                    self.wound_service.analyze, frame
                )

                vitals_result, wound_result = await asyncio.gather(
                    vitals_task, wound_task
                )

                result = {
                    "vitals": vitals_result,
                    "wound": wound_result
                }

                LATEST_VITALS["bpm"] = result["vitals"].get("bpm")
                LATEST_VITALS["rpm"] = result["vitals"].get("rpm")
                await self.result_queue.put(result)
            except asyncio.TimeoutError:
                continue
            
            except Exception as e:
                print(f"Error processing frame: {e}")

    async def stop(self):
        self.running = False
        await self.frame_queue.put(None)
