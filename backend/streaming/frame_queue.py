import asyncio
from backend.config import QUEUE_MAXSIZE
from backend.utils.logger import get_logger

logger = get_logger("Frame_queue")

class FrameQueue:

    def __init__(self):
        self.queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)
        self.dropped_frames = 0

    async def put(self, frame):
        if self.queue.full():
            self.dropped_frames += 1
            logger.warning(f"Frame dropped | total_dropped={self.dropped_frames}")

        await self.queue.put(frame)
        logger.info(f"Frame added | queue_size={self.queue.qsize()}")

    async def get(self):
        if self.queue.empty():
            return None
        frame = await self.queue.get()
        return frame
