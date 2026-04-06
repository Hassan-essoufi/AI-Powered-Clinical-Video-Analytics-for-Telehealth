import time
import cv2
import numpy as np
from aiortc import MediaStreamTrack
from backend.config import VIDEO_WIDTH, VIDEO_HEIGHT
from backend.utils.image_utils import resize_frame, normalize_frame, bgr_to_rgb, extract_roi
from backend.utils.logger import get_logger

logger = get_logger("VideoTrack")

class VideoTracker(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, frame_queue):
        super().__init__()
        self.track = track
        self.frame_queue = frame_queue
        self.frame_count = 0
        self.start_time = time.time()
        self.running = True

    async def recv(self):
        if self.track is None:
            raise RuntimeError("VideoTracker.track is not attached")

        media_frame = await self.track.recv()

        try:
            img = media_frame.to_ndarray(format="bgr24")

            await self.process_bgr_frame(img)

            self.frame_count += 1
            elapsed = time.time() - self.start_time

            if elapsed > 0:
                fps = self.frame_count / elapsed
                logger.info(f"FPS: {fps:.2f}")

            return media_frame
        except Exception as e:
            logger.error(f"Video pipeline error: {e}")
            return media_frame

    async def process_bgr_frame(self, img: np.ndarray) -> bool:
        """Apply tracker preprocessing pipeline to a raw BGR frame and enqueue it."""
        if img is None:
            return False

        roi = extract_roi(img)
        base_img = roi if roi is not None else img
        img_rgb = bgr_to_rgb(base_img)

        if img_rgb is None:
            logger.warning("bgr_to_rgb returned None, skipping frame")
            return False

        resized_img = resize_frame(img_rgb, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
        if resized_img is None:
            logger.warning("resize_frame returned None, skipping frame")
            return False

        normalized = normalize_frame(resized_img)
        if normalized is None:
            logger.warning("normalize_frame returned None, skipping frame")
            return False

        await self.frame_queue.put(normalized)
        return True

    async def process_encoded_frame(self, frame_bytes: bytes) -> bool:
        """Decode an encoded image (jpg/png) and run tracker preprocessing."""
        if not frame_bytes:
            return False

        np_bytes = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_bytes, cv2.IMREAD_COLOR)
        if frame is None:
            return False

        return await self.process_bgr_frame(frame)

    async def stop(self):
        self.running = False