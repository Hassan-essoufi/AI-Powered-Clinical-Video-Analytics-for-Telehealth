import { useEffect, useRef } from 'react';
import { ScrollArea } from './ui/scroll-area';
import { Terminal } from 'lucide-react';

interface LogEntry {
  timestamp: string;
  message: string;
  data?: any;
}

interface ActivityLogProps {
  logs: LogEntry[];
}

export function ActivityLog({ logs }: ActivityLogProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden h-full">
      <div className="px-4 py-3 border-b border-gray-800 bg-gray-950">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <Terminal className="h-4 w-4 text-green-500" />
          Activity Log
        </h2>
      </div>
      <ScrollArea className="h-[300px]">
        <div ref={scrollRef} className="p-4 space-y-1 font-mono text-xs">
          {logs.length === 0 ? (
            <div className="text-gray-500">No activity yet...</div>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="flex gap-2 text-gray-300">
                <span className="text-gray-500">[{log.timestamp}]</span>
                <span className="text-cyan-400">{log.message}</span>
                {log.data && (
                  <span className="text-yellow-400">
                    {typeof log.data === 'string' ? log.data : JSON.stringify(log.data)}
                  </span>
                )}
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
