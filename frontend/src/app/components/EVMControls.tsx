import { useState } from 'react';
import { Sparkles, Power } from 'lucide-react';
import { Button } from './ui/button';
import { Switch } from './ui/switch';
import { Label } from './ui/label';

interface EVMControlsProps {
  evmEnabled: boolean;
  onEnable: () => void;
  onDisable: () => void;
}

export function EVMControls({ evmEnabled, onEnable, onDisable }: EVMControlsProps) {
  const [localEnabled, setLocalEnabled] = useState(evmEnabled);

  const handleToggle = (checked: boolean) => {
    setLocalEnabled(checked);
    if (checked) {
      onEnable();
    } else {
      onDisable();
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-800 bg-gray-950">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-purple-500" />
          Eulerian Video Magnification
        </h2>
      </div>

      <div className="p-4 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Power className={`h-5 w-5 ${evmEnabled ? 'text-green-500' : 'text-gray-500'}`} />
            <div>
              <Label className="text-white font-medium">EVM Processing</Label>
              <p className="text-xs text-gray-400">
                Amplify subtle physiological motions
              </p>
            </div>
          </div>
          <Switch
            checked={localEnabled}
            onCheckedChange={handleToggle}
          />
        </div>

        <div className={`p-3 rounded-lg ${evmEnabled ? 'bg-green-950 border border-green-800' : 'bg-gray-950 border border-gray-800'}`}>
          <div className="flex items-center gap-2">
            <div className={`h-2 w-2 rounded-full ${evmEnabled ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
            <span className={`text-sm font-medium ${evmEnabled ? 'text-green-400' : 'text-gray-500'}`}>
              {evmEnabled ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
