import React from 'react';
import type { ProgressState } from '../progress/types';
import { ResearchExecutionTimeline } from './timeline/ResearchExecutionTimeline';
import { ResearchReport } from '../../reports';
import { resolveSourcesForResponse } from '../../../lib/utils/sources';

interface ResearchProgressProps {
  progressState: ProgressState;
  queryTitle: string;
  markdownContent?: string;
  sessionStatus?: string;
  reportSources?: any[];
  onRetry?: () => void;
}

export const ResearchProgress: React.FC<ResearchProgressProps> = ({
  progressState,
  queryTitle,
  markdownContent = '',
  sessionStatus = '',
  reportSources = [],
  onRetry,
}) => {
  const isFailed =
    progressState.status === 'failed' ||
    progressState.status === 'error' ||
    sessionStatus === 'FAILED';

  const isCompleted =
    !isFailed &&
    (progressState.status === 'completed' ||
      sessionStatus === 'COMPLETED' ||
      Boolean(markdownContent) ||
      Boolean(progressState.totalExecutionTimeMs));

  // Consolidate report sources, markdown citations, and live search timeline sources
  const resolvedSources = resolveSourcesForResponse(
    reportSources,
    markdownContent,
    progressState.sources
  );

  const effectiveProgressState: ProgressState = isFailed
    ? { ...progressState, status: 'failed', error: progressState.error || 'Workflow execution failed' }
    : progressState;

  // ── Cancelled: user clicked Stop — show only clean body text message, no timeline or report
  if (progressState.status === 'cancelled') {
    return (
      <p className="text-sm md:text-base text-white/80 font-sans-ui leading-relaxed py-1 animate-in fade-in duration-200">
        Research stopped by user.
      </p>
    );
  }



  return (
    <div className="w-full space-y-1.5 font-sans-ui text-left">
      {/* 1. Progressive Research Execution Timeline */}
      <ResearchExecutionTimeline
        progressState={effectiveProgressState}
        isCompletedOverride={isCompleted}
        sourcesOverride={resolvedSources}
        onRetry={onRetry}
      />



      {/* 2. Research Report Canvas — Renders 4-6px directly below timeline */}
      {isCompleted && (
        <div className="animate-in fade-in duration-250">
          <ResearchReport
            title={queryTitle}
            markdownContent={markdownContent}
            isStreaming={false}
            sources={resolvedSources}
            sourcesCount={resolvedSources.length}
          />
        </div>
      )}
    </div>
  );
};
