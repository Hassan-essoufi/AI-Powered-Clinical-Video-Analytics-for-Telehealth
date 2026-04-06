import asyncio
import unittest

import numpy as np

from backend.streaming.frame_queue import FrameQueue


class TestFrameQueue(unittest.TestCase):
    def test_put_get_roundtrip(self):
        queue = FrameQueue()
        fake_frame = np.zeros((480, 640, 3), dtype=np.float32)

        async def _scenario():
            await queue.put(fake_frame)
            frame = await queue.get()
            return frame

        frame = asyncio.run(_scenario())
        self.assertEqual(frame.shape, (480, 640, 3))

    def test_empty_flag(self):
        queue = FrameQueue()
        self.assertTrue(queue.empty())

        async def _scenario():
            await queue.put(np.zeros((2, 2, 3), dtype=np.float32))

        asyncio.run(_scenario())
        self.assertFalse(queue.empty())


if __name__ == "__main__":
    unittest.main()



