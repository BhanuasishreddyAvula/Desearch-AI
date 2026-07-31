import React from 'react';
import { Compass, ArrowUp } from 'lucide-react';

export const NewResearchView: React.FC = () => {
  return (
    <div className="h-full flex flex-col items-center justify-center px-4 py-12 max-w-3xl mx-auto text-center space-y-8 select-none">
      {/* Central Focal Brand Icon & Question */}
      <div className="space-y-3">
        <div className="w-12 h-12 rounded-full bg-accent/10 border border-accent/20 flex items-center justify-center mx-auto text-accent shadow-sm">
          <Compass className="w-6 h-6" />
        </div>
        <h1 className="font-serif-editorial text-3xl md:text-4xl font-semibold text-foreground tracking-tight">
          What are we researching today?
        </h1>
        <p className="text-muted-foreground text-sm max-w-md mx-auto leading-relaxed font-sans-ui">
          Synthesize complex technical topics into rigorous, evidence-backed reports with real-time web sources.
        </p>
      </div>

      {/* Production Composer Placeholder (Full functionality owned by P3-03) */}
      <div className="w-full max-w-xl bg-surface border border-border rounded-lg p-3 shadow-sm text-left space-y-3">
        <div className="text-xs text-text-muted font-sans-ui px-1 py-4">
          Ask a research question or enter a topic...
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-border-subtle">
          <span className="text-[11px] font-mono-code px-2 py-0.5 rounded bg-surface-elevated text-muted-foreground border border-border-subtle">
            Deep Research Mode
          </span>

          <div className="w-8 h-8 rounded-full bg-accent text-accent-foreground flex items-center justify-center opacity-60 cursor-not-allowed">
            <ArrowUp className="w-4 h-4" />
          </div>
        </div>
      </div>

      {/* Example Prompts Preview */}
      <div className="flex flex-wrap items-center justify-center gap-2 max-w-lg text-xs text-muted-foreground font-sans-ui">
        <span className="px-3 py-1.5 rounded-full bg-surface border border-border-subtle hover:border-border cursor-pointer transition-colors">
          Compare FastAPI and Flask for production APIs
        </span>
        <span className="px-3 py-1.5 rounded-full bg-surface border border-border-subtle hover:border-border cursor-pointer transition-colors">
          Analyze vector database performance
        </span>
      </div>
    </div>
  );
};
