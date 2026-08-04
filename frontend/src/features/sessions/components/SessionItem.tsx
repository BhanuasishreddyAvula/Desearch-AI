import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { EllipsisVertical, Check, X } from 'lucide-react';
import { cn } from '@/lib/utils/cn';
import type { ResearchSession } from '../../../types';
import { useRenameSession } from '../hooks/useRenameSession';
import { useDeleteSession } from '../hooks/useDeleteSession';
import { SessionActionMenu } from './SessionActionMenu';
import { SessionDeleteDialog } from './SessionDeleteDialog';

interface SessionItemProps {
  session: ResearchSession;
  isCollapsed?: boolean;
}

export const SessionItem: React.FC<SessionItemProps> = ({ session, isCollapsed = false }) => {
  const navigate = useNavigate();
  const { sessionId: activeSessionId } = useParams<{ sessionId?: string }>();
  const isSelected = activeSessionId === session.id;

  const [isRenaming, setIsRenaming] = useState(false);
  const [renameTitle, setRenameTitle] = useState(session.title || session.query || '');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [menuAnchorRect, setMenuAnchorRect] = useState<DOMRect | null>(null);

  const renameMutation = useRenameSession();
  const deleteMutation = useDeleteSession();
  const inputRef = useRef<HTMLInputElement>(null);

  const displayTitle = session.title || session.query || 'Untitled Research';

  useEffect(() => {
    if (isRenaming) {
      inputRef.current?.focus();
      inputRef.current?.select();
    }
  }, [isRenaming]);

  const handleClick = () => {
    if (isRenaming || showDeleteConfirm) return;
    navigate(`/research/${session.id}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  const handleOpenMenu = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    e.preventDefault();
    const rect = e.currentTarget.getBoundingClientRect();
    setMenuAnchorRect(rect);
  };

  const handleSaveRename = async () => {
    const trimmed = renameTitle.trim();
    // Validation: empty or unchanged title must NOT issue PATCH
    if (!trimmed || trimmed === displayTitle || renameMutation.isPending) {
      setIsRenaming(false);
      setRenameTitle(displayTitle);
      return;
    }

    try {
      await renameMutation.mutateAsync({ sessionId: session.id, title: trimmed });
    } catch {
      setRenameTitle(displayTitle);
    } finally {
      setIsRenaming(false);
    }
  };

  const handleCancelRename = () => {
    setRenameTitle(displayTitle);
    setIsRenaming(false);
  };

  const handleConfirmDelete = async () => {
    if (deleteMutation.isPending) return;

    try {
      await deleteMutation.mutateAsync(session.id);
      setShowDeleteConfirm(false);

      // If deleting the currently active session, navigate to root /
      if (isSelected) {
        navigate('/', { replace: true });
      }
    } catch {
      setShowDeleteConfirm(false);
    }
  };

  if (isCollapsed) {
    return null; // Collapsed rail renders 0 history content
  }

  // Inline Rename Mode
  if (isRenaming) {
    return (
      <div className="flex items-center gap-1.5 h-8 px-2 rounded-md bg-surface-elevated border border-accent/60">
        <input
          ref={inputRef}
          type="text"
          value={renameTitle}
          onChange={(e) => setRenameTitle(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') handleSaveRename();
            if (e.key === 'Escape') handleCancelRename();
          }}
          disabled={renameMutation.isPending}
          className="w-full bg-transparent text-xs text-white focus:outline-none font-sans-ui"
          aria-label="Rename session"
        />
        <button
          type="button"
          onClick={handleSaveRename}
          disabled={renameMutation.isPending}
          aria-label="Save title"
          className="p-1 rounded text-emerald-400 hover:bg-surface transition-colors cursor-pointer"
        >
          <Check className="w-3.5 h-3.5" />
        </button>
        <button
          type="button"
          onClick={handleCancelRename}
          disabled={renameMutation.isPending}
          aria-label="Cancel rename"
          className="p-1 rounded text-muted-foreground hover:bg-surface transition-colors cursor-pointer"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    );
  }

  return (
    <>
      <div
        role="button"
        tabIndex={0}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        title={displayTitle}
        aria-label={`Open research session: ${displayTitle}`}
        className={cn(
          'w-full text-left h-8 px-2.5 rounded-md transition-[background-color,color] duration-200 ease-out text-[13px] font-medium font-sans-ui relative flex items-center justify-between gap-2 group cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring overflow-hidden select-none',
          isSelected
            ? 'bg-surface-elevated text-white'
            : 'text-foreground/80 hover:bg-surface-hover/60 hover:text-white'
        )}
      >
        <span className="truncate flex-1 leading-none">{displayTitle}</span>

        {/* Vertical Three-Dot Menu Button — Visible ONLY on item hover or when menu is active */}
        <button
          type="button"
          onClick={handleOpenMenu}
          aria-label={`Actions for ${displayTitle}`}
          title="Session actions"
          className={cn(
            'p-1 rounded text-muted-foreground hover:text-white transition-opacity duration-200 ease-out focus:outline-none shrink-0',
            menuAnchorRect ? 'opacity-100 text-white' : 'opacity-0 group-hover:opacity-100'
          )}
        >
          <EllipsisVertical className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Floating Action Menu (Portal) */}
      {menuAnchorRect && (
        <SessionActionMenu
          anchorRect={menuAnchorRect}
          onClose={() => setMenuAnchorRect(null)}
          onRename={() => setIsRenaming(true)}
          onDelete={() => setShowDeleteConfirm(true)}
        />
      )}

      {/* Compact Delete Confirmation Dialog (Portal) */}
      {showDeleteConfirm && (
        <SessionDeleteDialog
          sessionTitle={displayTitle}
          isPending={deleteMutation.isPending}
          onConfirm={handleConfirmDelete}
          onCancel={() => setShowDeleteConfirm(false)}
        />
      )}
    </>
  );
};
