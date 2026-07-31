import React from 'react';
import { Compass, FileText } from 'lucide-react';

export const Header: React.FC = () => {
  const handleReportsClick = () => {
    // Reports drawer is owned by P3-07. Action is safe and inert in P3-02.
  };

  return (
    <header className="h-14 border-b border-border bg-sidebar px-4 md:px-6 flex items-center justify-between font-sans-ui select-none">
      {/* Left Brand Indicator (for mobile / narrow viewports) */}
      <div className="flex items-center gap-2 md:hidden">
        <Compass className="w-5 h-5 text-accent" />
        <span className="font-serif-editorial font-bold text-lg text-foreground tracking-tight">
          Desearch AI
        </span>
      </div>

      <div className="hidden md:block" />

      {/* Right Contextual Actions — ONLY Reports Control */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={handleReportsClick}
          aria-label="Reports contextual drawer"
          title="Reports & Evidence (P3-07)"
          className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-surface border border-border-subtle hover:bg-surface-hover text-foreground/90 hover:text-foreground text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-focus-ring"
        >
          <FileText className="w-3.5 h-3.5 text-accent" />
          <span>Reports</span>
        </button>
      </div>
    </header>
  );
};
