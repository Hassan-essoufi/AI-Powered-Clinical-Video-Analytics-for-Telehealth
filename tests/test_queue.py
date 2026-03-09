import asyncio
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.streaming.frame_queue import FrameQueue

async def test_queue():
    queue = FrameQueue()

    fake_frame = np.zeros((480, 640, 3))
    print("putting frame in queue....")
    await queue.put(fake_frame)

    print("Getting frame from queue....")
    frame = await queue.get()

    print("frame shape:", frame.shape)

asyncio.run(test_queue())


