import { Activity } from 'lucide-react';

export function Header() {
  return (
    <header className="border-b border-gray-800 bg-gray-950 px-6 py-4">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
          <Activity className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-xl font-semibold text-white">
            AI-Powered Clinical Video Analytics
          </h1>
          <p className="text-sm text-gray-400">Telehealth Monitoring Platform</p>
        </div>
      </div>
    </header>
  );
}
