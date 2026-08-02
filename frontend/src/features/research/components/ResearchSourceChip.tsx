import React from 'react';
import { Globe } from 'lucide-react';

interface ResearchSourceChipProps {
  domain: string;
}

export const ResearchSourceChip: React.FC<ResearchSourceChipProps> = ({ domain }) => {
  return (
    <span
      title={`Source domain: ${domain}`}
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-surface-elevated border border-border-subtle text-[11px] font-mono-code text-muted-foreground transition-colors hover:text-foreground"
    >
      <Globe className="w-3 h-3 text-accent shrink-0" />
      <span className="truncate max-w-[140px]">{domain}</span>
    </span>
  );
};
