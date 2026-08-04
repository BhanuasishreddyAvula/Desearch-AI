import React, { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Globe, ChevronDown, ChevronUp, Download, Menu } from 'lucide-react';
import { sessionsApi } from '@/lib/api/sessions';
import { conversationsApi } from '@/lib/api/conversations';
import { SourcesDropdown, SourceItem, SourceGroup } from '../../features/reports/components/sources/SourcesDropdown';
import { ExportMenu } from '../../features/reports/components/export/ExportMenu';
import { resolveSourcesForResponse } from '@/lib/utils/sources';
import { cn } from '@/lib/utils/cn';



export const FloatingHeaderActions: React.FC = () => {
  const [isSourcesOpen, setIsSourcesOpen] = useState(false);
  const [isExportOpen, setIsExportOpen] = useState(false);
  const [highlightedSourceNumber, setHighlightedSourceNumber] = useState<number | undefined>(undefined);
  const [targetResponseIndex, setTargetResponseIndex] = useState<number | undefined>(undefined);

  // In-flight accumulated sources pushed real-time during active streaming
  const [accumulatedSources, setAccumulatedSources] = useState<SourceItem[]>([]);

  const sourcesContainerRef = useRef<HTMLDivElement>(null);
  const exportContainerRef = useRef<HTMLDivElement>(null);

  const { sessionId } = useParams<{ sessionId?: string }>();
  const queryClient = useQueryClient();

  // Fetch active session if viewing a research session
  const { data: session } = useQuery({
    queryKey: ['session', sessionId],
    queryFn: ({ signal }) => sessionsApi.getSession(sessionId!, signal),
    enabled: Boolean(sessionId),
  });

  // Actively query conversation messages from backend/Supabase for real-time source calculation
  const { data: convMsgs } = useQuery({
    queryKey: ['conversation-messages', sessionId],
    queryFn: ({ signal }) => conversationsApi.listMessages(sessionId!, signal),
    enabled: Boolean(sessionId),
    staleTime: 1000 * 30,
  });


  // Reset local state when navigating to a different session
  useEffect(() => {
    setAccumulatedSources([]);
    setTargetResponseIndex(undefined);
  }, [sessionId]);

  // Listen for open-sources-popover custom events emitted by inline CitationBadges or Response Action Bars
  useEffect(() => {
    const handleOpenSources = (e: Event) => {
      const customEvent = e as CustomEvent<{ responseIndex?: number; sourceNumber?: number; domain?: string }>;
      if (customEvent.detail) {
        setIsSourcesOpen(true);
        setIsExportOpen(false);
        if (customEvent.detail.responseIndex) {
          setTargetResponseIndex(customEvent.detail.responseIndex);
        }
        if (customEvent.detail.sourceNumber) {
          setHighlightedSourceNumber(customEvent.detail.sourceNumber);
        }
      }
    };

    window.addEventListener('open-sources-popover', handleOpenSources);
    return () => window.removeEventListener('open-sources-popover', handleOpenSources);
  }, []);

  // Listen for real-time follow-up sources pushed by SessionView on active Q&A streaming
  useEffect(() => {
    const handleSourcesUpdate = (e: Event) => {
      const { sources: newSources } = (e as CustomEvent<{ sources: SourceItem[] }>).detail || {};
      if (!Array.isArray(newSources) || newSources.length === 0) return;

      setAccumulatedSources((prev) => {
        const merged = new Map<string, SourceItem>(prev.map((s) => [s.domain, s]));
        newSources.forEach((s) => {
          if (s.domain && s.domain !== 'source' && !merged.has(s.domain)) {
            merged.set(s.domain, s);
          }
        });
        return Array.from(merged.values());
      });
    };

    const handleSourcesClear = () => {
      setAccumulatedSources([]);
    };

    window.addEventListener('session-sources-update', handleSourcesUpdate);
    window.addEventListener('session-sources-clear', handleSourcesClear);
    return () => {
      window.removeEventListener('session-sources-update', handleSourcesUpdate);
      window.removeEventListener('session-sources-clear', handleSourcesClear);
    };
  }, []);

  // Clear live stream accumulated sources buffer when persisted conversation messages update
  useEffect(() => {
    if (convMsgs && convMsgs.length > 0) {
      setAccumulatedSources([]);
    }
  }, [convMsgs]);


  // Close dropdowns when clicking outside their container or hitting Escape
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (sourcesContainerRef.current && !sourcesContainerRef.current.contains(e.target as Node)) {
        setIsSourcesOpen(false);
      }
      if (exportContainerRef.current && !exportContainerRef.current.contains(e.target as Node)) {
        setIsExportOpen(false);
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsSourcesOpen(false);
        setIsExportOpen(false);
      }
    };

    if (isSourcesOpen || isExportOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isSourcesOpen, isExportOpen]);

  const isSessionActive = Boolean(sessionId);

  // Construct SourceGroup[] grouped chronologically by Assistant Response Turn
  const getSourceGroups = (): SourceGroup[] => {
    if (!session || !session.metadata) return [];

    try {
      let meta: any = session.metadata;
      if (typeof meta === 'string') meta = JSON.parse(meta);

      const groups: SourceGroup[] = [];

      const normalizeItem = (item: any): SourceItem | null => {
        if (!item) return null;
        let domainStr = '';
        let urlStr = '';
        let title = '';
        let snippet = '';

        if (typeof item === 'string') {
          urlStr = item.startsWith('http') ? item : `https://${item}`;
          try { domainStr = new URL(urlStr).hostname.replace(/^www\./, ''); } catch { domainStr = item; }
          title = `${domainStr} - Research Reference Source`;
          snippet = `Cited evidence extracted from ${domainStr} for this report.`;
        } else if (typeof item === 'object') {
          urlStr = item.url || '';
          domainStr = item.domain || '';
          try {
            if (urlStr.startsWith('http')) domainStr = new URL(urlStr).hostname.replace(/^www\./, '');
            else if (domainStr.startsWith('http')) domainStr = new URL(domainStr).hostname.replace(/^www\./, '');
          } catch { /* keep raw */ }
          if (!urlStr && domainStr) urlStr = `https://${domainStr}`;
          title = item.title || `${domainStr} - Research Reference Source`;
          snippet = item.snippet || item.description || `Evidence reference from ${domainStr}.`;
        }

        if (!domainStr || domainStr === 'source' || domainStr === 'null' || domainStr === 'undefined') return null;
        return {
          domain: domainStr,
          url: urlStr || `https://${domainStr}`,
          title,
          snippet,
          category: domainStr.includes('github') ? 'GitHub' : 'Official Documentation',
          confidence: 'High',
        };
      };

      const deduplicateInGroup = (items: any[]): SourceItem[] => {
        const unique = new Map<string, SourceItem>();
        items.forEach((it) => {
          const norm = normalizeItem(it);
          if (norm && !unique.has(norm.domain)) {
            unique.set(norm.domain, norm);
          }
        });
        return Array.from(unique.values());
      };

      // 1. Fetch assistant messages from conversation-messages query (hydrated directly from backend/Supabase)
      const assistantMsgs = Array.isArray(convMsgs)
        ? convMsgs.filter((m) => m.role === 'assistant')
        : [];

      if (assistantMsgs.length > 0) {
        // Build one SourceGroup per assistant message turn in exact 1-based chronological order
        assistantMsgs.forEach((msg, idx) => {
          const respIdx = idx + 1; // Response 1, Response 2, Response 3...
          const rawSecs = msg.metadata?.sources_cited || msg.sources || [];
          const msgMd = msg.metadata?.full_markdown || msg.content || '';
          const groupSources = resolveSourcesForResponse(
            Array.isArray(rawSecs) ? rawSecs : [],
            msgMd,
            msg.metadata?.timeline_sources || msg.metadata?.timelineSources || accumulatedSources
          );

          groups.push({
            id: `response-${respIdx}`,
            title: `Response ${respIdx}`,
            responseIndex: respIdx,
            sources: groupSources,
          });
        });
      } else {
        // Fallback (for fresh session before conversation-messages query resolves):
        // Build Response 1 from session.metadata.report_result
        const reportResult = meta.report_result || meta.reportResult;
        const primaryRawSources =
          reportResult?.sources_cited || reportResult?.sources ||
          meta.sources || meta.sources_cited || [];
        const primaryFullMd = reportResult?.full_markdown || meta?.full_markdown || '';

        const primarySources = resolveSourcesForResponse(
          Array.isArray(primaryRawSources) ? primaryRawSources : [],
          primaryFullMd,
          accumulatedSources
        );

        if (primarySources.length > 0 || primaryFullMd) {
          groups.push({
            id: 'response-1',
            title: 'Response 1',
            responseIndex: 1,
            sources: primarySources,
          });
        }
      }




      // ── Real-time Streaming Response Sources (if active) ──
      if (accumulatedSources.length > 0) {
        const activeRespIdx = groups.length + 1;
        const streamingSources = deduplicateInGroup(accumulatedSources);
        groups.push({
          id: `response-${activeRespIdx}`,
          title: `Response ${activeRespIdx} (Live Stream)`,
          responseIndex: activeRespIdx,
          sources: streamingSources,
        });
      }

      return groups;
    } catch {
      return [];
    }
  };

  // Extract Markdown content for export
  const getExportMarkdown = (): string => {
    if (!session || !session.metadata) return '';
    try {
      let meta: any = session.metadata;
      if (typeof meta === 'string') meta = JSON.parse(meta);

      const reportResult = meta.report_result || meta.reportResult || meta;
      let primaryMd = reportResult?.full_markdown || reportResult?.fullMarkdown || meta?.full_markdown || '';

      const convMsgs = queryClient.getQueryData<any[]>(['conversation-messages', sessionId]);
      if (Array.isArray(convMsgs) && convMsgs.length > 0) {
        let followupMd = '\n\n## Follow-up Research Conversation\n\n';
        convMsgs.forEach((msg: any) => {
          if (msg.role === 'user') {
            followupMd += `### User Query\n${msg.content}\n\n`;
          } else if (msg.role === 'assistant') {
            followupMd += `### Assistant Answer\n${msg.metadata?.full_markdown || msg.content}\n\n`;
          }
        });
        primaryMd += followupMd;
      }

      return primaryMd;
    } catch {
      return '';
    }
  };

  const sourceGroups = getSourceGroups();
  const totalSourcesCount = sourceGroups.reduce((acc, g) => acc + g.sources.length, 0);

  // Flattened source list for Export menu
  const allSourcesList: SourceItem[] = sourceGroups.flatMap((g) => g.sources);
  const exportMarkdown = getExportMarkdown();

  return (
    <div className="pointer-events-none fixed md:absolute top-0 left-0 right-0 h-16 pt-3 px-4 md:px-8 md:top-4 flex items-start justify-between z-30 select-none bg-gradient-to-b from-background via-background/40 to-transparent border-none shadow-none md:bg-none">
      {/* 1. Top-Left Mobile 3-Line Sidebar Trigger Button (Normal Button) */}
      <button
        type="button"
        onClick={() => window.dispatchEvent(new CustomEvent('toggle-mobile-sidebar'))}
        aria-label="Toggle navigation sidebar"
        title="Open navigation menu"
        className="flex items-center justify-center w-9 h-9 rounded-full bg-surface hover:bg-surface-hover border border-border-subtle text-white shadow-sm cursor-pointer pointer-events-auto md:hidden"
      >
        <Menu className="w-5 h-5 text-white" />
      </button>

      <div className="hidden md:block" />

      {/* 2. Top-Right Floating Action Bar */}
      {isSessionActive && (
        <div className="pointer-events-auto flex items-center gap-2">
          {/* Download / Export Button */}
          <div ref={exportContainerRef} className="relative">
            <button
              type="button"
              onClick={() => {
                setIsExportOpen((prev) => !prev);
                setIsSourcesOpen(false);
              }}
              aria-expanded={isExportOpen}
              aria-label="Export report menu"
              title={isExportOpen ? 'Collapse Export Menu' : 'Download & Export Report'}
              className={cn(
                'flex items-center justify-center w-9 h-9 rounded-full transition-all duration-200 focus:outline-none cursor-pointer select-none animate-in fade-in duration-150',
                isExportOpen
                  ? 'bg-surface-hover border border-white/30 text-white'
                  : 'bg-surface hover:bg-surface-hover border border-border-subtle text-white shadow-sm'
              )}
            >
              <Download className="w-4 h-4 text-white" />
            </button>

            {/* Export Action Menu Popover */}
            {isExportOpen && (
              <ExportMenu
                markdownContent={exportMarkdown}
                title={session?.title || session?.query || 'Research Report'}
                sources={allSourcesList}
                onClose={() => setIsExportOpen(false)}
                position="bottom"
              />
            )}
          </div>

          {/* Sources Dropdown Button */}
          <div ref={sourcesContainerRef} className="relative">
            {/* Desktop View Button (Full Text) */}
            <button
              type="button"
              onClick={() => {
                setIsSourcesOpen((prev) => !prev);
                setIsExportOpen(false);
                setTargetResponseIndex(undefined);
              }}
              aria-expanded={isSourcesOpen}
              aria-label="Sources dropdown"
              title={isSourcesOpen ? 'Collapse Sources' : 'Expand Sources'}
              className={cn(
                'hidden md:flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-medium transition-all duration-200 focus:outline-none focus:ring-0 shadow-md cursor-pointer select-none animate-in fade-in duration-150',
                isSourcesOpen
                  ? 'bg-surface-hover border border-white/30 text-white'
                  : 'bg-surface hover:bg-surface-hover border border-border-subtle text-foreground/90 hover:text-white'
              )}
            >
              <span>Sources ({totalSourcesCount})</span>
              {isSourcesOpen ? (
                <ChevronUp className="w-3.5 h-3.5 text-muted-foreground" />
              ) : (
                <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
              )}
            </button>

            {/* Mobile View Button (Normal Solid Button) */}
            <button
              type="button"
              onClick={() => {
                setIsSourcesOpen((prev) => !prev);
                setIsExportOpen(false);
                setTargetResponseIndex(undefined);
              }}
              aria-expanded={isSourcesOpen}
              aria-label="Sources dropdown"
              title={isSourcesOpen ? 'Collapse Sources' : 'Expand Sources'}
              className={cn(
                'flex md:hidden items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 focus:outline-none cursor-pointer select-none animate-in fade-in duration-150',
                isSourcesOpen
                  ? 'bg-surface-hover border border-white/30 text-white'
                  : 'bg-surface hover:bg-surface-hover border border-border-subtle text-white shadow-sm'
              )}
            >
              <Globe className="w-4 h-4 text-white shrink-0" />
              <span className="text-[11px] font-bold text-white leading-none">({totalSourcesCount})</span>
              {isSourcesOpen ? (
                <ChevronUp className="w-3 h-3 text-muted-foreground" />
              ) : (
                <ChevronDown className="w-3 h-3 text-muted-foreground" />
              )}
            </button>

            {/* Sources Dropdown Popover */}
            <SourcesDropdown
              groups={sourceGroups}
              isOpen={isSourcesOpen}
              targetResponseIndex={targetResponseIndex}
              highlightedSourceNumber={highlightedSourceNumber}
            />
          </div>
        </div>
      )}
    </div>
  );
};
