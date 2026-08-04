import React, { useState, useEffect } from 'react';
import { AlertCircle, ChevronRight, ChevronDown, CheckCircle2 } from 'lucide-react';
import type { ProgressState, StageId } from '../../progress/types';
import { ResearchExecutionRow } from './ResearchExecutionRow';
import { ResearchExecutionDetails } from './ResearchExecutionDetails';

interface ResearchExecutionTimelineProps {
  progressState: ProgressState;
  onRetry?: () => void;
  isCompletedOverride?: boolean;
  sourcesOverride?: any[];
}

export const ResearchExecutionTimeline: React.FC<ResearchExecutionTimelineProps> = ({
  progressState,
  onRetry,
  isCompletedOverride = false,
  sourcesOverride = [],
}) => {
  const { status, stages, activeStageId, sources, error, totalExecutionTimeMs, sessionId } = progressState;
  const [expandedStageIds, setExpandedStageIds] = useState<Record<string, boolean>>({});

  // Consolidate live stream sources + completed response sources
  const rawSources = (sourcesOverride && sourcesOverride.length > 0)
    ? sourcesOverride
    : (sources && sources.length > 0 ? sources : []);

  const domainList: string[] = Array.from(
    new Set(
      rawSources.map((item) => {
        if (typeof item === 'string') return item;
        if (typeof item === 'object' && item !== null) {
          return item.domain || item.url || '';
        }
        return '';
      }).filter(Boolean)
    )
  );


  // Restore expanded/collapsed workflow panel state per session from localStorage
  const [isSummaryExpanded, setIsSummaryExpanded] = useState<boolean>(() => {
    if (!sessionId) return false;
    try {
      const saved = localStorage.getItem(`workflow_expanded_${sessionId}`);
      return saved !== null ? saved === 'true' : false;
    } catch {
      return false;
    }
  });

  const isCompleted =
    isCompletedOverride ||
    status === 'completed' ||
    Boolean(totalExecutionTimeMs);

  const isFailed = status === 'failed' || status === 'error';

  const toggleSummaryExpand = () => {
    setIsSummaryExpanded((prev) => {
      const next = !prev;
      if (sessionId) {
        try {
          localStorage.setItem(`workflow_expanded_${sessionId}`, String(next));
        } catch {
          // Silent fallback
        }
      }
      return next;
    });
  };

  // Idle state without completion summary: render nothing
  if (status === 'idle' && !isCompleted) {
    return null;
  }

  const orderedStageIds: StageId[] = [
    'planning',
    'searching',
    'reading',
    'writing',
    'reviewing',
  ];

  const toggleExpand = (id: string) => {
    setExpandedStageIds((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // Format raw technical exceptions into user-friendly messages
  const formatUserFriendlyError = (rawError?: string): string => {
    if (!rawError) return 'Free tier AI limit reached. Please try asking again!';
    const lower = rawError.toLowerCase();
    if (lower.includes('json') || lower.includes('parse') || lower.includes('invalid') || lower.includes('empty')) {
      return 'Free tier AI limit reached or provider returned incomplete output. Please try asking again!';
    }
    if (lower.includes('rate') || lower.includes('429') || lower.includes('quota') || lower.includes('limit')) {
      return 'AI free tier rate limit exceeded. Please wait a few seconds and try again!';
    }
    if (lower.includes('timeout') || lower.includes('network') || lower.includes('504')) {
      return 'Network connection timed out while researching. Please try again!';
    }
    if (lower.includes('workflow execution failed:')) {
      return rawError.replace(/^workflow execution failed:\s*/i, '').trim();
    }
    return rawError;
  };

  // Terminal Failure Alert
  if (isFailed) {
    return (
      <div className="flex items-center justify-between gap-3 text-xs md:text-sm text-destructive font-sans-ui bg-destructive/10 border border-destructive/30 px-3.5 py-2.5 rounded-xl shadow-xs animate-in fade-in duration-200">
        <div className="flex items-center gap-2 font-medium">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>Research failed</span>
          {error && <span className="text-destructive/80 font-normal">({formatUserFriendlyError(error)})</span>}
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

  // 1. Completion State: "Worked for Xm Xs >" collapsed/expanded summary row
  if (isCompleted) {
    const durationMs =
      totalExecutionTimeMs ||
      progressState.totalExecutionTimeMs ||
      (progressState.startTimeMs ? Date.now() - progressState.startTimeMs : undefined);

    const formattedDuration = durationMs
      ? durationMs >= 60000
        ? `${Math.floor(durationMs / 60000)}m ${Math.round((durationMs % 60000) / 1000)}s`
        : `${(durationMs / 1000).toFixed(1)}s`
      : '4.2s';

    return (
      <div className="w-full space-y-2 font-sans-ui text-left select-none animate-in fade-in duration-200">
        <button
          type="button"
          onClick={toggleSummaryExpand}
          aria-expanded={isSummaryExpanded}
          className="flex items-center gap-1.5 text-xs md:text-sm font-medium text-white/60 hover:text-white/90 transition-colors cursor-pointer focus:outline-none py-0.5"
        >
          <CheckCircle2 className="w-3.5 h-3.5 text-white/50" />
          <span>Worked for {formattedDuration}</span>

          {isSummaryExpanded ? (
            <ChevronDown className="w-3.5 h-3.5 text-muted-foreground/70" />
          ) : (
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground/70" />
          )}
        </button>

        {/* Restores exact expanded/collapsed preference */}
        {isSummaryExpanded && (
          <div className="space-y-2 border-l border-border-subtle/40 pl-3 my-2 pt-1 animate-in fade-in duration-200">
            {orderedStageIds.map((stageId) => (
              <ResearchExecutionRow
                key={stageId}
                stageId={stageId}
                label={stages[stageId].label}
                status="completed"
                isExpanded={Boolean(expandedStageIds[stageId])}
                onToggleExpand={() => toggleExpand(stageId)}
                sources={domainList}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  // 2. Active Streaming State: Synchronized Collapsed Row projecting currentActivePhase
  const currentActiveStageId: StageId = activeStageId || 'planning';
  const currentStage = stages[currentActiveStageId] || stages['planning'];
  const currentLabel = currentStage.label || 'Planning research...';
  const activeIndex = orderedStageIds.findIndex((id) => id === currentActiveStageId);
  const safeActiveIndex = activeIndex >= 0 ? activeIndex : 0;

  return (
    <div className="w-full space-y-2 font-sans-ui text-left select-none transition-all duration-200">
      {/* Collapsed Row Header: Always displays currentActivePhase */}
      <button
        type="button"
        onClick={toggleSummaryExpand}
        aria-expanded={isSummaryExpanded}
        className="flex items-center gap-1 text-xs md:text-sm font-medium transition-colors cursor-pointer focus:outline-none select-none py-0.5"
      >
        <span
          key={currentActiveStageId}
          className="flex items-center gap-1 animate-shimmer-stage font-medium tracking-wide animate-in fade-in duration-150"
        >
          <span>{currentLabel}</span>
        </span>


        {isSummaryExpanded ? (
          <ChevronDown className="w-3.5 h-3.5 text-muted-foreground/70" />
        ) : (
          <ChevronRight className="w-3.5 h-3.5 text-muted-foreground/70" />
        )}
      </button>

      {/* Expanded Dropdown */}
      {isSummaryExpanded && (
        <div className="space-y-2 border-l border-border-subtle/40 pl-3 my-2 pt-1 animate-in fade-in duration-200">
          {/* Completed past phases */}
          {orderedStageIds.slice(0, safeActiveIndex).map((stageId) => (
            <ResearchExecutionRow
              key={stageId}
              stageId={stageId}
              label={stages[stageId].label}
              status="completed"
              isExpanded={Boolean(expandedStageIds[stageId])}
              onToggleExpand={() => toggleExpand(stageId)}
              sources={domainList}
            />
          ))}

          {/* Active phase work details directly */}
          <ResearchExecutionDetails
            stageId={currentActiveStageId}
            sources={domainList}
            isActive={true}
          />
        </div>
      )}

    </div>
  );
};
