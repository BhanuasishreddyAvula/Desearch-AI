import React, { useEffect, useState } from 'react';
import { ExternalLink, Globe, ChevronDown, ChevronUp, Layers } from 'lucide-react';
import { cn } from '@/lib/utils/cn';

export interface SourceItem {
  domain: string;
  title?: string;
  url?: string;
  snippet?: string;
  category?: string;
  confidence?: 'High' | 'Medium' | 'Low';
  timestamp?: string;
}

export interface SourceGroup {
  id: string;
  title: string;
  responseIndex: number; // 1-based index (1 = main report, 2..N = follow-ups)
  sources: SourceItem[];
}

interface SourcesDropdownProps {
  groups: SourceGroup[];
  isOpen: boolean;
  targetResponseIndex?: number;
  highlightedSourceNumber?: number;
}

export const SourcesDropdown: React.FC<SourcesDropdownProps> = ({
  groups = [],
  isOpen,
  targetResponseIndex,
  highlightedSourceNumber,
}) => {
  // Track expanded state for each response group accordion
  const [expandedGroups, setExpandedGroups] = useState<Record<string, boolean>>({});

  // Initialize all groups as expanded by default when groups change
  useEffect(() => {
    if (groups.length > 0) {
      const initial: Record<string, boolean> = {};
      groups.forEach((g) => {
        initial[g.id] = true;
      });
      setExpandedGroups((prev) => ({ ...initial, ...prev }));
    }
  }, [groups]);

  // When triggered by inline source chip or citation badge, ensure target group is expanded & scrolled into view
  useEffect(() => {
    if (!isOpen) return;

    if (targetResponseIndex) {
      const targetGroup = groups.find((g) => g.responseIndex === targetResponseIndex);
      if (targetGroup) {
        setExpandedGroups((prev) => ({ ...prev, [targetGroup.id]: true }));
        setTimeout(() => {
          const el = document.getElementById(`source-group-${targetResponseIndex}`);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        }, 100);
      }
    } else if (highlightedSourceNumber) {
      setTimeout(() => {
        const targetCard = document.getElementById(`source-card-${highlightedSourceNumber}`);
        if (targetCard) {
          targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    }
  }, [isOpen, targetResponseIndex, highlightedSourceNumber, groups]);

  if (!isOpen) return null;

  const toggleGroup = (groupId: string) => {
    setExpandedGroups((prev) => ({
      ...prev,
      [groupId]: !prev[groupId],
    }));
  };

  const totalSourcesCount = groups.reduce((acc, g) => acc + g.sources.length, 0);

  return (
    <div
      role="dialog"
      aria-label="Session Sources Panel"
      className="absolute top-full right-0 mt-2 z-40 w-80 md:w-[420px] bg-surface/95 backdrop-blur-md border border-border-subtle/90 rounded-2xl shadow-2xl p-3 font-sans-ui text-left select-none animate-popover-in"
    >
      {/* Panel Header */}
      <div className="flex items-center justify-between pb-2 mb-2 border-b border-border-subtle/60 px-1">
        <div className="flex items-center gap-2">
          <Globe className="w-4 h-4 text-accent" />
          <h3 className="text-xs font-semibold text-foreground tracking-wide uppercase">
            Session Sources
          </h3>
        </div>
      </div>

      {/* Scrollable Response Groups Container (Medium height with smooth scrolling) */}
      <div className="max-h-[300px] overflow-y-auto space-y-3 pr-1 custom-scrollbar">


        {groups.length === 0 || totalSourcesCount === 0 ? (
          <div className="py-8 text-center text-xs text-muted-foreground/80 space-y-1.5">
            <Globe className="w-6 h-6 mx-auto text-muted-foreground/40" />
            <p className="font-medium text-foreground/80">No active sources cited yet.</p>
            <p className="text-[11px] text-muted-foreground/70">Sources retrieved during research will appear here grouped by response.</p>
          </div>
        ) : (
          groups.map((group) => {
            const isExpanded = expandedGroups[group.id] !== false; // default true
            const isTargeted = targetResponseIndex === group.responseIndex;

            return (
              <div
                key={group.id}
                id={`source-group-${group.responseIndex}`}
                className={cn(
                  'rounded-xl border transition-all duration-200 overflow-hidden',
                  isTargeted
                    ? 'border-accent/40 bg-accent/5 shadow-xs'
                    : 'border-border-subtle/70 bg-surface-hover/40 hover:border-border-subtle'
                )}
              >
                {/* Group Accordion Header */}
                <button
                  type="button"
                  onClick={() => toggleGroup(group.id)}
                  className="w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-foreground hover:bg-surface-hover/80 transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-2 truncate">
                    <Layers className="w-3.5 h-3.5 text-accent shrink-0" />
                    <span className="font-semibold text-white truncate">{group.title}</span>
                    <span className="text-[10px] text-muted-foreground bg-surface-elevated/80 px-1.5 py-0.5 rounded-md border border-border-subtle/50 shrink-0">
                      {group.sources.length} {group.sources.length === 1 ? 'source' : 'sources'}
                    </span>
                  </div>
                  {isExpanded ? (
                    <ChevronUp className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                  )}
                </button>

                {/* Group Sources List */}
                {isExpanded && (
                  <div className="p-2 pt-0 space-y-2 border-t border-border-subtle/40 bg-surface/40">
                    {group.sources.length === 0 ? (
                      <p className="py-2 text-[11px] text-muted-foreground text-center italic">
                        No web evidence cited for this response.
                      </p>
                    ) : (
                      group.sources.map((item, idx) => {
                        const globalCardNum = idx + 1;
                        const isHighlighted = highlightedSourceNumber === globalCardNum;
                        const rawDomain = item.domain || 'source';
                        const cleanDomain = rawDomain.replace(/^https?:\/\//, '').replace(/\/.*$/, '');
                        const targetUrl = item.url || (item.domain.startsWith('http') ? item.domain : `https://${item.domain}`);
                        const displayTitle = item.title || `${cleanDomain} - Information & Evidence Reference`;
                        const displaySnippet = item.snippet || `Explore evidence and research findings from ${cleanDomain}.`;

                        return (
                          <a
                            id={`source-card-${globalCardNum}`}
                            key={`${group.id}-${idx}`}
                            href={targetUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={cn(
                              'block p-2.5 rounded-lg border transition-all duration-200 space-y-1 group/card cursor-pointer',
                              isHighlighted
                                ? 'bg-surface-elevated border-accent/60 ring-2 ring-accent/20 shadow-md'
                                : 'bg-surface/80 hover:bg-surface-elevated border-border-subtle/60 hover:border-white/20'
                            )}
                          >
                            {/* Favicon + Domain Header */}
                            <div className="flex items-center gap-1.5 text-[11px] font-medium text-muted-foreground group-hover/card:text-foreground">
                              <img
                                src={`https://www.google.com/s2/favicons?domain=${cleanDomain}&sz=32`}
                                alt=""
                                aria-hidden="true"
                                className="w-3.5 h-3.5 rounded-xs shrink-0 object-contain"
                                onError={(e) => {
                                  e.currentTarget.style.display = 'none';
                                }}
                              />
                              <span className="truncate">{cleanDomain}</span>
                              <ExternalLink className="w-3 h-3 ml-auto opacity-0 group-hover/card:opacity-100 transition-opacity duration-fast text-accent shrink-0" />
                            </div>

                            {/* Card Title */}
                            <h4 className="text-xs font-semibold text-white group-hover/card:text-accent leading-snug line-clamp-2 transition-colors duration-fast">
                              {displayTitle}
                            </h4>

                            {/* Card Snippet */}
                            <p className="text-[11px] text-muted-foreground/85 leading-relaxed line-clamp-2 font-light">
                              {displaySnippet}
                            </p>
                          </a>
                        );
                      })
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
