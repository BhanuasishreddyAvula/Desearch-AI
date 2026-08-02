import React from 'react';

export const ReportSkeleton: React.FC = () => {
  return (
    <div className="w-full max-w-[760px] mx-auto space-y-6 pt-2 font-sans-ui text-left select-none animate-in fade-in duration-200">
      {/* Title Skeleton */}
      <div className="space-y-3 pb-4 border-b border-border-subtle/40">
        <div className="h-3 w-28 bg-surface-hover/80 rounded-md animate-pulse" />
        <div className="h-8 w-3/4 bg-surface-hover/90 rounded-xl animate-pulse" />
      </div>

      {/* Paragraph Block 1 Skeleton */}
      <div className="space-y-3">
        <div className="h-4 w-full bg-surface-hover/70 rounded-md animate-pulse" />
        <div className="h-4 w-[92%] bg-surface-hover/70 rounded-md animate-pulse" />
        <div className="h-4 w-[85%] bg-surface-hover/70 rounded-md animate-pulse" />
        <div className="h-4 w-[65%] bg-surface-hover/70 rounded-md animate-pulse" />
      </div>

      {/* Subheading Skeleton */}
      <div className="pt-2">
        <div className="h-6 w-1/3 bg-surface-hover/90 rounded-lg animate-pulse" />
      </div>

      {/* Paragraph Block 2 Skeleton */}
      <div className="space-y-3">
        <div className="h-4 w-[98%] bg-surface-hover/70 rounded-md animate-pulse" />
        <div className="h-4 w-[88%] bg-surface-hover/70 rounded-md animate-pulse" />
        <div className="h-4 w-[75%] bg-surface-hover/70 rounded-md animate-pulse" />
      </div>

      {/* List Items Skeleton */}
      <div className="space-y-2.5 pl-4 border-l border-border-subtle/40 my-4">
        <div className="h-4 w-[60%] bg-surface-hover/60 rounded-md animate-pulse" />
        <div className="h-4 w-[72%] bg-surface-hover/60 rounded-md animate-pulse" />
        <div className="h-4 w-[50%] bg-surface-hover/60 rounded-md animate-pulse" />
      </div>

      {/* Table Skeleton */}
      <div className="w-full h-32 rounded-xl border border-border-subtle/50 bg-surface-hover/40 animate-pulse my-6" />

      {/* Paragraph Block 3 Skeleton */}
      <div className="space-y-3">
        <div className="h-4 w-[95%] bg-surface-hover/70 rounded-md animate-pulse" />
        <div className="h-4 w-[80%] bg-surface-hover/70 rounded-md animate-pulse" />
      </div>
    </div>
  );
};
