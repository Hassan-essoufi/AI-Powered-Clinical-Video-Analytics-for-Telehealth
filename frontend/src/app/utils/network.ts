export function normalizeBaseUrl(raw: string | undefined | null): string {
  if (!raw) {
    return '';
  }
  return raw.replace(/\/+$/, '');
}

export function getApiBaseUrl(raw: string | undefined | null): string {
  return normalizeBaseUrl(raw);
}

export function getWsBaseUrl(raw: string | undefined | null): string {
  const normalized = normalizeBaseUrl(raw);

  if (normalized) {
    return normalized.replace('http://', 'ws://').replace('https://', 'wss://');
  }

  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${window.location.host}`;
  }

  return '';
}
