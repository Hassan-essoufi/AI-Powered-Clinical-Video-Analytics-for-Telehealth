import { useEffect } from 'react';
import { Video, VideoOff, Play, Square, PlayCircle, StopCircle } from 'lucide-react';
import { Button } from './ui/button';
import { StreamingStatus } from '../types';

interface CameraPanelProps {
  videoRef: React.RefObject<HTMLVideoElement | null>;
  cameraActive: boolean;
  streamActive: boolean;
  frameStatus: StreamingStatus;
  sessionId: string | null;
  onStartSession: () => void;
  onStopSession: () => void;
  onStartCamera: () => void;
  onStopCamera: () => void;
  onStartFrameStream: () => void;
  onStopFrameStream: () => void;
}

export function CameraPanel({
  videoRef,
  cameraActive,
  streamActive,
  frameStatus,
  sessionId,
  onStartSession,
  onStopSession,
  onStartCamera,
  onStopCamera,
  onStartFrameStream,
  onStopFrameStream,
}: CameraPanelProps) {
  useEffect(() => {
    const video = videoRef.current;
    if (video && cameraActive) {
      video.play().catch((err) => console.error('Failed to play video:', err));
    }
  }, [cameraActive, videoRef]);

  return (
    <div className="flex flex-col bg-gray-900 rounded-lg border border-gray-800 overflow-hidden h-full">
      <div className="px-4 py-2 border-b border-gray-800 bg-gray-950 flex justify-center items-center gap-2 flex-nowrap overflow-x-auto">
        <Button
          onClick={onStartSession}
          disabled={streamActive}
          className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs h-9 px-2 font-medium flex-shrink-0"
        >
          <Play className="h-3 w-3 mr-1" />
          Session
        </Button>
        <Button
          onClick={onStopSession}
          disabled={!streamActive}
          variant="destructive"
          className="text-xs h-9 px-2 font-medium flex-shrink-0"
        >
          <Square className="h-3 w-3 mr-1" />
          Stop
        </Button>

        <Button
          onClick={onStartCamera}
          disabled={cameraActive}
          className="bg-purple-600 hover:bg-purple-700 text-white text-xs h-9 px-2 font-medium flex-shrink-0"
        >
          <Video className="h-3 w-3 mr-1" />
          Camera
        </Button>
        <Button
          onClick={onStopCamera}
          disabled={!cameraActive}
          className="bg-orange-600 hover:bg-orange-700 text-white text-xs h-9 px-2 font-medium flex-shrink-0"
        >
          <VideoOff className="h-3 w-3 mr-1" />
          Stop
        </Button>

        <Button
          onClick={onStartFrameStream}
          disabled={frameStatus === 'streaming' || !sessionId || !cameraActive}
          className="bg-cyan-600 hover:bg-cyan-700 text-white text-xs h-9 px-2 font-medium flex-shrink-0"
        >
          <PlayCircle className="h-3 w-3 mr-1" />
          Stream
        </Button>
        <Button
          onClick={onStopFrameStream}
          disabled={frameStatus !== 'streaming'}
          variant="destructive"
          className="text-xs h-9 px-2 font-medium flex-shrink-0"
        >
          <StopCircle className="h-3 w-3 mr-1" />
          Stop
        </Button>
      </div>

      <div className="flex-1 relative bg-black">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-contain"
        />
        {!cameraActive && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <VideoOff className="h-16 w-16 text-gray-600 mx-auto mb-3" />
              <p className="text-gray-500">Camera not active</p>
            </div>
          </div>
        )}
        {frameStatus === 'streaming' && (
          <div className="absolute top-4 right-4 flex items-center gap-2 bg-red-600 px-3 py-1 rounded-full">
            <div className="h-2 w-2 rounded-full bg-white animate-pulse" />
            <span className="text-xs font-semibold text-white">STREAMING</span>
          </div>
        )}
      </div>
    </div>
  );
}
