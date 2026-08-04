import { API_BASE_URL, ApiClientError } from '../api/client';
import { getDeviceId } from '../device';
import type { ProgressEvent } from '../../types';
import type { SseStreamOptions, SseStreamControl } from './types';

/**
 * Low-level SSE fetch reader for POST /api/v1/orchestrator/stream
 * Reads text/event-stream incrementally via ReadableStream default reader.
 */
export function streamResearchProgress(
  options: SseStreamOptions
): SseStreamControl {
  const controller = new AbortController();

  // Combine parent signal with internal abort controller
  if (options.signal) {
    if (options.signal.aborted) {
      controller.abort();
    } else {
      options.signal.addEventListener('abort', () => controller.abort(), { once: true });
    }
  }

  const endpointUrl = options.url.startsWith('http')
    ? options.url
    : `${API_BASE_URL}${options.url.startsWith('/') ? options.url : `/${options.url}`}`;

  (async () => {
    try {
      const response = await fetch(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
          'X-Device-ID': getDeviceId(),  // Device-scoped session ownership
        },
        body: JSON.stringify(options.body),
        signal: controller.signal,
      });


      if (!response.ok) {
        let errorMsg = `HTTP ${response.status}: ${response.statusText}`;
        try {
          const errJson = await response.json();
          if (errJson.detail) errorMsg = errJson.detail;
        } catch {
          // ignore non-json error parsing
        }
        throw new ApiClientError(errorMsg, response.status);
      }

      if (!response.body) {
        throw new ApiClientError('Response body is null', 500);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      let currentEventType = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split(/\r?\n/);
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed) {
            currentEventType = '';
            continue;
          }

          if (trimmed.startsWith('event:')) {
            currentEventType = trimmed.slice(6).trim();
          } else if (trimmed.startsWith('data:')) {
            const dataStr = trimmed.slice(5).trim();
            try {
              const eventData = JSON.parse(dataStr) as ProgressEvent;
              // Ensure event_type is populated from SSE event line if missing in data
              if (!eventData.event_type && currentEventType) {
                eventData.event_type = currentEventType as ProgressEvent['event_type'];
              }
              options.onEvent(eventData);
            } catch {
              // Ignore malformed JSON frame gracefully
            }
          }
        }
      }

      options.onComplete?.();
    } catch (err) {
      if (controller.signal.aborted) {
        return; // Aborted cleanly
      }
      const errorObj = err instanceof Error ? err : new Error(String(err));
      options.onError?.(errorObj);
    }
  })();

  return {
    abort: () => controller.abort(),
  };
}
