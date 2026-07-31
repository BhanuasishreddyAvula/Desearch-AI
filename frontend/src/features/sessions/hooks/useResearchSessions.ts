import { useQuery } from '@tanstack/react-query';
import { sessionsApi } from '../../../lib/api/sessions';
import type { ResearchSession } from '../../../types';

export function useResearchSessions() {
  return useQuery<ResearchSession[], Error>({
    queryKey: ['research-sessions'],
    queryFn: ({ signal }) => sessionsApi.listSessions(signal),
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
}
