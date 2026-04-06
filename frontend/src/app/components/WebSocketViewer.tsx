import { Code } from 'lucide-react';
import { MetricsPayload } from '../types';

interface WebSocketViewerProps {
  lastPayload: MetricsPayload | null;
}

export function WebSocketViewer({ lastPayload }: WebSocketViewerProps) {
  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden h-full">
      <div className="px-4 py-3 border-b border-gray-800 bg-gray-950">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <Code className="h-4 w-4 text-cyan-500" />
          Live WebSocket Payload
        </h2>
      </div>
      <div className="p-4 overflow-auto max-h-[300px]">
        <pre className="text-xs text-green-400 font-mono bg-black rounded p-3 overflow-x-auto">
          {lastPayload ? JSON.stringify(lastPayload, null, 2) : 'Waiting for data...'}
        </pre>
      </div>
    </div>
  );
}
