import { apiFetch } from './client';
import type {
  BaseResponse,
  ResearchSession,
  SessionListResponseData,
  SessionStatus,
} from '../../types';

export const sessionsApi = {
  createSession: async (query: string, title?: string, signal?: AbortSignal): Promise<ResearchSession> => {
    const res = await apiFetch<BaseResponse<ResearchSession>>('/api/v1/sessions', {
      method: 'POST',
      body: JSON.stringify({ query, title: title || undefined }),
      signal,
    });
    return res.data;
  },

  listSessions: async (signal?: AbortSignal): Promise<ResearchSession[]> => {
    const res = await apiFetch<BaseResponse<SessionListResponseData>>('/api/v1/sessions', {
      method: 'GET',
      signal,
    });
    return res.data?.sessions || [];
  },

  getSession: async (sessionId: string, signal?: AbortSignal): Promise<ResearchSession> => {
    const res = await apiFetch<BaseResponse<ResearchSession>>(`/api/v1/sessions/${sessionId}`, {
      method: 'GET',
      signal,
    });
    return res.data;
  },

  updateSession: async (
    sessionId: string,
    payload: { title?: string; status?: SessionStatus; metadata?: Record<string, unknown> },
    signal?: AbortSignal
  ): Promise<ResearchSession> => {
    const res = await apiFetch<BaseResponse<ResearchSession>>(`/api/v1/sessions/${sessionId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
      signal,
    });
    return res.data;
  },

  deleteSession: async (sessionId: string, signal?: AbortSignal): Promise<void> => {
    await apiFetch<BaseResponse<null>>(`/api/v1/sessions/${sessionId}`, {
      method: 'DELETE',
      signal,
    });
  },

  renameSession: async (sessionId: string, title: string, signal?: AbortSignal): Promise<ResearchSession> => {
    const res = await apiFetch<BaseResponse<ResearchSession>>(`/api/v1/sessions/${sessionId}`, {
      method: 'PATCH',
      body: JSON.stringify({ title }),
      signal,
    });
    return res.data;
  },
};
