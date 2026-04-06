import { Activity, Heart, Wind, Camera, Wifi } from 'lucide-react';
import { ConnectionStatus, StreamingStatus } from '../types';

interface KPIStripProps {
  streamActive: boolean;
  sessionId: string | null;
  wsStatus: ConnectionStatus;
  frameStatus: StreamingStatus;
  bpm: number | null;
  rpm: number | null;
}

export function KPIStrip({
  streamActive,
  sessionId,
  wsStatus,
  frameStatus,
  bpm,
  rpm,
}: KPIStripProps) {
  const getStatusColor = (status: ConnectionStatus) => {
    switch (status) {
      case 'connected':
        return 'text-green-500';
      case 'reconnecting':
        return 'text-yellow-500';
      case 'disconnected':
        return 'text-red-500';
    }
  };

  const getStreamStatusColor = (status: StreamingStatus) => {
    switch (status) {
      case 'streaming':
        return 'text-green-500';
      case 'idle':
        return 'text-gray-500';
      case 'stopped':
        return 'text-red-500';
    }
  };

  return (
    <div className="border-b border-gray-800 bg-gray-900 px-6 py-4">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-blue-500" />
          <div>
            <div className="text-xs text-gray-400">Stream Status</div>
            <div className={`text-sm font-semibold ${streamActive ? 'text-green-500' : 'text-gray-500'}`}>
              {streamActive ? 'Active' : 'Inactive'}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Wifi className="h-5 w-5 text-purple-500" />
          <div>
            <div className="text-xs text-gray-400">WS Status</div>
            <div className={`text-sm font-semibold capitalize ${getStatusColor(wsStatus)}`}>
              {wsStatus}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Camera className="h-5 w-5 text-cyan-500" />
          <div>
            <div className="text-xs text-gray-400">Frame Stream</div>
            <div className={`text-sm font-semibold capitalize ${getStreamStatusColor(frameStatus)}`}>
              {frameStatus}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex h-5 w-5 items-center justify-center rounded bg-gray-700 text-xs text-gray-300">
            ID
          </div>
          <div>
            <div className="text-xs text-gray-400">Session ID</div>
            <div className="text-sm font-semibold text-white truncate max-w-[120px]">
              {sessionId || 'None'}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Heart className="h-5 w-5 text-red-500" />
          <div>
            <div className="text-xs text-gray-400">Heart Rate</div>
            <div className="text-sm font-semibold text-white">
              {bpm !== null ? `${bpm} BPM` : '--'}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Wind className="h-5 w-5 text-teal-500" />
          <div>
            <div className="text-xs text-gray-400">Respiration</div>
            <div className="text-sm font-semibold text-white">
              {rpm !== null ? `${rpm} RPM` : '--'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
