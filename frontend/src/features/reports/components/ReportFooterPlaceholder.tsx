import React from 'react';
import { Download, Layers } from 'lucide-react';

interface ReportFooterPlaceholderProps {
  sourcesCount?: number;
}

export const ReportFooterPlaceholder: React.FC<ReportFooterPlaceholderProps> = ({
  sourcesCount = 0,
}) => {
  return (
    <div className="pt-8 pb-4 mt-10 border-t border-border-subtle/60 flex items-center justify-between text-xs font-sans-ui text-muted-foreground select-none">
      <div className="flex items-center gap-1.5 font-mono-code text-[11px]">
        <Layers className="w-3.5 h-3.5 text-accent/80" />
        <span>{sourcesCount > 0 ? `${sourcesCount} Sources Cited` : 'End of Report'}</span>
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          disabled
          aria-label="Export report placeholder"
          title="Export format choices"
          className="flex items-center gap-1.5 text-xs text-muted-foreground/80 hover:text-white transition-colors cursor-not-allowed opacity-70"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export</span>
        </button>
      </div>
    </div>
  );
};
