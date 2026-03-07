import asyncio

class VideoProcessor:
    """
    Feeds frames from frame_queue.py to AI modules.
    Bridge between Person A (streaming) and Person B (AI).
    """

    def __init__(self, frame_queue, vitals_service, wound_service):
        self.frame_queue = frame_queue      # from Person A
        self.vitals_service = vitals_service
        self.wound_service = wound_service
        self.running = False

    async def start(self):
        """Start consuming frames from the queue."""
        self.running = True
        await self._process_loop()

    async def _process_loop(self):
        while self.running:
            # TODO: get frame from frame_queue (Person A)
            # frame = await self.frame_queue.get()
            # self.vitals_service.estimate_heart_rate([frame])
            await asyncio.sleep(0.033)  # ~30 FPS placeholder

    def stop(self):
        self.running = False
