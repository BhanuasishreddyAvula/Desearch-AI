import { useMutation, useQueryClient } from '@tanstack/react-query';
import { sessionsApi } from '@/lib/api/sessions';

export function useDeleteSession() {
  const queryClient = useQueryClient();

  return useMutation<void, Error, string>({
    mutationFn: (sessionId) => sessionsApi.deleteSession(sessionId),
    onSuccess: (_, deletedSessionId) => {
      queryClient.invalidateQueries({ queryKey: ['research-sessions'] });
      queryClient.removeQueries({ queryKey: ['session', deletedSessionId] });
    },
  });
}
