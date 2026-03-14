import asyncio
from services.vitals_service import VitalsService
from services.wound_service import WoundService

class VideoProcessor:
    """
    Feeds frames from frame_queue (Person A) to AI modules (Person B).
    Central bridge of the whole pipeline.
    """

    def __init__(self, frame_queue=None):
        self.frame_queue = frame_queue   # from Person A
        self.vitals_service = VitalsService()
        self.wound_service = WoundService()
        self.running = False
        self.frame_buffer = []
        self.buffer_size = 30            # 1 seconde à 30 FPS

    async def start(self):
        """Start consuming frames from the queue."""
        self.running = True
        print("VideoProcessor started")
        await self._process_loop()

    async def _process_loop(self):
        """Main loop: get frames → feed AI modules."""
        while self.running:
            try:
                if self.frame_queue:
                    # Récupérer frame de Person A
                    frame = await self.frame_queue.get()
                    await self._process_frame(frame)
                else:
                    # Mode test sans frame_queue
                    await asyncio.sleep(0.033)  # ~30 FPS

            except Exception as e:
                print(f"VideoProcessor error: {e}")
                await asyncio.sleep(0.1)

    async def _process_frame(self, frame):
        """Process a single frame through all AI modules."""

        # Accumuler les frames dans le buffer
        self.frame_buffer.append(frame)

        # Garder seulement les 30 dernières frames
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

        # Envoyer au module rPPG de Person B toutes les 30 frames
        if len(self.frame_buffer) == self.buffer_size:
            await self._run_vitals()

    async def _run_vitals(self):
        """Send buffer to rPPG module (Person B)."""
        try:
            # TODO: appeler le vrai module de Person B
            # self.vitals_service.estimate_heart_rate(self.frame_buffer)
            bpm = self.vitals_service.get_latest_vitals()
            print(f"Vitals updated: {bpm}")
        except Exception as e:
            print(f"Vitals error: {e}")

    def stop(self):
        """Stop the processing loop."""
        self.running = False
        print("VideoProcessor stopped")