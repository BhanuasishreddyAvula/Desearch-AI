import React, { useState } from 'react';
import { useResearchSessions } from '../hooks/useResearchSessions';
import { SessionItem } from './SessionItem';
import { ChevronDown, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils/cn';

interface SessionListProps {
  isCollapsed?: boolean;
}

export const SessionList: React.FC<SessionListProps> = ({ isCollapsed = false }) => {
  const [isRecentsExpanded, setIsRecentsExpanded] = useState(true);
  const { data: sessions, isLoading, isError, refetch } = useResearchSessions();

  // Collapsed workspace rail renders 0 history content
  if (isCollapsed) {
    return null;
  }

  const toggleRecents = () => {
    setIsRecentsExpanded((prev) => !prev);
  };

  const SKELETON_WIDTHS = [88, 68, 94, 75, 82];

  return (
    <div className="space-y-1 font-sans-ui select-none">
      {/* Recents Header Row */}
      <button
        type="button"
        onClick={toggleRecents}
        aria-expanded={isRecentsExpanded}
        aria-label={isRecentsExpanded ? 'Collapse recent research' : 'Expand recent research'}
        className="w-full flex items-center justify-between h-8 px-2.5 rounded-md text-foreground/90 hover:bg-surface-hover/50 transition-[background-color,color] duration-200 ease-out focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring group text-left cursor-pointer"
      >
        <span className="text-[13px] font-semibold tracking-tight">Recents</span>
        <ChevronDown
          className={cn(
            'w-3.5 h-3.5 text-muted-foreground group-hover:text-white transition-transform duration-200 shrink-0',
            !isRecentsExpanded && '-rotate-90'
          )}
        />
      </button>

      {/* Recents Session History List */}
      <div
        className={cn(
          'space-y-0.5 transition-all duration-200 ease-out overflow-hidden',
          isRecentsExpanded
            ? 'max-h-[800px] opacity-100'
            : 'max-h-0 opacity-0 pointer-events-none'
        )}
      >
        {/* Skeleton Shimmer Rows (Matching Chat Interface ReportSkeleton) */}
        {isLoading && (
          <div className="space-y-2 py-2 px-2.5" aria-label="Loading recent research">
            {SKELETON_WIDTHS.map((widthPct, i) => (
              <div
                key={i}
                style={{ width: `${widthPct}%` }}
                className="h-4 bg-surface-hover/70 rounded-md animate-pulse"
              />
            ))}
          </div>
        )}

        {isError && (
          <div className="px-3 py-3 rounded-md bg-surface/40 border border-border-subtle text-xs text-muted-foreground space-y-2 my-1">
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
        )}

        {!isLoading && !isError && (!sessions || sessions.length === 0) && (
          <div className="px-3 py-3 text-xs text-muted-foreground italic text-center">
            No recent research
          </div>
        )}

        {!isLoading &&
          !isError &&
          sessions &&
          sessions.map((session) => (
            <SessionItem key={session.id} session={session} isCollapsed={false} />
          ))}
      </div>
    </div>
  );
};
