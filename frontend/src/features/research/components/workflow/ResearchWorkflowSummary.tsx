import React from 'react';
import { CheckCircle2, Clock, Globe2, ShieldCheck } from 'lucide-react';

interface ResearchWorkflowSummaryProps {
  sourcesCount: number;
  totalExecutionTimeMs?: number;
}

export const ResearchWorkflowSummary: React.FC<ResearchWorkflowSummaryProps> = ({
  sourcesCount,
  totalExecutionTimeMs,
}) => {
  const formattedTime = totalExecutionTimeMs
    ? totalExecutionTimeMs >= 60000
      ? `${Math.floor(totalExecutionTimeMs / 60000)}m ${Math.round((totalExecutionTimeMs % 60000) / 1000)}s`
      : `${(totalExecutionTimeMs / 1000).toFixed(1)}s`
    : null;

  return (
    <div className="flex flex-wrap items-center gap-2.5 text-xs font-sans-ui text-muted-foreground">
      <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
        <CheckCircle2 className="w-4 h-4 shrink-0" />
        <span>Research completed</span>
      </div>

      <div className="h-3 w-px bg-border-subtle/60" />

      {sourcesCount > 0 && (
        <div className="flex items-center gap-1 bg-surface-hover/80 px-2 py-0.5 rounded-md border border-border-subtle/50 font-mono-code text-[11px]">
          <Globe2 className="w-3 h-3 text-accent" />
          <span>{sourcesCount} {sourcesCount === 1 ? 'source' : 'sources'}</span>
        </div>
      )}

      {formattedTime && (
        <div className="flex items-center gap-1 bg-surface-hover/80 px-2 py-0.5 rounded-md border border-border-subtle/50 font-mono-code text-[11px]">
          <Clock className="w-3 h-3 text-muted-foreground" />
          <span>{formattedTime}</span>
        </div>
      )}

      <div className="flex items-center gap-1 bg-surface-hover/80 px-2 py-0.5 rounded-md border border-border-subtle/50 font-mono-code text-[11px] text-emerald-400/90">
        <ShieldCheck className="w-3 h-3" />
        <span>Confidence: High</span>
      </div>
    </div>
  );
};
