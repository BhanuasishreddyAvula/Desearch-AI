import React from 'react';
import { Globe } from 'lucide-react';

interface ResearchWorkflowSourceListProps {
  sources: string[];
  maxDisplayCount?: number;
}

export const ResearchWorkflowSourceList: React.FC<ResearchWorkflowSourceListProps> = ({
  sources,
  maxDisplayCount = 8,
}) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  const visibleSources = sources.slice(0, maxDisplayCount);
  const overflowCount = sources.length - maxDisplayCount;

  return (
    <div className="flex flex-wrap gap-1.5 pt-2 max-w-xl animate-in fade-in duration-200">
      {visibleSources.map((domain) => (
        <div
          key={domain}
          title={domain}
          className="inline-flex items-center gap-1.5 bg-surface-hover/90 hover:bg-surface-elevated text-foreground/90 hover:text-white px-2.5 py-1 rounded-md border border-border-subtle/80 font-mono-code text-[11px] transition-all duration-150 shadow-xs cursor-default select-none animate-in fade-in zoom-in-95 duration-150"
        >
          <img
            src={`https://www.google.com/s2/favicons?domain=${domain}&sz=32`}
            alt=""
            aria-hidden="true"
            className="w-3 h-3 rounded-xs shrink-0 object-contain"
            onError={(e) => {
              // Fallback to globe icon if favicon load fails
              e.currentTarget.style.display = 'none';
              e.currentTarget.nextElementSibling?.classList.remove('hidden');
            }}
          />
          <Globe className="w-3 h-3 text-muted-foreground hidden shrink-0" aria-hidden="true" />
          <span className="truncate max-w-[140px]">{domain}</span>
        </div>
      ))}

      {overflowCount > 0 && (
        <div className="inline-flex items-center px-2 py-1 rounded-md bg-surface-hover text-muted-foreground font-mono-code text-[11px] border border-border-subtle/60 select-none">
          +{overflowCount} more
        </div>
      )}
    </div>
  );
};
