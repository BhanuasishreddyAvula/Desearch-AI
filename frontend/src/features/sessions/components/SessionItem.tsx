import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { FileText } from 'lucide-react';
import { cn } from '../../../lib/utils/cn';
import type { ResearchSession } from '../../../types';

interface SessionItemProps {
  session: ResearchSession;
  isCollapsed?: boolean;
}

export const SessionItem: React.FC<SessionItemProps> = ({ session, isCollapsed = false }) => {
  const navigate = useNavigate();
  const { sessionId: activeSessionId } = useParams<{ sessionId?: string }>();
  const isSelected = activeSessionId === session.id;

  const displayTitle = session.title || session.query || 'Untitled Research';

  const handleClick = () => {
    navigate(`/research/${session.id}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  if (isCollapsed) {
    return (
      <button
        type="button"
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        title={displayTitle}
        aria-label={`Open research session: ${displayTitle}`}
        className={cn(
          'w-full flex items-center justify-center p-2 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-focus-ring',
          isSelected
            ? 'bg-surface border-l-2 border-accent text-foreground'
            : 'text-muted-foreground hover:bg-surface-hover hover:text-foreground'
        )}
      >
        <FileText className={cn('w-4 h-4', isSelected ? 'text-accent' : 'text-muted-foreground')} />
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      title={displayTitle}
      aria-label={`Open research session: ${displayTitle}`}
      className={cn(
        'w-full text-left px-3 py-2 rounded-md transition-colors text-xs font-sans-ui flex items-center gap-2.5 group focus:outline-none focus:ring-2 focus:ring-focus-ring',
        isSelected
          ? 'bg-surface text-foreground font-medium border-l-2 border-accent shadow-sm'
          : 'text-muted-foreground hover:bg-surface-hover hover:text-foreground'
      )}
    >
      <FileText className={cn('w-3.5 h-3.5 shrink-0', isSelected ? 'text-accent' : 'text-text-muted group-hover:text-foreground')} />
      <span className="truncate flex-1">{displayTitle}</span>
    </button>
  );
};
