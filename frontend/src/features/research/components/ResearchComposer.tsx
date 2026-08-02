import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowUp, Loader2, AlertCircle, Square } from 'lucide-react';
import { cn } from '../../../lib/utils/cn';
import { useCreateResearchSession } from '../../sessions/hooks/useCreateResearchSession';
import { executionTokenRegistry } from '../utils/executionTokenRegistry';

interface ResearchComposerProps {
  initialValue?: string;
  onQueryChange?: (query: string) => void;
  onFollowup?: (query: string) => Promise<void> | void;
  isFollowupSubmitting?: boolean;
  onStop?: () => void;
}

export const ResearchComposer: React.FC<ResearchComposerProps> = ({
  initialValue = '',
  onQueryChange,
  onFollowup,
  isFollowupSubmitting = false,
  onStop,
}) => {

  const { sessionId } = useParams<{ sessionId?: string }>();
  const draftKey = `draft_query_${sessionId || 'new'}`;

  // Restore unsent text draft per session from localStorage
  const [query, setQuery] = useState(() => {
    try {
      const savedDraft = localStorage.getItem(draftKey);
      return savedDraft || initialValue;
    } catch {
      return initialValue;
    }
  });

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const navigate = useNavigate();

  const createSessionMutation = useCreateResearchSession();

  // Sync draft text on session switch
  useEffect(() => {
    try {
      const savedDraft = localStorage.getItem(draftKey);
      if (savedDraft) {
        setQuery(savedDraft);
      } else {
        setQuery(initialValue || '');
      }
    } catch {
      setQuery(initialValue || '');
    }
  }, [draftKey, initialValue]);

  // Automatic textarea height adjustment (min 48px, max 180px)
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      const newHeight = Math.min(Math.max(textarea.scrollHeight, 48), 180);
      textarea.style.height = `${newHeight}px`;
    }
  }, [query]);

  const trimmedQuery = query.trim();
  const isValid = trimmedQuery.length >= 3;
  const isSubmitting = createSessionMutation.isPending || isFollowupSubmitting;

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    setQuery(val);
    onQueryChange?.(val);
    try {
      if (val) {
        localStorage.setItem(draftKey, val);
      } else {
        localStorage.removeItem(draftKey);
      }
    } catch {
      // Silent fallback
    }
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();

    if (!isValid || isSubmitting) {
      return;
    }

    const q = trimmedQuery;

    // Immediately clear local state & localStorage draft upon submission
    setQuery('');
    onQueryChange?.('');
    try {
      localStorage.removeItem(draftKey);
    } catch {
      // Fallback
    }

    // Follow-up flow: invoke onFollowup directly without navigating away
    if (onFollowup) {
      try {
        await onFollowup(q);
      } catch {
        // Handled in parent
      } finally {
        // Enforce clean composer input reset after submission completes
        setQuery('');
        try {
          localStorage.removeItem(draftKey);
        } catch {
          // Fallback
        }
      }
      return;
    }


    // Initial query flow: create session and navigate
    try {
      const session = await createSessionMutation.mutateAsync({
        query: trimmedQuery,
        title: trimmedQuery,
      });

      // Generate explicit one-time execution token for newly created session
      const executionToken = executionTokenRegistry.createToken(session.id);

      // Pass executionToken to SessionView via router navigation state
      navigate(`/research/${session.id}`, { state: { executionToken } });
    } catch {
      // Error handled by mutation state
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-[760px] mx-auto space-y-2 font-sans-ui pointer-events-auto">
      {/* 106px Height Composer with Top Text Area & Bottom-Right Circular Send Button */}
      <div
        className={cn(
          'relative w-full rounded-2xl p-4 md:p-4.5 flex flex-col justify-between min-h-[106px]',
          'bg-surface/95 backdrop-blur-md border border-border-subtle/80',
          'hover:border-white/30 focus-within:border-white/60 transition-all duration-200',
          'shadow-[0_12px_40px_rgba(0,0,0,0.6)]'
        )}
      >
        {/* Multiline Textarea positioned at the TOP inside chat box */}
        <textarea
          ref={textareaRef}
          value={query}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          disabled={isSubmitting}
          placeholder="Ask a follow-up or research question..."
          aria-label="Research query prompt"
          rows={2}
          className="w-full bg-transparent text-white placeholder:text-muted-foreground/60 focus:placeholder:text-muted-foreground/40 text-sm md:text-base leading-relaxed resize-none focus:outline-none overflow-y-auto font-sans-ui pt-0 pr-12"
        />

        {/* Circular Send / Stop Button positioned at Bottom-Right Corner */}
        <div className="flex items-center justify-end shrink-0 pt-1">
          {isSubmitting && onStop ? (
            <button
              type="button"
              onClick={onStop}
              aria-label="Stop generation"
              title="Stop generation"
              className="group/btn w-8 h-8 rounded-full bg-accent hover:bg-accent-hover text-white flex items-center justify-center transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring cursor-pointer shadow-sm hover:scale-105 active:scale-95 select-none"
            >
              <Square className="w-3.5 h-3.5 fill-white text-white" />
            </button>
          ) : (
            <button
              type="submit"
              disabled={!isValid || isSubmitting}
              aria-label="Send query"
              title={isValid ? 'Send (Enter)' : 'Enter a question'}
              className={cn(
                'group/btn w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring select-none',
                isValid && !isSubmitting
                  ? 'bg-accent hover:bg-accent-hover text-white shadow-sm cursor-pointer hover:scale-105 active:scale-95'
                  : 'bg-accent/70 text-white/80 cursor-pointer hover:bg-accent/90'
              )}
            >
              {isSubmitting ? (
                <Loader2 className="w-4 h-4 animate-spin text-white" />
              ) : (
                <ArrowUp className="w-4 h-4 text-white stroke-[2.5] transition-transform duration-200 group-hover/btn:-translate-y-0.5" />
              )}
            </button>
          )}
        </div>
      </div>


      {/* Error Feedback */}
      {createSessionMutation.isError && (
        <div
          role="alert"
          aria-live="polite"
          className="p-3 rounded-xl bg-destructive/10 border border-destructive/30 text-destructive text-xs flex items-center justify-between gap-2 shadow-sm animate-in fade-in duration-200"
        >
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-destructive" />
            <span>
              {createSessionMutation.error?.message || "Couldn't create research session. Please try again."}
            </span>
          </div>
          <button
            type="button"
            onClick={() => handleSubmit()}
            className="text-[11px] font-medium text-foreground underline hover:no-underline"
          >
            Retry
          </button>
        </div>
      )}
    </form>
  );
};
