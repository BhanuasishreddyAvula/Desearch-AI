import type { ProgressEvent } from '../../types';

export interface SseStreamOptions {
  url: string;
  body: unknown;
  signal?: AbortSignal;
  onEvent: (event: ProgressEvent) => void;
  onError?: (error: Error) => void;
  onComplete?: () => void;
}

export interface SseStreamControl {
  abort: () => void;
}
