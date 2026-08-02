import React, { useState, useRef } from 'react';
import type { Source, Evidence } from '../../../../types/citation';
import { ShieldCheck, ShieldAlert, Globe } from 'lucide-react';
import { cn } from '../../../../lib/utils/cn';

interface CitationBadgeProps {
  citationNumber: number;
  source?: Source;
  evidence?: Evidence;
}

export const CitationBadge: React.FC<CitationBadgeProps> = ({
  citationNumber,
  source,
  evidence,
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const badgeRef = useRef<HTMLButtonElement>(null);

  const displayDomain = source?.domain || 'source';
  const displayTitle = source?.title || `${displayDomain} Evidence Reference`;
  const displaySnippet = evidence?.snippet || `Cited evidence and supporting research findings from ${displayDomain}.`;
  const confidence = source?.trustScore || evidence?.confidence || 'High';

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    // Dispatch CustomEvent to open Sources Popover and scroll to matching card
    window.dispatchEvent(
      new CustomEvent('open-sources-popover', {
        detail: {
          sourceNumber: citationNumber,
          domain: displayDomain,
        },
      })
    );
  };

  return (
    <span className="relative inline-block mx-0.5 select-none font-sans-ui">
      <button
        ref={badgeRef}
        type="button"
        onClick={handleClick}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        aria-label={`Citation ${citationNumber}: ${displayTitle}`}
        className="inline-flex items-center justify-center text-[11px] font-semibold text-accent hover:text-white bg-accent/10 hover:bg-accent px-1.5 py-0.5 rounded-md border border-accent/30 hover:border-accent transition-all duration-120 cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent align-baseline"
      >
        [{citationNumber}]
      </button>

      {/* Hover Tooltip (Compact, max 2 lines preview, does NOT open popover) */}
      {isHovered && (
        <div
          role="tooltip"
          className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 w-72 bg-surface/95 backdrop-blur-md border border-border-subtle/90 rounded-xl shadow-2xl p-3 text-left font-sans-ui text-xs animate-popover-in pointer-events-none"
        >
          {/* Header: Domain + Favicon + Confidence Badge */}
          <div className="flex items-center justify-between gap-2 pb-1.5 border-b border-border-subtle/50 mb-1.5">
            <div className="flex items-center gap-1.5 truncate">
              <img
                src={`https://www.google.com/s2/favicons?domain=${displayDomain}&sz=32`}
                alt=""
                aria-hidden="true"
                className="w-3.5 h-3.5 rounded-xs shrink-0 object-contain"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                }}
              />
              <span className="font-medium text-foreground truncate">{displayDomain}</span>
            </div>

            {/* Confidence Badge */}
            <span
              className={cn(
                'inline-flex items-center gap-1 text-[10px] font-medium px-1.5 py-0.5 rounded-md border shrink-0',
                confidence === 'High'
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  : confidence === 'Medium'
                  ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                  : 'bg-muted/10 text-muted-foreground border-muted-foreground/30'
              )}
            >
              {confidence === 'High' ? (
                <ShieldCheck className="w-3 h-3 text-emerald-400" />
              ) : (
                <ShieldAlert className="w-3 h-3 text-amber-400" />
              )}
              <span>{confidence} Confidence</span>
            </span>
          </div>

          {/* Source Title */}
          <h5 className="font-semibold text-white leading-snug line-clamp-1 mb-1">
            {displayTitle}
          </h5>

          {/* Evidence Snippet Preview (Max 2 lines) */}
          <p className="text-[11px] text-muted-foreground/90 leading-relaxed line-clamp-2 font-light">
            {displaySnippet}
          </p>
        </div>
      )}
    </span>
  );
};
