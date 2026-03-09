import asyncio
from backend.config import QUEUE_MAXSIZE

class FrameQueue:

    def __init__(self):
        self.queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)

    async def put(self, frame):
        await self.queue.put(frame)

    async def get(self):
        frame = await self.queue.get()
        return frame
