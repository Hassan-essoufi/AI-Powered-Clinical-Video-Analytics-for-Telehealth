from aiortc import MediaStreamTrack

class VideoTracker(MediaStreamTrack):

    kind = "video"

    def __init__(self, track, frame_queue):
        super().__init__()
        self.track = track
        self.frame_queue = frame_queue

        async def recv(self):
            frame = await self.track.recv()
            img = frame.to_ndarry(format="bgr24")
            
            await self.frame_queue.put(img)

            return frame
        