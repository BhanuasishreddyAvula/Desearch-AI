import React, { useState } from 'react';
import { Globe, Download } from 'lucide-react';
import { ExportMenu } from './export/ExportMenu';
import type { ReportSource } from '../../../types';

interface ReportActionBarProps {
  sources?: (string | ReportSource)[];
  sourcesCount?: number;
  markdownContent?: string;
  fullMarkdown?: string;
  title?: string;
  isCompleted?: boolean;
  responseIndex?: number; // 1-based response index (1 = main report, 2..N = follow-ups)
}

export const ReportActionBar: React.FC<ReportActionBarProps> = ({
  sources = [],
  sourcesCount = 0,
  markdownContent = '',
  fullMarkdown = '',
  title = 'Research Report',
  isCompleted = true,
  responseIndex = 1,
}) => {

  const [isExportOpen, setIsExportOpen] = useState(false);

  const activeContent = markdownContent || fullMarkdown;

  // Hidden during streaming, rendered only after research completion
  if (!isCompleted || !activeContent) {
    return null;
  }

  // Universally calculate exact real sources count without hardcoded numbers
  const getEffectiveCount = (): number => {
    // 1. Explicit sources array passed as props
    if (Array.isArray(sources) && sources.length > 0) {
      return sources.length;
    }

    // 2. Explicit sourcesCount passed as props
    if (typeof sourcesCount === 'number' && sourcesCount > 0) {
      return sourcesCount;
    }

    if (activeContent) {
      // 3. Extract bracketed citation numbers e.g. [1], [2], [3]
      const citeMatches = activeContent.match(/\[\d+\]/g) || [];
      if (citeMatches.length > 0) {
        const uniqueNums = new Set(
          citeMatches.map((c) => parseInt(c.replace(/[\[\]]/g, ''), 10)).filter((n) => !isNaN(n))
        );
        if (uniqueNums.size > 0) {
          return uniqueNums.size;
        }
      }

      // 4. Extract cited HTTP URLs and clean domain references
      const urlMatches = activeContent.match(/(https?:\/\/[^\s<>"'\(\)\]]+)/g) || [];
      if (urlMatches.length > 0) {
        const uniqueDomains = new Set(
          urlMatches.map((u) => {
            try {
              return new URL(u).hostname.replace(/^www\./, '');
            } catch {
              return u;
            }
          })
        );
        if (uniqueDomains.size > 0) {
          return uniqueDomains.size;
        }
      }
    }

    return 0; // Return exact real count (0 if no web sources cited)
  };

  const effectiveCount = getEffectiveCount();

  const handleSourcesClick = () => {
    // Triggers top-right Sources floating panel and scrolls/expands matching response group
    window.dispatchEvent(
      new CustomEvent('open-sources-popover', {
        detail: { responseIndex: responseIndex || 1, sourceNumber: 1 },
      })
    );
  };


  return (
    <div className="w-full flex items-center justify-between mt-4 mb-6 pt-0 pb-0 select-none font-sans-ui">
      {/* Left Side: Clickable Sources Chip (Triggers Top-Right Sources Popover) */}
      <button
        type="button"
        onClick={handleSourcesClick}
        role="button"
        aria-label={`View ${effectiveCount} sources`}
        title="Click to view all session sources"
        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface/80 hover:bg-surface-hover border border-border-subtle/70 text-xs text-foreground/90 hover:text-white transition-colors duration-150 cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring whitespace-nowrap shadow-xs"
      >
        <Globe className="w-3.5 h-3.5 text-accent shrink-0" />
        <span className="font-medium truncate max-w-[120px] md:max-w-none">
          {effectiveCount} {effectiveCount === 1 ? 'Source' : 'Sources'}
        </span>
      </button>

      {/* Right Side: Single Export Icon Button */}
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsExportOpen(!isExportOpen)}
          role="button"
          aria-label="Export report options"
          title="Export Report"
          className="p-1.5 text-muted-foreground/80 hover:text-white opacity-75 hover:opacity-100 transition-opacity duration-150 focus:outline-none cursor-pointer"
        >
          <Download className="w-4 h-4" />
        </button>

        {/* Export Menu Dropdown */}
        {isExportOpen && (
          <ExportMenu
            markdownContent={activeContent}
            title={title}
            onClose={() => setIsExportOpen(false)}
          />
        )}
      </div>
    </div>
  );
};
