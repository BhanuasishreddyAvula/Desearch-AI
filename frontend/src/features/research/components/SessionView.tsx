import React, { useEffect, useRef, useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { sessionsApi } from '@/lib/api/sessions';
import { conversationsApi } from '@/lib/api/conversations';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { useResearchProgress } from '../hooks/useResearchProgress';
import { ResearchProgress } from './ResearchProgress';
import { UserMessageBubble } from './UserMessageBubble';
import { ResearchComposer } from './ResearchComposer';
import { ReportSkeleton } from '../../reports';
import { FollowupResponseItem, FollowupMessagePair } from './FollowupResponseItem';
import { streamResearchProgress } from '@/lib/sse/reader';
import type { SseStreamControl } from '@/lib/sse/types';
import { createInitialProgressState, progressReducer } from '../progress/reducer';
import { extractCleanMarkdown, resolveSourcesForResponse } from '@/lib/utils/sources';
import type { ReportSource } from '../../../types';


export const SessionView: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const scrollRef = useRef<HTMLDivElement>(null);
  const streamControlRef = useRef<SseStreamControl | null>(null);

  // Extract explicit single-use executionToken navigation state
  const executionToken = (location.state as { executionToken?: string } | null)?.executionToken;

  // Follow-up messages state & active streaming state
  const [followupMessages, setFollowupMessages] = useState<FollowupMessagePair[]>([]);
  const [isFollowupStreaming, setIsFollowupStreaming] = useState(false);

  // Stop active workflow research generation
  // Pattern: POST /cancel to backend first (stops agents at next boundary),
  // then abort the SSE reader (closes the browser stream immediately).
  const handleStopGeneration = async () => {
    // 1. Signal the backend agents to stop (fire-and-forget, non-blocking)
    if (sessionId) {
      try {
        const { API_BASE_URL } = await import('@/lib/api/client');
        const { getDeviceId } = await import('@/lib/device');
        fetch(`${API_BASE_URL}/api/v1/orchestrator/cancel`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Device-ID': getDeviceId(),
          },
          body: JSON.stringify({ session_id: sessionId }),
        }).catch(() => {}); // silent — if no active run it's fine
      } catch {
        // Silent — frontend still closes stream
      }
    }

    // 2. Immediately close the SSE stream from the browser side
    if (streamControlRef.current) {
      streamControlRef.current.abort();
      streamControlRef.current = null;
    }

    // 3. Update UI state — mark as 'cancelled' (not 'completed') to show clean stopped message
    setIsFollowupStreaming(false);
    setFollowupMessages((prev) =>
      prev.map((msg) =>
        msg.status === 'streaming'
          ? {
              ...msg,
              status: 'cancelled' as const,
              assistantContent: '',
            }
          : msg
      )
    );
  };


  // ─── UNIVERSAL SESSION ISOLATION ──────────────────────────────────────────
  // Reset all session-local state whenever sessionId changes.
  // This prevents follow-up messages from a previous session bleeding into
  // the newly opened session when React reuses the same component instance.
  useEffect(() => {
    setFollowupMessages([]);
    setIsFollowupStreaming(false);
  }, [sessionId]);

  // Clear executionToken from history state after reading
  useEffect(() => {
    if (executionToken) {
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [executionToken, location.pathname, navigate]);


  // React Query session fetching with 5-minute instant client cache & hydration
  const { data: session, isLoading, isError, refetch } = useQuery({
    queryKey: ['session', sessionId],
    queryFn: ({ signal }) => sessionsApi.getSession(sessionId!, signal),
    enabled: Boolean(sessionId),
    staleTime: 1000 * 60 * 5, // 5 minutes instant client cache
    gcTime: 1000 * 60 * 15,    // 15 minutes garbage collection
  });

  const { progressState, isStreaming: isQ1Streaming, stopQ1Stream } = useResearchProgress(session, { executionToken });

  // Unified streaming state: true when either Q1 or any follow-up is running
  const isAnyStreaming = isQ1Streaming || isFollowupStreaming;

  // Unified stop: covers both Q1 initial stream and Q2+ follow-up streams
  const handleUnifiedStop = async () => {
    if (isQ1Streaming) {
      await stopQ1Stream();
    }
    if (isFollowupStreaming) {
      await handleStopGeneration();
    }
  };


  // ─── Load persisted conversation messages from backend (replaces session.metadata.messages) ─
  const { data: persistedMessages } = useQuery({
    queryKey: ['conversation-messages', sessionId],
    queryFn: ({ signal }) => conversationsApi.listMessages(sessionId!, signal),
    enabled: Boolean(sessionId) && !isLoading,
    staleTime: 1000 * 30,  // 30s — backend is source of truth
    gcTime: 1000 * 60 * 10,
  });

  // Hydrate followupMessages from persisted backend messages with strict deduplication
  useEffect(() => {
    if (!persistedMessages || persistedMessages.length === 0) return;

    // Build FollowupMessagePair[] with strict deduplication by pair_id & normalized user query
    const uniquePairsMap = new Map<string, FollowupMessagePair>();

    for (let i = 0; i < persistedMessages.length; i += 2) {
      const uMsg = persistedMessages[i];
      const aMsg = persistedMessages[i + 1];
      if (!uMsg || uMsg.role !== 'user') continue;

      const pairId = uMsg.metadata?.pair_id || uMsg.id;
      const rawContent = aMsg?.metadata?.full_markdown || aMsg?.content || '';
      const cleanContent = extractCleanMarkdown(rawContent);

      const sourcesRaw = aMsg?.metadata?.sources_cited || aMsg?.sources || [];
      const sources: ReportSource[] = resolveSourcesForResponse(
        Array.isArray(sourcesRaw) ? sourcesRaw : [],
        cleanContent
      );

      const execTime = aMsg?.metadata?.total_execution_time_ms;
      const initProgState = createInitialProgressState(pairId, 'completed');
      if (typeof execTime === 'number') {
        initProgState.totalExecutionTimeMs = execTime;
      }

      const pairItem: FollowupMessagePair = {
        id: pairId,
        userQuery: uMsg.content,
        assistantContent: cleanContent,
        status: 'completed',
        progressState: initProgState,
        sources,
        createdAt: uMsg.created_at,
      };

      // Key by pairId or normalized user query so duplicates collapse into the latest clean response
      const dedupKey = pairId || uMsg.content.trim().toLowerCase();
      uniquePairsMap.set(dedupKey, pairItem);
    }

    const pairs = Array.from(uniquePairsMap.values());
    if (pairs.length === 0) return;

    setFollowupMessages((prev) => {
      if (prev.length === 0) return pairs;

      // Merge: keep in-flight streaming pairs, update completed ones from backend
      const backendIds = new Set(pairs.map((p) => p.id));
      const backendQueries = new Set(pairs.map((p) => p.userQuery.trim().toLowerCase()));

      const unsyncedLocalPairs = prev.filter(
        (p) => p.status === 'streaming' || (!backendIds.has(p.id) && !backendQueries.has(p.userQuery.trim().toLowerCase()))
      );

      const updatedPairs = pairs.map((bPair) => {
        const localMatch = prev.find((p) => p.id === bPair.id || p.userQuery.trim().toLowerCase() === bPair.userQuery.trim().toLowerCase());
        if (!localMatch) return bPair;
        return {
          ...bPair,
          assistantContent: bPair.assistantContent || localMatch.assistantContent,
          sources: (bPair.sources && bPair.sources.length > 0)
            ? bPair.sources
            : (localMatch.sources && localMatch.sources.length > 0 ? localMatch.sources : []),
        };
      });

      // Deduplicate merged list strictly
      const finalMap = new Map<string, FollowupMessagePair>();
      [...updatedPairs, ...unsyncedLocalPairs].forEach((item) => {
        finalMap.set(item.id || item.userQuery.trim().toLowerCase(), item);
      });

      return Array.from(finalMap.values());
    });
  }, [persistedMessages]);



  // Restore saved scroll position per session
  useEffect(() => {
    if (!sessionId || isLoading || !scrollRef.current) return;

    try {
      const savedPos = sessionStorage.getItem(`scroll_pos_${sessionId}`);
      if (savedPos) {
        const pos = parseInt(savedPos, 10);
        if (!isNaN(pos) && pos > 0) {
          scrollRef.current.scrollTop = pos;
        }
      }
    } catch {
      // Fallback
    }
  }, [sessionId, isLoading]);

  // Save scroll position on scroll
  const handleScroll = () => {
    if (sessionId && scrollRef.current) {
      try {
        sessionStorage.setItem(`scroll_pos_${sessionId}`, String(scrollRef.current.scrollTop));
      } catch {
        // Fallback
      }
    }
  };

  // Render Skeleton Placeholders while fetching session data
  if (isLoading) {
    return (
      <div className="relative flex flex-col h-full w-full overflow-hidden font-sans-ui animate-in fade-in duration-200">
        <div className="flex-1 overflow-y-auto px-4 md:px-6 pt-16 md:pt-20 pb-4">
          <div className="max-w-[760px] mx-auto min-h-full flex flex-col justify-between space-y-8">
            <div className="space-y-8">
              <div className="flex justify-end">
                <div className="h-10 w-2/3 bg-surface-hover/80 rounded-2xl animate-pulse" />
              </div>
              <ReportSkeleton />
            </div>
            <div className="sticky bottom-3.5 z-30 pointer-events-none pt-4">
              <ResearchComposer initialValue="" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Error Recovery UI with lightweight Retry action
  if (isError || !session) {
    return (
      <div className="max-w-md mx-auto my-20 p-8 rounded-2xl bg-surface border border-border text-center space-y-4 font-sans-ui shadow-sm animate-in fade-in duration-200">
        <AlertCircle className="w-10 h-10 text-destructive mx-auto" />
        <h2 className="text-lg font-medium text-foreground">Session Not Found</h2>
        <p className="text-xs md:text-sm text-muted-foreground leading-relaxed">
          The requested research session could not be retrieved from the server.
        </p>
        <button
          type="button"
          onClick={() => refetch()}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-accent text-white text-xs font-medium hover:bg-accent-hover transition-colors cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry</span>
        </button>
      </div>
    );
  }

  const promptText = session.query || session.title || 'Research Question';

  // Extract markdown content from primary research report
  const getMarkdownContent = (): string => {
    if (!session || !session.metadata) return '';
    try {
      let meta: any = session.metadata;
      if (typeof meta === 'string') {
        meta = JSON.parse(meta);
      }
      const reportResult = meta.report_result || meta.reportResult || meta;
      if (!reportResult) return '';
      if (typeof reportResult === 'string') {
        const parsed = JSON.parse(reportResult);
        return parsed.full_markdown || parsed.fullMarkdown || parsed.content || '';
      }
      return reportResult.full_markdown || reportResult.fullMarkdown || reportResult.content || '';
    } catch {
      return '';
    }
  };

  // Extract explicit sources array from primary research report metadata
  const getReportSources = (): any[] => {
    if (!session || !session.metadata) return [];
    try {
      let meta: any = session.metadata;
      if (typeof meta === 'string') meta = JSON.parse(meta);
      const reportResult = meta.report_result || meta.reportResult;
      if (reportResult) {
        if (typeof reportResult === 'string') {
          const parsed = JSON.parse(reportResult);
          return parsed.sources_cited || parsed.sources || [];
        }
        return reportResult.sources_cited || reportResult.sources || [];
      }
      return meta.sources_cited || meta.sources || [];
    } catch {
      return [];
    }
  };

  const markdownContent = getMarkdownContent();
  const reportSources = getReportSources();


  // Handle Question Submission / Re-execution (Supports unlimited sequential questions and in-place turn edits)
  const handleFollowupSubmit = async (queryText: string, targetPairId?: string) => {
    if (!sessionId || isFollowupStreaming) return;

    let pairId = targetPairId;
    let targetTurnIndex: number | undefined = undefined;

    if (pairId) {
      targetTurnIndex = followupMessages.findIndex((msg) => msg.id === pairId);
      if (targetTurnIndex < 0) targetTurnIndex = 0;

      // Re-execute / Edit existing turn in place (Truncate downstream turns like ChatGPT/Claude)
      setFollowupMessages((prev) => {
        const targetIndex = prev.findIndex((msg) => msg.id === pairId);
        if (targetIndex >= 0) {
          const truncated = prev.slice(0, targetIndex + 1);
          return truncated.map((msg, idx) =>
            idx === targetIndex
              ? {
                  ...msg,
                  userQuery: queryText,
                  assistantContent: '',
                  status: 'streaming' as const,
                  progressState: createInitialProgressState(pairId!, 'streaming'),
                  sources: [],
                }
              : msg
          );
        }
        return prev;
      });
    } else {
      // Append new turn for fresh follow-up query
      pairId = `pair-${Date.now()}`;
      const newPair: FollowupMessagePair = {
        id: pairId,
        userQuery: queryText,
        assistantContent: '',
        status: 'streaming',
        progressState: createInitialProgressState(pairId, 'streaming'),
        createdAt: new Date().toISOString(),
      };
      setFollowupMessages((prev) => [...prev, newPair]);
    }

    setIsFollowupStreaming(true);
    window.dispatchEvent(new CustomEvent('session-sources-clear'));

    // 2. Smoothly scroll to target message
    setTimeout(() => {
      if (scrollRef.current) {
        scrollRef.current.scrollTo({
          top: scrollRef.current.scrollHeight,
          behavior: 'smooth',
        });
      }
    }, 100);

    let accumulatedContent = '';
    let streamSources: ReportSource[] = [];

    // 3. Initiate SSE stream for query
    streamControlRef.current = streamResearchProgress({
      url: '/api/v1/orchestrator/stream',
      body: {
        session_id: sessionId,
        query: queryText,
        target_message_id: targetPairId,
        turn_index: targetTurnIndex,
      },
      onEvent: (event) => {
        const payload = (event as any).metadata || (event as any).data;
        if (payload) {
          const extractedMd = extractCleanMarkdown(payload);
          if (extractedMd && extractedMd.length > accumulatedContent.length) {
            accumulatedContent = extractedMd;
          }

          const reportResult = payload.report_result || payload.reportResult || payload;
          const rawSources =
            reportResult?.sources_cited ||
            reportResult?.sources ||
            payload.sources_cited ||
            payload.sources;
          if (Array.isArray(rawSources) && rawSources.length > 0) {
            streamSources = rawSources as ReportSource[];
          }
        }

        // Update React state with extracted markdown
        setFollowupMessages((prev) =>
          prev.map((msg) => {
            if (msg.id !== pairId) return msg;
            const nextProgressState = progressReducer(msg.progressState, { type: 'EVENT_RECEIVED', event });
            return {
              ...msg,
              progressState: nextProgressState,
              assistantContent: accumulatedContent || msg.assistantContent,
              sources: streamSources.length > 0 ? streamSources : msg.sources,
            };
          })
        );

        if (streamSources.length > 0) {
          const sourceItems = streamSources
            .map((s) => {
              let d = s.domain || s.url || '';
              try {
                if (s.url?.startsWith('http')) d = new URL(s.url).hostname.replace(/^www\./, '');
                else if (d.startsWith('http')) d = new URL(d).hostname.replace(/^www\./, '');
              } catch { /* keep raw */ }
              if (!d || d === 'source') return null;
              return {
                domain: d,
                url: s.url || `https://${d}`,
                title: s.title || `${d} - Research Reference Source`,
                snippet: s.snippet || `Evidence reference from ${d}.`,
                category: 'Official Documentation' as const,
                confidence: 'High' as const,
              };
            })
            .filter(Boolean);
          if (sourceItems.length > 0) {
            window.dispatchEvent(new CustomEvent('session-sources-update', { detail: { sources: sourceItems } }));
          }
        }

        if (scrollRef.current) {
          scrollRef.current.scrollTo({
            top: scrollRef.current.scrollHeight,
            behavior: 'smooth',
          });
        }
      },
      onComplete: async () => {
        streamControlRef.current = null;
        setIsFollowupStreaming(false);
        window.dispatchEvent(new CustomEvent('session-sources-clear'));


        setFollowupMessages((prev) => {
          const updated = prev.map((msg) =>
            msg.id === pairId
              ? {
                  ...msg,
                  status: 'completed' as const,
                  assistantContent: accumulatedContent || msg.assistantContent,
                  sources: streamSources.length > 0 ? streamSources : msg.sources,
                }
              : msg
          );
          return updated;
        });

        queryClient.invalidateQueries({ queryKey: ['conversation-messages', sessionId] });

        setTimeout(() => {
          if (scrollRef.current) {
            scrollRef.current.scrollTo({
              top: scrollRef.current.scrollHeight,
              behavior: 'smooth',
            });
          }
        }, 150);
      },
      onError: (err) => {
        streamControlRef.current = null;
        setIsFollowupStreaming(false);
        setFollowupMessages((prev) =>
          prev.map((msg) =>
            msg.id === pairId
              ? {
                  ...msg,
                  status: 'failed' as const,
                  assistantContent: msg.assistantContent || `Follow-up research failed: ${err.message}`,
                }
              : msg
          )
        );
      },
    });

  };

  return (
    <div className="relative flex flex-col h-full w-full overflow-hidden font-sans-ui animate-in fade-in duration-200">
      {/* Scrollable Conversation Timeline Canvas */}
      <div
        ref={scrollRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto px-4 md:px-6 pt-16 md:pt-20 pb-4 scroll-smooth"
      >
        <div className="max-w-[760px] mx-auto min-h-[calc(100vh-100px)] flex flex-col justify-between">
          <div className="space-y-6 md:space-y-8 pb-10">
            {/* Unified Conversation Timeline (Renders all Q&A turns in 1-based chronological order) */}
            {followupMessages.length > 0 ? (
              followupMessages.map((msgPair, idx) => (
                <FollowupResponseItem
                  key={msgPair.id}
                  message={msgPair}
                  queryTitle={session?.title || session?.query || 'Research Session'}
                  responseIndex={idx + 1}
                  onRetry={(qText) => handleFollowupSubmit(qText, msgPair.id)}
                  onEdit={(qText) => handleFollowupSubmit(qText, msgPair.id)}
                />
              ))
            ) : (
              <>
                {/* Initial Q1 User Query + Live Execution Progress (For brand-new active streaming) */}
                <UserMessageBubble
                  content={promptText}
                  onEdit={(qText) => handleFollowupSubmit(qText, followupMessages[0]?.id)}
                />
                <ResearchProgress
                  progressState={progressState}
                  queryTitle={session?.title || session?.query || 'Research Session'}
                  markdownContent={markdownContent}
                  sessionStatus={session?.status}
                  reportSources={reportSources}
                  onRetry={() => handleFollowupSubmit(promptText)}
                />

              </>
            )}




          </div>

          {/* 4. Pure Floating Sticky Composer for Follow-up Queries */}
          <div className="sticky bottom-2 z-20 pointer-events-none pt-2">
            <ResearchComposer
              onFollowup={handleFollowupSubmit}
              isFollowupSubmitting={isAnyStreaming}
              onStop={handleUnifiedStop}
            />
          </div>

        </div>
      </div>
    </div>
  );
};
