import { useRef, useState, useCallback } from 'react';
import { StreamingStatus } from '../types';
import { getWsBaseUrl } from '../utils/network';

interface UseFrameStreamingOptions {
  videoElement: HTMLVideoElement | null;
  sessionId: string | null;
  baseUrl: string;
  frameInterval?: number;
}

export function useFrameStreaming({
  videoElement,
  sessionId,
  baseUrl,
  frameInterval = 100,
}: UseFrameStreamingOptions) {
  const [status, setStatus] = useState<StreamingStatus>('idle');
  const wsRef = useRef<WebSocket | null>(null);
  const intervalRef = useRef<NodeJS.Timeout>();
  const canvasRef = useRef<HTMLCanvasElement>();
  const shouldStreamRef = useRef(false);

  const startStreaming = useCallback(() => {
    if (!videoElement || !sessionId) {
      console.error('Cannot start streaming: missing video element or session ID');
      return;
    }

    shouldStreamRef.current = true;
    const wsUrl = getWsBaseUrl(baseUrl);
    const ws = new WebSocket(`${wsUrl}/stream/ws/frame-stream/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('Frame streaming WebSocket connected');
      setStatus('streaming');

      if (!canvasRef.current) {
        canvasRef.current = document.createElement('canvas');
      }
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      intervalRef.current = setInterval(() => {
        if (
          !videoElement ||
          !ws ||
          ws.readyState !== WebSocket.OPEN ||
          !shouldStreamRef.current
        ) {
          return;
        }

        // Skip if buffered amount is too high (>100KB) to prevent lag
        if (ws.bufferedAmount > 100000) {
          return;
        }

        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;

        if (ctx && canvas.width > 0 && canvas.height > 0) {
          ctx.drawImage(videoElement, 0, 0);
          canvas.toBlob(
            (blob) => {
              if (blob && ws.readyState === WebSocket.OPEN) {
                blob.arrayBuffer().then((buffer) => {
                  ws.send(buffer);
                });
              }
            },
            'image/jpeg',
            0.8
          );
        }
      }, frameInterval);
    };

    ws.onerror = (error) => {
      console.error('Frame streaming WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('Frame streaming WebSocket closed');
      setStatus('stopped');
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }

      // Auto-reconnect if should still be streaming
      if (shouldStreamRef.current && sessionId) {
        setTimeout(() => {
          if (shouldStreamRef.current) {
            startStreaming();
          }
        }, 1000);
      }
    };
  }, [videoElement, sessionId, baseUrl, frameInterval]);

  const stopStreaming = useCallback(() => {
    shouldStreamRef.current = false;
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setStatus('idle');
  }, []);

  return { status, startStreaming, stopStreaming };
}
