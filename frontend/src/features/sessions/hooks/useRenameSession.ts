import { useMutation, useQueryClient } from '@tanstack/react-query';
import { sessionsApi } from '@/lib/api/sessions';
import type { ResearchSession } from '../../../types';

export function useRenameSession() {
  const queryClient = useQueryClient();

  return useMutation<ResearchSession, Error, { sessionId: string; title: string }>({
    mutationFn: ({ sessionId, title }) => sessionsApi.renameSession(sessionId, title),
    onSuccess: (updatedSession) => {
      queryClient.invalidateQueries({ queryKey: ['research-sessions'] });
      queryClient.invalidateQueries({ queryKey: ['session', updatedSession.id] });
    },
  });
}
