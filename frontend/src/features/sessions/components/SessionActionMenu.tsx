import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { SquarePen, Trash2 } from 'lucide-react';

interface SessionActionMenuProps {
  anchorRect: DOMRect;
  onClose: () => void;
  onRename: () => void;
  onDelete: () => void;
}

export const SessionActionMenu: React.FC<SessionActionMenuProps> = ({
  anchorRect,
  onClose,
  onRename,
  onDelete,
}) => {
  const menuRef = useRef<HTMLDivElement>(null);

  // Position ~4px to the right of sidebar/item, vertically aligned
  const topPos = Math.min(Math.max(anchorRect.top, 8), window.innerHeight - 100);
  const leftPos = anchorRect.right + 4;

  useEffect(() => {
    const handleMouseDown = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [onClose]);

  return createPortal(
    <div
      ref={menuRef}
      style={{ top: `${topPos}px`, left: `${leftPos}px` }}
      role="menu"
      aria-label="Session actions menu"
      className="fixed z-50 w-36 py-1.5 bg-surface border border-border-subtle rounded-lg shadow-xl font-sans-ui text-xs text-foreground animate-in fade-in zoom-in-95 duration-150 select-none"
    >
      <button
        type="button"
        role="menuitem"
        onClick={() => {
          onRename();
          onClose();
        }}
        className="w-full px-3 py-2 flex items-center gap-2.5 hover:bg-surface-hover text-foreground/90 hover:text-white transition-colors text-left font-medium"
      >
        <SquarePen className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
        <span>Rename</span>
      </button>
      <button
        type="button"
        role="menuitem"
        onClick={() => {
          onDelete();
          onClose();
        }}
        className="w-full px-3 py-2 flex items-center gap-2.5 hover:bg-destructive/10 text-destructive transition-colors text-left font-medium"
      >
        <Trash2 className="w-3.5 h-3.5 text-destructive shrink-0" />
        <span>Delete</span>
      </button>
    </div>,
    document.body
  );
};
