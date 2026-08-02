import React from 'react';
import { Check, Circle } from 'lucide-react';
import { cn } from '../../../lib/utils/cn';
import type { ProgressStage } from '../progress/types';

interface ResearchProgressStageProps {
  stage: ProgressStage;
  isActive: boolean;
  children?: React.ReactNode;
}

export const ResearchProgressStage: React.FC<ResearchProgressStageProps> = ({
  stage,
  isActive,
  children,
}) => {
  const isCompleted = stage.status === 'completed';
  const isPending = stage.status === 'pending';

  return (
    <div className="space-y-2 select-none">
      <div className="flex items-center gap-3 text-sm font-sans-ui">
        {/* Status Indicator Icon */}
        <div className="w-5 h-5 flex items-center justify-center shrink-0">
          {isCompleted ? (
            <div className="w-4 h-4 rounded-full bg-accent/20 border border-accent/40 flex items-center justify-center text-accent">
              <Check className="w-3 h-3 stroke-[2.5]" />
            </div>
          ) : isActive ? (
            <div className="w-4 h-4 rounded-full bg-accent/30 border border-accent flex items-center justify-center">
              <span className="w-1.5 h-1.5 rounded-full bg-accent animate-ping" />
            </div>
          ) : (
            <Circle className="w-3 h-3 text-text-muted/40 fill-transparent" />
          )}
        </div>

        {/* Stage Label with Shimmer on Active Stage Only */}
        <div className="flex-1 flex items-center justify-between gap-2 overflow-hidden">
          <span
            className={cn(
              'font-medium transition-colors',
              isCompleted && 'text-foreground/90',
              isActive && 'text-white font-semibold animate-shimmer-stage',
              isPending && 'text-text-muted/60 font-normal'
            )}
          >
            {stage.label}
            {isCompleted && ' complete'}
            {isActive && '...'}
          </span>

          {stage.detail && (
            <span className="text-[11px] font-mono-code text-muted-foreground/70 truncate max-w-[180px]">
              {stage.detail}
            </span>
          )}
        </div>
      </div>

      {/* Embedded Children (e.g., Source Domain Chips under Reading Sources) */}
      {children && <div className="pl-8 pt-1">{children}</div>}
    </div>
  );
};
