import { useState, useEffect, useCallback, useMemo } from 'react';
import { Header } from './components/Header';
import { KPIStrip } from './components/KPIStrip';
import { CameraPanel } from './components/CameraPanel';
import { EVMControls } from './components/EVMControls';
import { WoundAnalysis } from './components/WoundAnalysis';
import { WebSocketViewer } from './components/WebSocketViewer';
import { ActivityLog } from './components/ActivityLog';
import { useWebSocket } from './hooks/useWebSocket';
import { useCamera } from './hooks/useCamera';
import { useFrameStreaming } from './hooks/useFrameStreaming';
import { MetricsPayload } from './types';
import { getWsBaseUrl } from './utils/network';

interface LogEntry {
  timestamp: string;
  message: string;
  data?: any;
}

function App() {
  const baseUrl = useMemo(() => '', []);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [streamActive, setStreamActive] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [metrics, setMetrics] = useState<MetricsPayload>({});
  const [lastPayload, setLastPayload] = useState<MetricsPayload | null>(null);

  const { isActive: cameraActive, videoRef, startCamera, stopCamera } = useCamera();

  const log = useCallback((message: string, data?: any) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs((prev) => [...prev, { timestamp, message, data }]);
  }, []);

  const handleMetricsMessage = useCallback(
    (data: MetricsPayload) => {
      setLastPayload(data);
      setMetrics((prev) => ({ ...prev, ...data }));
    },
    []
  );

  const wsUrl = getWsBaseUrl(baseUrl);
  const { status: wsStatus } = useWebSocket({
    url: `${wsUrl}/ws/metrics`,
    onMessage: handleMetricsMessage,
    reconnectDelay: 500,
    autoConnect: true,
  });

  const { status: frameStatus, startStreaming, stopStreaming } = useFrameStreaming({
    videoElement: videoRef.current,
    sessionId,
    baseUrl,
    frameInterval: 33,
  });

  const api = async (path: string, init?: RequestInit) => {
    try {
      const response = await fetch(`${baseUrl}${path}`, {
        ...init,
        headers: {
          'Content-Type': 'application/json',
          ...init?.headers,
        },
      });
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      log('API Error', error instanceof Error ? error.message : 'Unknown error');
      throw error;
    }
  };

  const handleStartSession = async () => {
    try {
      log('Starting session...');
      const data = await api('/stream/start', { method: 'POST' });
      setSessionId(data.session_id);
      setStreamActive(true);
      log('Session started', data.session_id);
    } catch (error) {
      log('Failed to start session', error);
    }
  };

  const handleStopSession = async () => {
    if (!sessionId) return;
    try {
      log('Stopping session...');
      await api(`/stream/stop?session_id=${sessionId}`, { method: 'POST' });
      stopStreaming();
      setStreamActive(false);
      setSessionId(null);
      log('Session stopped');
    } catch (error) {
      log('Failed to stop session', error);
    }
  };

  const handleStartCamera = async () => {
    try {
      log('Starting camera...');
      await startCamera();
      log('Camera started');
    } catch (error) {
      log('Failed to start camera', error);
    }
  };

  const handleStopCamera = () => {
    log('Stopping camera...');
    stopCamera();
    stopStreaming();
    log('Camera stopped');
  };

  const handleStartFrameStream = () => {
    if (!sessionId || !cameraActive) {
      log('Cannot start frame stream: missing session or camera');
      return;
    }
    log('Starting frame stream...');
    startStreaming();
    log('Frame stream started');
  };

  const handleStopFrameStream = () => {
    log('Stopping frame stream...');
    stopStreaming();
    log('Frame stream stopped');
  };
  const handleEnableEVM = async () => {
    try {
      log('Enabling EVM...');
      await api('/evm/enable', { method: 'POST' });
      log('EVM enabled');
    } catch (error) {
      log('Failed to enable EVM', error);
    }
  };

  const handleDisableEVM = async () => {
    try {
      log('Disabling EVM...');
      await api('/evm/disable', { method: 'POST' });
      log('EVM disabled');
    } catch (error) {
      log('Failed to disable EVM', error);
    }
  };
  useEffect(() => {
    log('Dashboard initialized');
  }, [log]);

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col">
      <Header />
      
      <KPIStrip
        streamActive={streamActive}
        sessionId={sessionId}
        wsStatus={wsStatus}
        frameStatus={frameStatus}
        bpm={metrics.bpm ?? null}
        rpm={metrics.rpm ?? null}
      />

      <main className="flex-1 p-6 space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <CameraPanel
              videoRef={videoRef}
              cameraActive={cameraActive}
              streamActive={streamActive}
              frameStatus={frameStatus}
              sessionId={sessionId}
              onStartSession={handleStartSession}
              onStopSession={handleStopSession}
              onStartCamera={handleStartCamera}
              onStopCamera={handleStopCamera}
              onStartFrameStream={handleStartFrameStream}
              onStopFrameStream={handleStopFrameStream}
            />
          </div>

          <div className="space-y-6">
            <EVMControls
              evmEnabled={metrics.evm_enabled ?? false}
              onEnable={handleEnableEVM}
              onDisable={handleDisableEVM}
            />
            <WoundAnalysis
              woundArea={metrics.wound_area ?? null}
              infectionRisk={metrics.infection_risk ?? null}
              woundColor={metrics.wound_color ?? null}
              woundStatus={metrics.wound_status ?? null}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <WebSocketViewer lastPayload={lastPayload} />
          <ActivityLog logs={logs} />
        </div>
      </main>
    </div>
  );
}

export default App;
