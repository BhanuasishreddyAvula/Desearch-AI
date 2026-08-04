import React from 'react';
import { Sparkles } from 'lucide-react';
import { ResearchComposer } from './ResearchComposer';

export const NewResearchView: React.FC = () => {
  return (
    <div className="relative flex flex-col justify-between items-center h-full w-full min-h-[100dvh] sm:min-h-0 overflow-hidden font-sans-ui select-none">
      {/* 1. Hero Welcome Section (Centered in Top/Middle Viewport, Claude Style) */}
      <div className="flex-1 flex flex-col items-center justify-center text-center w-full px-4 sm:px-6 py-6 md:py-12 my-auto select-none">
        <div className="w-full max-w-[760px] mx-auto flex flex-col items-center justify-center space-y-3.5 sm:space-y-5 md:space-y-6 my-auto">
          
          {/* Welcome Badge */}
          <div className="relative inline-flex items-center gap-2.5 px-1 py-1 select-none animate-in fade-in duration-300 mb-1 sm:mb-2">
            {/* Subtle Ambient Radial Glow */}
            <div className="absolute -inset-4 bg-accent/20 rounded-full blur-xl opacity-70 pointer-events-none" />

            <Sparkles className="w-4.5 h-4.5 sm:w-5 sm:h-5 text-accent drop-shadow-[0_0_10px_rgba(217,83,56,0.7)] relative z-10 shrink-0" />
            <span className="font-serif-editorial text-base sm:text-lg md:text-xl text-foreground/90 tracking-tight relative z-10">
              Welcome to <span className="font-bold text-white">Desearch</span> <span className="font-extrabold text-accent">AI</span>
            </span>
          </div>

          {/* Main Heading */}
          <h1 className="font-serif-editorial text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-normal text-white tracking-tight leading-[1.15] max-w-xl">
            What are we researching today?
          </h1>
          
          {/* Subheading */}
          <p className="text-muted-foreground/85 text-xs sm:text-sm md:text-base max-w-md mx-auto leading-relaxed font-sans-ui font-light">
            Enter any topic or question to generate an evidence-backed, deep technical research report.
          </p>

        </div>
      </div>

      {/* 2. Bottom Anchored Research Composer (Claude Mobile Style: Snug on Keyboard) */}
      <div className="w-full max-w-[760px] mx-auto px-4 sm:px-6 pb-4 sm:pb-8 md:pb-12 pt-2 shrink-0">
        <ResearchComposer />
      </div>
    </div>
  );
};
