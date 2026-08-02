import React from 'react';
import { ChevronDown, ChevronRight, Loader2, AlertCircle } from 'lucide-react';
import type { ProgressState } from '../../progress/types';
import { ResearchWorkflowSummary } from './ResearchWorkflowSummary';

interface ResearchWorkflowHeaderProps {
  progressState: ProgressState;
  isExpanded: boolean;
  onToggleExpand: () => void;
  onRetry?: () => void;
}

export const ResearchWorkflowHeader: React.FC<ResearchWorkflowHeaderProps> = ({
  progressState,
  isExpanded,
  onToggleExpand,
  onRetry,
}) => {
  const { status, stages, activeStageId, sources, totalExecutionTimeMs, error } = progressState;

  const isCompleted = status === 'completed';
  const isFailed = status === 'failed' || status === 'error';
  const activeStage = activeStageId ? stages[activeStageId] : null;

  // Active or collapsed stage display label
  const activeLabel = activeStage ? activeStage.label : 'Planning research...';

  if (isFailed) {
    return (
      <div className="flex items-center justify-between gap-3 text-xs md:text-sm text-destructive font-sans-ui bg-destructive/10 border border-destructive/30 px-3.5 py-2.5 rounded-xl shadow-xs">
        <div className="flex items-center gap-2 font-medium">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>Research failed</span>
          {error && <span className="text-destructive/80 font-normal">({error})</span>}
        </div>
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="px-2.5 py-1 rounded-md bg-destructive/20 hover:bg-destructive/30 text-destructive-foreground text-xs font-medium transition-colors cursor-pointer focus:outline-none"
          >
            Retry
          </button>
        )}
      </div>
    );
  }

  if (isCompleted) {
    return (
      <div className="flex items-center justify-between gap-2 py-1 select-none">
        <button
          type="button"
          onClick={onToggleExpand}
          className="flex items-center gap-2 text-xs md:text-sm font-medium text-muted-foreground hover:text-white transition-colors cursor-pointer focus:outline-none"
        >
          {isExpanded ? <ChevronDown className="w-4 h-4 shrink-0" /> : <ChevronRight className="w-4 h-4 shrink-0" />}
          <ResearchWorkflowSummary
            sourcesCount={sources.length}
            totalExecutionTimeMs={totalExecutionTimeMs}
          />
        </button>
      </div>
    );
  }

  return (
    <button
      type="button"
      onClick={onToggleExpand}
      aria-expanded={isExpanded}
      className="flex items-center gap-2 text-xs md:text-sm font-medium text-muted-foreground hover:text-white transition-colors cursor-pointer focus:outline-none select-none py-1"
    >
      {isExpanded ? <ChevronDown className="w-4 h-4 shrink-0" /> : <ChevronRight className="w-4 h-4 shrink-0" />}

      <span className="flex items-center gap-2 text-accent font-medium">
        <Loader2 className="w-3.5 h-3.5 animate-spin" />
        <span>{activeLabel}</span>
      </span>
    </button>
  );
};
