import React from 'react';
import { Globe, ExternalLink } from 'lucide-react';

interface ExecutionSourceChipProps {
  domain: string;
}

export const ExecutionSourceChip: React.FC<ExecutionSourceChipProps> = ({ domain }) => {
  const url = domain.startsWith('http://') || domain.startsWith('https://')
    ? domain
    : `https://${domain}`;

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      title={`Open ${domain}`}
      className="inline-flex items-center gap-1.5 bg-surface-hover/90 hover:bg-surface-elevated text-foreground/90 hover:text-white px-2.5 py-1 rounded-md border border-border-subtle/80 hover:border-accent/50 font-mono-code text-[11px] transition-all duration-150 shadow-xs cursor-pointer select-none group/chip animate-in fade-in duration-150"
    >
      <img
        src={`https://www.google.com/s2/favicons?domain=${domain}&sz=32`}
        alt=""
        aria-hidden="true"
        className="w-3 h-3 rounded-xs shrink-0 object-contain"
        onError={(e) => {
          e.currentTarget.style.display = 'none';
          e.currentTarget.nextElementSibling?.classList.remove('hidden');
        }}
      />
      <Globe className="w-3 h-3 text-muted-foreground hidden shrink-0" aria-hidden="true" />
      <span className="truncate max-w-[160px] group-hover/chip:underline decoration-accent/60 underline-offset-2">
        {domain}
      </span>
      <ExternalLink className="w-2.5 h-2.5 text-muted-foreground/60 group-hover/chip:text-accent transition-colors shrink-0" />
    </a>
  );
};
