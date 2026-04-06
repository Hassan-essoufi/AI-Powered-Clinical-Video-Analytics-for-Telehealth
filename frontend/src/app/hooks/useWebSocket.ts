import { useEffect, useRef, useState, useCallback } from 'react';
import { ConnectionStatus } from '../types';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  reconnectDelay?: number;
  autoConnect?: boolean;
}

export function useWebSocket({
  url,
  onMessage,
  reconnectDelay = 500,
  autoConnect = true,
}: UseWebSocketOptions) {
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const shouldConnectRef = useRef(autoConnect);

  const connect = useCallback(() => {
    if (!url || wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        setStatus('connected');
        console.log('WebSocket connected:', url);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          onMessage?.(data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        setStatus('disconnected');
        console.log('WebSocket closed:', url);

        if (shouldConnectRef.current) {
          setStatus('reconnecting');
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectDelay);
        }
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setStatus('disconnected');
    }
  }, [url, onMessage, reconnectDelay]);

  const disconnect = useCallback(() => {
    shouldConnectRef.current = false;
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setStatus('disconnected');
  }, []);

  const send = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      if (data instanceof ArrayBuffer) {
        wsRef.current.send(data);
      } else {
        wsRef.current.send(JSON.stringify(data));
      }
    }
  }, []);

  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    return () => {
      shouldConnectRef.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect, autoConnect]);

  return { status, connect, disconnect, send };
}
