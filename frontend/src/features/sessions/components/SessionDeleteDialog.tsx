import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Loader2, Trash2 } from 'lucide-react';

interface SessionDeleteDialogProps {
  sessionTitle: string;
  isPending: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

export const SessionDeleteDialog: React.FC<SessionDeleteDialogProps> = ({
  sessionTitle,
  isPending,
  onConfirm,
  onCancel,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !isPending) {
        onCancel();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onCancel, isPending]);

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs font-sans-ui animate-in fade-in duration-150">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-dialog-title"
        className="w-full max-w-sm bg-surface border border-border-subtle rounded-2xl p-6 shadow-2xl space-y-5 animate-in zoom-in-95 duration-150 select-none text-left"
      >
        <div className="space-y-2">
          <h3 id="delete-dialog-title" className="text-base font-semibold text-white tracking-tight">
            Delete research?
          </h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            This will permanently delete <span className="text-foreground/90 font-medium">"{sessionTitle}"</span> and its generated report. This action cannot be undone.
          </p>
        </div>

        <div className="flex items-center justify-end gap-2.5 pt-1">
          <button
            type="button"
            onClick={onCancel}
            disabled={isPending}
            className="px-3.5 py-2 rounded-xl text-xs font-medium text-muted-foreground hover:text-white hover:bg-surface-hover transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={isPending}
            className="px-4 py-2 rounded-xl text-xs font-medium bg-destructive hover:bg-destructive/90 text-white transition-all shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring cursor-pointer flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isPending ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Deleting...</span>
              </>
            ) : (
              <>
                <Trash2 className="w-3.5 h-3.5" />
                <span>Delete</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>,
    document.body
  );
};
