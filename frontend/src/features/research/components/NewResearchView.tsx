import React from 'react';
import { ResearchComposer } from './ResearchComposer';

export const NewResearchView: React.FC = () => {
  return (
    <div className="relative flex flex-col items-center justify-center h-full w-full overflow-hidden font-sans-ui">
      {/* Centered Hero Header Canvas */}
      <div className="flex-1 flex flex-col items-center justify-center w-full px-4 md:px-6 py-12 text-center select-none">
        <div className="w-full max-w-[760px] mx-auto flex flex-col items-center space-y-8 md:space-y-12">
          {/* Hero Header Block */}
          <div className="space-y-3.5 max-w-xl mx-auto">
            <h1 className="font-serif-editorial text-4xl md:text-5xl lg:text-6xl font-normal text-white tracking-tight leading-[1.15]">
              What are we researching today?
            </h1>
            <p className="text-muted-foreground/85 text-sm md:text-base lg:text-lg max-w-md mx-auto leading-relaxed font-sans-ui font-light">
              Enter any question or topic to generate an evidence-backed intelligence report.
            </p>
          </div>

          {/* Research Composer Container (Synchronized 760px Alignment) */}
          <div className="w-full max-w-[760px] mx-auto flex justify-center">
            <ResearchComposer />
          </div>
        </div>
      </div>
    </div>
  );
};
