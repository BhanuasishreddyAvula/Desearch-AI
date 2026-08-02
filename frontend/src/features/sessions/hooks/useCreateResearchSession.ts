import { useMutation, useQueryClient } from '@tanstack/react-query';
import { sessionsApi } from '../../../lib/api/sessions';
import type { ResearchSession } from '../../../types';

export interface CreateSessionVariables {
  query: string;
  title?: string;
}

export function useCreateResearchSession() {
  const queryClient = useQueryClient();

  return useMutation<ResearchSession, Error, CreateSessionVariables>({
    mutationFn: ({ query, title }) => sessionsApi.createSession(query, title),
    onSuccess: (newSession) => {
      // Targeted cache invalidation to update sidebar Recent Research list
      queryClient.invalidateQueries({ queryKey: ['research-sessions'] });
      // Populate single session query cache for immediate rendering after navigation
      queryClient.setQueryData(['session', newSession.id], newSession);
    },
  });
}
