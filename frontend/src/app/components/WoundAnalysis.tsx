import { Droplets, AlertTriangle, Palette } from 'lucide-react';

interface WoundAnalysisProps {
  woundArea: number | null;
  infectionRisk: string | null;
  woundColor: {
    red?: number;
    green?: number;
    blue?: number;
    r_mean?: number;
    g_mean?: number;
    b_mean?: number;
  } | null;
  woundStatus: string | null;
}

export function WoundAnalysis({
  woundArea,
  infectionRisk,
  woundColor,
  woundStatus,
}: WoundAnalysisProps) {
  const colorChannels = woundColor
    ? {
        red: woundColor.red ?? woundColor.r_mean ?? 0,
        green: woundColor.green ?? woundColor.g_mean ?? 0,
        blue: woundColor.blue ?? woundColor.b_mean ?? 0,
      }
    : null;

  const getRiskColor = (risk: string | null) => {
    if (!risk) return 'text-gray-500';
    const lower = risk.toLowerCase();
    if (lower.includes('high')) return 'text-red-500';
    if (lower.includes('medium') || lower.includes('moderate')) return 'text-yellow-500';
    return 'text-green-500';
  };

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-800 bg-gray-950">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <Droplets className="h-5 w-5 text-rose-500" />
          Wound Analysis
        </h2>
      </div>

      <div className="p-4 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-950 rounded-lg p-4 border border-gray-800">
            <div className="text-xs text-gray-400 mb-1">Wound Area</div>
            <div className="text-2xl font-bold text-white">
              {woundArea !== null ? `${woundArea.toFixed(2)} cm²` : '--'}
            </div>
          </div>

          <div className="bg-gray-950 rounded-lg p-4 border border-gray-800">
            <div className="flex items-center gap-2 mb-1">
              <AlertTriangle className="h-4 w-4 text-yellow-500" />
              <div className="text-xs text-gray-400">Infection Risk</div>
            </div>
            <div className={`text-2xl font-bold capitalize ${getRiskColor(infectionRisk)}`}>
              {infectionRisk || '--'}
            </div>
          </div>
        </div>

        <div className="bg-gray-950 rounded-lg p-4 border border-gray-800">
          <div className="flex items-center gap-2 mb-3">
            <Palette className="h-4 w-4 text-blue-400" />
            <div className="text-xs text-gray-400">Skin Color Composition</div>
          </div>
          {colorChannels ? (
            <div className="space-y-2">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-12 text-xs text-gray-400">Skin</div>
                <div
                  className="h-5 w-5 rounded-full border border-gray-700"
                  style={{
                    backgroundColor: `rgb(${Math.round(colorChannels.red)}, ${Math.round(colorChannels.green)}, ${Math.round(colorChannels.blue)})`,
                  }}
                />
              </div>

              <div className="flex items-center gap-3">
                <div className="w-12 text-xs text-gray-400">Red</div>
                <div className="flex-1 h-6 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-red-500"
                    style={{ width: `${(colorChannels.red / 255) * 100}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-white text-right">
                  {colorChannels.red.toFixed(1)}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-12 text-xs text-gray-400">Green</div>
                <div className="flex-1 h-6 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500"
                    style={{ width: `${(colorChannels.green / 255) * 100}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-white text-right">
                  {colorChannels.green.toFixed(1)}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-12 text-xs text-gray-400">Blue</div>
                <div className="flex-1 h-6 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500"
                    style={{ width: `${(colorChannels.blue / 255) * 100}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-white text-right">
                  {colorChannels.blue.toFixed(1)}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-4">No data available</div>
          )}
        </div>

        <div className="bg-gray-950 rounded-lg p-4 border border-gray-800">
          <div className="text-xs text-gray-400 mb-2">Status</div>
          <div className="text-sm text-white">
            {woundStatus || 'Awaiting analysis...'}
          </div>
        </div>
      </div>
    </div>
  );
}
