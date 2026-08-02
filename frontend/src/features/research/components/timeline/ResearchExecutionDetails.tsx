import React from 'react';
import { ExecutionSourceChip } from './ExecutionSourceChip';
import type { StageId } from '../../progress/types';

interface ResearchExecutionDetailsProps {
  stageId: StageId;
  sources?: string[];
  isActive?: boolean;
}

const STAGE_TASKS: Record<StageId, string[]> = {
  planning: [
    'Understanding request',
    'Identifying objectives',
    'Creating execution plan',
  ],
  searching: [
    'Searching Google',
    'Searching GitHub',
    'Searching Documentation',
    'Searching Academic Sources',
  ],
  reading: [
    'Extracting key findings',
    'Analyzing evidence items',
    'Cross referencing benchmarks',
  ],
  writing: [
    'Generating Introduction',
    'Generating Comparison',
    'Generating Recommendations',
    'Generating Summary',
  ],
  reviewing: [
    'Checking citations',
    'Checking markdown',
    'Checking consistency',
    'Checking completeness',
  ],
};

export const ResearchExecutionDetails: React.FC<ResearchExecutionDetailsProps> = ({
  stageId,
  sources = [],
  isActive = false,
}) => {
  const tasks = STAGE_TASKS[stageId] || [];

  return (
    <div className="pl-4 py-2 space-y-2 font-sans-ui text-xs text-muted-foreground border-l border-border-subtle/40 animate-in fade-in slide-in-from-top-1 duration-150">
      <div className="space-y-1.5">
        {tasks.map((taskText, idx) => (
          <div
            key={idx}
            className="flex items-center gap-2 animate-in fade-in duration-150"
            style={{ animationDelay: `${idx * 40}ms` }}
          >
            <div
              className={`w-1 h-1 rounded-full ${
                isActive && idx === tasks.length - 1
                  ? 'bg-accent animate-pulse'
                  : 'bg-muted-foreground/40'
              }`}
            />
            <span className={isActive && idx === tasks.length - 1 ? 'text-foreground/90 font-medium' : ''}>
              {taskText}
            </span>
          </div>
        ))}
      </div>

      {/* Discovered Sources Chips for Searching / Extracting */}
      {(stageId === 'searching' || stageId === 'reading') && sources.length > 0 && (
        <div className="pt-2 flex flex-wrap gap-1.5 max-w-xl animate-in fade-in duration-200">
          {sources.map((domain) => (
            <ExecutionSourceChip key={domain} domain={domain} />
          ))}
        </div>
      )}
    </div>
  );
};
