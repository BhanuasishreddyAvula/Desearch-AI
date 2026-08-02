import React from 'react';
import { ChevronRight, ChevronDown, Check } from 'lucide-react';
import type { StageId, StageStatus } from '../../progress/types';
import { ResearchExecutionDetails } from './ResearchExecutionDetails';

interface ResearchExecutionRowProps {
  stageId: StageId;
  label: string;
  status: StageStatus;
  isExpanded: boolean;
  onToggleExpand: () => void;
  sources?: string[];
  childNode?: React.ReactNode;
}

export const ResearchExecutionRow: React.FC<ResearchExecutionRowProps> = ({
  stageId,
  label,
  status,
  isExpanded,
  onToggleExpand,
  sources = [],
  childNode,
}) => {
  const isActive = status === 'active';
  const isCompleted = status === 'completed';

  return (
    <div className="space-y-1 font-sans-ui text-xs md:text-sm text-left transition-all duration-200">
      {/* Header Button with Post-Text Chevron (Vertically Parallel Left Alignment) */}
      <button
        type="button"
        onClick={onToggleExpand}
        aria-expanded={isExpanded}
        className="flex items-center gap-1 font-medium transition-colors cursor-pointer focus:outline-none select-none py-0.5"
      >
        {isCompleted && (
          <span className="flex items-center gap-1.5 text-white/60 font-medium">
            <span>{label.replace(/\.\.\.$/, '')}</span>
            <Check className="w-3.5 h-3.5 text-white/50 stroke-[2.5]" aria-label="Completed" />
          </span>
        )}

        {isActive && (
          <span className="flex items-center gap-1 animate-shimmer-stage font-medium tracking-wide">
            <span>{label}</span>
          </span>
        )}


        {!isActive && !isCompleted && (
          <span className="text-muted-foreground/60">{label}</span>
        )}

        {/* Chevron AFTER text */}
        {isExpanded ? (
          <ChevronDown className="w-3.5 h-3.5 text-muted-foreground/70" />
        ) : (
          <ChevronRight className="w-3.5 h-3.5 text-muted-foreground/70" />
        )}
      </button>

      {/* Expanded Sub-Task Details + Next Phase List Child (Vertically Parallel Alignment) */}
      {isExpanded && (
        <div className="space-y-2">
          <ResearchExecutionDetails stageId={stageId} sources={sources} isActive={isActive} />
          {childNode && <div className="pt-2">{childNode}</div>}
        </div>
      )}
    </div>
  );
};
