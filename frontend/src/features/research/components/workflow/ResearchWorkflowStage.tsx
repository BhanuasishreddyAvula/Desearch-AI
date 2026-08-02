import React from 'react';
import { Check, Loader2 } from 'lucide-react';
import type { ProgressStage } from '../../progress/types';

interface ResearchWorkflowStageProps {
  stage: ProgressStage;
  isActive: boolean;
  children?: React.ReactNode;
}

export const ResearchWorkflowStage: React.FC<ResearchWorkflowStageProps> = ({
  stage,
  isActive,
  children,
}) => {
  const isCompleted = stage.status === 'completed';
  const isPending = stage.status === 'pending';

  return (
    <div className="space-y-1.5 font-sans-ui text-xs md:text-sm text-left transition-colors duration-200">
      <div className="flex items-center gap-2.5">
        {/* Stage Status Icon */}
        <div className="flex items-center justify-center w-4 h-4 shrink-0">
          {isCompleted && (
            <Check className="w-3.5 h-3.5 text-emerald-400 stroke-[2.5]" aria-label="Completed stage" />
          )}

          {isActive && (
            <Loader2 className="w-3.5 h-3.5 text-accent animate-spin" aria-label="Active stage" />
          )}

          {isPending && (
            <div className="w-3 h-3 border border-muted-foreground/40 rounded-full" aria-hidden="true" />
          )}
        </div>

        {/* Stage Label with Active Shimmer */}
        <div className="flex items-center gap-2">
          <span
            className={
              isCompleted
                ? 'text-white font-medium'
                : isActive
                ? 'text-white font-medium animate-pulse tracking-wide'
                : 'text-muted-foreground'
            }
          >
            {stage.label}
          </span>

          {stage.detail && (
            <span className="text-xs text-muted-foreground/70 font-mono-code">
              ({stage.detail})
            </span>
          )}
        </div>
      </div>

      {/* Discovered Sources or Stage Children */}
      {children && <div className="pl-6.5">{children}</div>}
    </div>
  );
};
