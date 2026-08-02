import React, { useEffect, useRef } from 'react';
import { X, Globe, ExternalLink } from 'lucide-react';

interface SourcesPopoverProps {
  sources: string[];
  isOpen: boolean;
  onClose: () => void;
}

export const SourcesPopover: React.FC<SourcesPopoverProps> = ({
  sources = [],
  isOpen,
  onClose,
}) => {
  const popoverRef = useRef<HTMLDivElement>(null);

  // Close on Escape key or outside click
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    const handleClickOutside = (e: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-150">
      <div
        ref={popoverRef}
        role="dialog"
        aria-modal="true"
        aria-label="Cited Sources"
        className="w-full max-w-md bg-surface border border-border-subtle rounded-2xl shadow-2xl overflow-hidden font-sans-ui text-left animate-in zoom-in-95 duration-150"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-border-subtle/60 select-none">
          <div className="flex items-center gap-2">
            <Globe className="w-4 h-4 text-accent" />
            <h3 className="text-sm font-semibold text-white tracking-tight">
              Cited Sources ({sources.length})
            </h3>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close sources popover"
            className="p-1 rounded-lg text-muted-foreground hover:text-white hover:bg-surface-hover transition-colors cursor-pointer focus:outline-none"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Source List Container */}
        <div className="max-h-[360px] overflow-y-auto p-3 space-y-1.5">
          {sources.length === 0 ? (
            <div className="py-8 text-center text-xs text-muted-foreground">
              No explicit web sources cited.
            </div>
          ) : (
            sources.map((domain, idx) => {
              const url = domain.startsWith('http://') || domain.startsWith('https://')
                ? domain
                : `https://${domain}`;

              return (
                <a
                  key={idx}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-2.5 rounded-xl hover:bg-surface-hover border border-transparent hover:border-border-subtle/60 transition-all duration-150 group/item cursor-pointer"
                >
                  <div className="flex items-center gap-2.5 min-w-0 pr-2">
                    <img
                      src={`https://www.google.com/s2/favicons?domain=${domain}&sz=32`}
                      alt=""
                      aria-hidden="true"
                      className="w-4 h-4 rounded-xs shrink-0 object-contain"
                      onError={(e) => {
                        e.currentTarget.style.display = 'none';
                      }}
                    />
                    <div className="min-w-0">
                      <div className="text-xs font-medium text-foreground group-hover/item:text-white truncate">
                        {domain}
                      </div>
                      <div className="text-[10px] font-mono-code text-muted-foreground/70 truncate">
                        {url}
                      </div>
                    </div>
                  </div>
                  <ExternalLink className="w-3.5 h-3.5 text-muted-foreground/60 group-hover/item:text-accent transition-colors shrink-0" />
                </a>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
