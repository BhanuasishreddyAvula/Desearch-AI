/**
 * Desearch AI Thin API Client Abstraction
 * Communicates ONLY with FastAPI backend (never direct to OpenRouter/Exa/Firecrawl/Supabase).
 */

import { getDeviceId } from '../device';

export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public errorCode?: string,
    public detail?: string
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

const getBaseUrl = (): string => {
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (envUrl) {
    return envUrl.replace(/\/+$/, '');
  }
  return 'http://127.0.0.1:8000';
};

export const API_BASE_URL = getBaseUrl();

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }
  if (!headers.has('Accept')) {
    headers.set('Accept', 'application/json');
  }
  // Inject the persistent anonymous device ID on every request.
  // The backend uses this to scope session lists and enforce ownership.
  headers.set('X-Device-ID', getDeviceId());


  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      let errorCode: string | undefined;
      let errorDetail: string | undefined;

      try {
        const errorJson = await response.json();
        if (typeof errorJson.detail === 'string') {
          errorMessage = errorJson.detail;
          errorDetail = errorJson.detail;
        } else if (typeof errorJson.message === 'string') {
          errorMessage = errorJson.message;
        }
        if (typeof errorJson.error_code === 'string') {
          errorCode = errorJson.error_code;
        }
      } catch {
        // Fallback to HTTP status text if response is not JSON
      }

      throw new ApiClientError(errorMessage, response.status, errorCode, errorDetail);
    }

    // 204 No Content handling
    if (response.status === 204) {
      return undefined as unknown as T;
    }

    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new ApiClientError('Request was cancelled', 499, 'ABORTED');
    }
    throw new ApiClientError(
      error instanceof Error ? error.message : 'Network request failed',
      500,
      'NETWORK_ERROR'
    );
  }
}
