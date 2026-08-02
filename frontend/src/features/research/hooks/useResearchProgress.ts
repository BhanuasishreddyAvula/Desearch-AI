import { useReducer, useEffect, useRef } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import type { ResearchSession } from '../../../types';
import { streamResearchProgress } from '../../../lib/sse/reader';
import type { SseStreamControl } from '../../../lib/sse/types';
import {
  createInitialProgressState,
  progressReducer,
} from '../progress/reducer';
import { streamRegistry } from '../utils/streamRegistry';
import { executionTokenRegistry } from '../utils/executionTokenRegistry';
import { API_BASE_URL } from '../../../lib/api/client';
import { getDeviceId } from '../../../lib/device';

export interface UseResearchProgressOptions {
  executionToken?: string;
}

export function useResearchProgress(
  session: ResearchSession | undefined,
  options: UseResearchProgressOptions = {}
) {
  const queryClient = useQueryClient();

  const sessionId = session?.id || '';
  const sessionStatus = session?.status;
  const sessionQuery = session?.query || session?.title || '';
  const executionToken = options.executionToken;

  // Ref holding the SSE control for Q1 so SessionView can abort on Stop
  const streamControlRef = useRef<SseStreamControl | null>(null);

  // Initial status derived from authoritative backend session state or active stream
  const getInitialStreamStatus = () => {
    if (sessionStatus === 'COMPLETED') return 'completed';
    if (sessionStatus === 'FAILED') return 'failed';
    if (sessionId && streamRegistry.hasInitiated(sessionId)) return 'streaming';
    return 'idle';
  };

  const [state, dispatch] = useReducer(
    progressReducer,
    sessionId,
    (id) => createInitialProgressState(id, getInitialStreamStatus())
  );

  // Sync state if session is or becomes COMPLETED or FAILED
  useEffect(() => {
    if (!session) return;

    if (session.status === 'COMPLETED' && state.status !== 'completed') {
      dispatch({ type: 'SET_COMPLETED' });
    }
  }, [session, sessionStatus, state.status]);

  useEffect(() => {
    if (!session || !sessionId || !sessionQuery) return;

    // 1. NEVER stream if session status is COMPLETED or FAILED
    if (sessionStatus === 'COMPLETED' || sessionStatus === 'FAILED') {
      return;
    }

    // 2. NEVER stream if this session ID has already initiated a stream in this browser tab
    if (streamRegistry.hasInitiated(sessionId)) {
      return;
    }

    // 3. Atomically check and consume single-use executionToken
    // MUST NOT start research based on session.status alone!
    const isStartAuthorized = executionTokenRegistry.consumeToken(sessionId, executionToken);

    if (!isStartAuthorized) {
      return;
    }

    // Mark as initiated IMMEDIATELY in module-level registry before calling backend
    streamRegistry.markInitiated(sessionId);

    streamControlRef.current = streamResearchProgress({
      url: '/api/v1/orchestrator/stream',
      body: {
        session_id: sessionId,
        query: sessionQuery,
      },
      onEvent: (event) => {
        dispatch({ type: 'EVENT_RECEIVED', event });

        if (event.event_type === 'workflow.completed') {
          queryClient.invalidateQueries({ queryKey: ['session', sessionId] });
          queryClient.invalidateQueries({ queryKey: ['research-sessions'] });
        }
      },
      onComplete: () => {
        streamControlRef.current = null;
        queryClient.invalidateQueries({ queryKey: ['session', sessionId] });
        queryClient.invalidateQueries({ queryKey: ['research-sessions'] });
      },
      onError: (error) => {
        streamControlRef.current = null;
        dispatch({ type: 'TRANSPORT_ERROR', error: error.message });
      },
    });

    return () => {
      // Cleanup handled externally via stopQ1Stream()
    };
  }, [sessionId, sessionQuery, sessionStatus, executionToken, queryClient]);

  /**
   * Signal cancellation for Q1 (initial session query).
   * Calls the backend /cancel endpoint then aborts the SSE stream.
   * The backend server continues to run unaffected.
   */
  const stopQ1Stream = async () => {
    if (sessionId) {
      try {
        fetch(`${API_BASE_URL}/api/v1/orchestrator/cancel`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Device-ID': getDeviceId(),
          },
          body: JSON.stringify({ session_id: sessionId }),
        }).catch(() => {});
      } catch {
        // silent
      }
    }
    if (streamControlRef.current) {
      streamControlRef.current.abort();
      streamControlRef.current = null;
    }
    dispatch({ type: 'SET_CANCELLED' });
  };

  return {
    progressState: state,
    isStreaming: state.status === 'streaming',
    isCompleted: state.status === 'completed' || sessionStatus === 'COMPLETED',
    isFailed: state.status === 'failed' || state.status === 'error' || sessionStatus === 'FAILED',
    stopQ1Stream,
  };
}
