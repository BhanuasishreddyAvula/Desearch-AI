import React from 'react';
import { UserMessageBubble } from './UserMessageBubble';
import { ResearchExecutionTimeline } from './timeline/ResearchExecutionTimeline';
import { MarkdownRenderer } from '../../reports/components/markdown/MarkdownRenderer';
import { ReportActionBar } from '../../reports/components/ReportActionBar';
import { resolveSourcesForResponse, extractCleanMarkdown } from '@/lib/utils/sources';
import type { ProgressState } from '../progress/types';

import type { ReportSource } from '../../../types';

export interface FollowupMessagePair {
  id: string;
  userQuery: string;
  assistantContent: string;
  progressState: ProgressState;
  status: 'streaming' | 'completed' | 'cancelled' | 'failed';
  sources?: ReportSource[];
  createdAt?: string;
}

interface FollowupResponseItemProps {
  message: FollowupMessagePair;
  queryTitle: string;
  responseIndex: number; // 1-based index (2 for first follow-up, 3 for second, etc.)
  onRetry?: (queryText: string) => void;
  onEdit?: (newQueryText: string) => void;
}

export const FollowupResponseItem: React.FC<FollowupResponseItemProps> = ({
  message,
  queryTitle,
  responseIndex,
  onRetry,
  onEdit,
}) => {
  const isCompleted = (message.status === 'completed' || Boolean(message.assistantContent && message.status !== 'failed')) && message.status !== 'cancelled';
  const isFailed = message.status === 'failed';

  const handleEditSubmit = (newText: string) => {
    if (onEdit) {
      onEdit(newText);
    } else if (onRetry) {
      onRetry(newText);
    }
  };

  return (
    <div className="space-y-6 md:space-y-8 pt-4 border-t border-border-subtle/30 animate-in fade-in duration-300">
      {/* 1. User Follow-up Question Bubble */}
      <UserMessageBubble content={message.userQuery} onEdit={handleEditSubmit} />

      {/* 2. Cancelled: show clean body text message without dot — no timeline, sources, or export */}
      {message.status === 'cancelled' ? (
        <p className="text-sm md:text-base text-white/80 font-sans-ui leading-relaxed py-1 animate-in fade-in duration-200">
          Research stopped by user.
        </p>
      ) : (

        /* 3. Active / Completed / Failed Response Block */
        <div className="space-y-4 font-sans-ui text-left">
          {/* Follow-up Workflow Execution Timeline */}
          <ResearchExecutionTimeline
            progressState={message.progressState}
            isCompletedOverride={isCompleted}
            sourcesOverride={message.sources}
          />

          {/* Failed State UI with Retry Action */}
          {isFailed && (
            <div className="p-4 rounded-2xl bg-destructive/10 border border-destructive/30 text-destructive text-xs md:text-sm space-y-2 font-sans-ui animate-in fade-in duration-200">
              <p className="font-medium flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
                <span>Research connection issue encountered.</span>
              </p>
              <p className="text-[12px] opacity-80 leading-relaxed">
                {message.assistantContent || 'Network communication with OpenRouter API was interrupted.'}
              </p>
              {onRetry && (
                <button
                  type="button"
                  onClick={() => onRetry(message.userQuery)}
                  className="mt-1 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-destructive/20 hover:bg-destructive/30 text-white text-xs font-semibold transition-colors cursor-pointer"
                >
                  <span>Retry Question</span>
                </button>
              )}
            </div>
          )}

          {/* Follow-up Streamed / Completed Markdown Response */}
          {!isFailed && message.assistantContent && (
            <div className="pt-2 text-foreground/90 space-y-4 transition-all duration-300 ease-out animate-in fade-in-50 slide-in-from-bottom-2">
              <MarkdownRenderer content={extractCleanMarkdown(message.assistantContent)} />

              {/* End-of-Response Action Bar (Sources & Export) */}
              <ReportActionBar
                title={queryTitle}
                fullMarkdown={extractCleanMarkdown(message.assistantContent)}
                sources={message.sources || []}
                responseIndex={responseIndex}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
};


