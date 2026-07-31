import React from 'react';
import { useResearchSessions } from '../hooks/useResearchSessions';
import { SessionItem } from './SessionItem';
import { RefreshCw } from 'lucide-react';

interface SessionListProps {
  isCollapsed?: boolean;
}

export const SessionList: React.FC<SessionListProps> = ({ isCollapsed = false }) => {
  const { data: sessions, isLoading, isError, refetch } = useResearchSessions();

  // Collapsed rail mode renders 0 session/history/error content
  if (isCollapsed) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="space-y-1 py-1" aria-label="Loading recent research">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="h-8 rounded-md bg-surface/50 border border-border-subtle opacity-60 animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="px-3 py-3 rounded-md bg-surface/40 border border-border-subtle text-xs text-muted-foreground space-y-2">
        <p className="text-foreground/80">Couldn't load recent research.</p>
        <button
          onClick={() => refetch()}
          type="button"
          className="flex items-center gap-1.5 text-[11px] text-accent hover:underline focus:outline-none"
        >
          <RefreshCw className="w-3 h-3" />
          <span>Retry</span>
        </button>
      </div>
    );
  }

  if (!sessions || sessions.length === 0) {
    return (
      <div className="px-3 py-4 text-xs text-text-muted italic text-center">
        No research yet
      </div>
    );
  }

  return (
    <div className="space-y-0.5">
      {sessions.map((session) => (
        <SessionItem key={session.id} session={session} isCollapsed={false} />
      ))}
    </div>
  );
};
