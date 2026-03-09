import time
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

    async def recv(self):
        
        try:
            frame = await self.track.recv()
            img = frame.to_ndarray(format="bgr24")

            # Transfomrmations
            frame = extract_roi(img)
            img_rgb = bgr_to_rgb(img)
            resized_img = resize_frame(img_rgb, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
            normalized = normalize_frame(resized_img)
            
            await self.frame_queue.put(normalized)
            self.frame_count += 1
            elapsed = time.time() - self.start_time

            if elapsed > 0:
                fps = self.frame_count / elapsed
                logger.info(f"FPS: {fps:.2f}")

            return frame
        except Exception as e:
            logger.error(f"Video pipeline error: {e}")
            return frame
    