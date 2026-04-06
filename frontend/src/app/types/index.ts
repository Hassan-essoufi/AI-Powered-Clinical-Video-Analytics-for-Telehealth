export interface MetricsPayload {
  bpm?: number;
  rpm?: number;
  wound_area?: number;
  infection_risk?: string;
  wound_color?: {
    red?: number;
    green?: number;
    blue?: number;
    r_mean?: number;
    g_mean?: number;
    b_mean?: number;
  };
  wound_status?: string;
  evm_enabled?: boolean;
  server_time?: string;
  status?: string;
}

export interface StreamStatus {
  active: boolean;
  session_id?: string;
  frame_count?: number;
}

export interface EVMConfig {
  alpha?: number;
  lambda_c?: number;
  fl?: number;
  fh?: number;
  sample_rate?: number;
}

export interface EVMStatus {
  enabled: boolean;
  config?: EVMConfig;
}

export type ConnectionStatus = 'connected' | 'reconnecting' | 'disconnected';
export type StreamingStatus = 'idle' | 'streaming' | 'stopped';
