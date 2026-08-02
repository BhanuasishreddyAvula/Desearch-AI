import React from 'react';
import { Compass, FileText } from 'lucide-react';

export const Header: React.FC = () => {
  const handleReportsClick = () => {
    // Reports drawer action owned by P3-07
  };

  return (
    <header className="h-16 bg-background px-4 md:px-8 flex items-center justify-between font-sans-ui select-none">
      {/* Left Brand Indicator (for mobile viewports) */}
      <div className="flex items-center gap-2 md:hidden">
        <div className="w-5 h-5 rounded-md bg-accent flex items-center justify-center text-accent-foreground">
          <Compass className="w-3.5 h-3.5" />
        </div>
        <span className="font-serif-editorial font-bold text-lg text-white tracking-tight">
          Desearch AI
        </span>
      </div>

      <div className="hidden md:block" />

      {/* Right Top-Header Action — Reports Button */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={handleReportsClick}
          aria-label="Reports contextual drawer"
          title="Reports & Evidence"
          className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-surface/80 border border-border-subtle hover:bg-surface-hover hover:border-border text-foreground/90 hover:text-white text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-focus-ring shadow-sm"
        >
          <FileText className="w-4 h-4 text-muted-foreground" />
          <span>Reports</span>
        </button>
      </div>
    </header>
  );
};
