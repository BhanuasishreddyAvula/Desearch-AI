import React, { useState, useRef, useEffect } from 'react';
import { Copy, Check, Pencil } from 'lucide-react';

interface UserMessageBubbleProps {
  content: string;
  onEdit?: (newContent: string) => void;
  isEditingDisabled?: boolean;
}

export const UserMessageBubble: React.FC<UserMessageBubbleProps> = ({
  content,
  onEdit,
  isEditingDisabled = false,
}) => {
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(content);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Dynamically auto-resize textarea height based on text content length
  useEffect(() => {
    if (isEditing && textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 220)}px`;
    }
  }, [editText, isEditing]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      /* fallback */
    }
  };

  const handleStartEdit = () => {
    setEditText(content);
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditText(content);
  };

  const handleSaveEdit = () => {
    const trimmed = editText.trim();
    if (!trimmed) return;
    setIsEditing(false);
    if (trimmed !== content && onEdit) {
      onEdit(trimmed);
    }
  };

  return (
    <div className="flex flex-col items-end w-full select-none group">
      {/* 1. Main Question Bubble / Adaptive Auto-Resizing Inline Edit View */}
      {isEditing ? (
        <div className="w-full max-w-[92%] md:max-w-[70%] bg-surface-elevated text-foreground border border-border-subtle/80 px-4 py-3 rounded-2xl shadow-md space-y-2 font-sans-ui text-sm md:text-base leading-relaxed animate-in fade-in duration-150">
          <textarea
            ref={textareaRef}
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                handleSaveEdit();
              } else if (e.key === 'Escape') {
                handleCancelEdit();
              }
            }}
            rows={1}
            autoFocus
            className="w-full bg-transparent text-foreground text-sm md:text-base focus:outline-none resize-none custom-scrollbar leading-relaxed whitespace-pre-wrap break-words [word-break:break-word] min-h-[24px]"
            placeholder="Edit your question..."
          />
          <div className="flex items-center justify-end gap-2 pt-0.5">
            <button
              type="button"
              onClick={handleCancelEdit}
              className="px-3.5 py-1.5 rounded-full bg-surface-hover hover:bg-surface text-foreground text-xs md:text-sm font-medium transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSaveEdit}
              disabled={!editText.trim()}
              className="px-4 py-1.5 rounded-full bg-foreground text-background font-semibold hover:opacity-90 disabled:opacity-50 text-xs md:text-sm transition-opacity cursor-pointer shadow-xs"
            >
              Send
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="max-w-[92%] md:max-w-[70%] bg-surface-elevated text-foreground border border-border-subtle/80 px-4 py-3 rounded-2xl shadow-xs font-sans-ui text-sm md:text-base leading-relaxed whitespace-pre-wrap break-words [word-break:break-word] select-text">
            {content}
          </div>




          {/* 2. Action Icons (Copy & Edit) directly below the bubble */}
          <div className="flex items-center gap-1 mt-1 pr-1 opacity-70 group-hover:opacity-100 transition-opacity duration-150">
            {/* Copy Icon */}
            <button
              type="button"
              onClick={handleCopy}
              title="Copy question text"
              aria-label="Copy question text"
              className="p-1.5 rounded-lg hover:bg-surface-hover text-muted-foreground/80 hover:text-foreground transition-colors cursor-pointer"
            >
              {copied ? (
                <Check className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <Copy className="w-3.5 h-3.5" />
              )}
            </button>

            {/* Edit Icon */}
            {onEdit && !isEditingDisabled && (
              <button
                type="button"
                onClick={handleStartEdit}
                title="Edit question"
                aria-label="Edit question"
                className="p-1.5 rounded-lg hover:bg-surface-hover text-muted-foreground/80 hover:text-foreground transition-colors cursor-pointer"
              >
                <Pencil className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
};
