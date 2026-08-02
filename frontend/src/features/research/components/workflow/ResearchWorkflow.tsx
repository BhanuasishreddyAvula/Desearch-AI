import React, { useState } from 'react';
import type { ProgressState, StageId } from '../../progress/types';
import { ResearchWorkflowHeader } from './ResearchWorkflowHeader';
import { ResearchWorkflowStage } from './ResearchWorkflowStage';
import { ResearchWorkflowSourceList } from './ResearchWorkflowSourceList';

interface ResearchWorkflowProps {
  progressState: ProgressState;
  onRetry?: () => void;
}

export const ResearchWorkflow: React.FC<ResearchWorkflowProps> = ({
  progressState,
  onRetry,
}) => {
  const { status, stages, activeStageId, sources } = progressState;
  
  // Default state is Collapsed (isExpanded = false while streaming, true if completed)
  const [isExpanded, setIsExpanded] = useState(false);

  // Empty State: If workflow has not started or is idle, render nothing
  if (status === 'idle') {
    return null;
  }

  const orderedStageIds: StageId[] = [
    'planning',
    'searching',
    'reading',
    'writing',
    'reviewing',
  ];

  return (
    <div className="w-full space-y-3 font-sans-ui text-left">
      {/* 1. Header (Collapsed active stage row OR Completed Summary) */}
      <ResearchWorkflowHeader
        progressState={progressState}
        isExpanded={isExpanded}
        onToggleExpand={() => setIsExpanded((prev) => !prev)}
        onRetry={onRetry}
      />

      {/* 2. Expanded Stages List */}
      {isExpanded && (
        <div className="pl-6 space-y-3 border-l border-border-subtle/50 my-2 animate-in fade-in slide-in-from-top-1 duration-200">
          {orderedStageIds.map((stageId) => {
            const stage = stages[stageId];
            const isActive = activeStageId === stageId;

            return (
              <ResearchWorkflowStage key={stageId} stage={stage} isActive={isActive}>
                {/* Source chips rendered under Extracting content (reading) or Searching sources */}
                {(stageId === 'reading' || stageId === 'searching') && isActive && (
                  <ResearchWorkflowSourceList sources={sources} />
                )}
              </ResearchWorkflowStage>
            );
          })}
        </div>
      )}
    </div>
  );
};
