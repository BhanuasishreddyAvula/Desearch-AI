import React from 'react';
import { MarkdownRenderer } from './markdown/MarkdownRenderer';
import { ReportActionBar } from './ReportActionBar';

interface ResearchReportProps {
  title?: string;
  markdownContent?: string;
  isStreaming?: boolean;
  sourcesCount?: number;
  sources?: string[];
}

export const ResearchReport: React.FC<ResearchReportProps> = ({
  title = 'Research Report',
  markdownContent = '',
  sourcesCount = 0,
  sources = [],
}) => {
  // The report does not exist until markdown content is present
  if (!markdownContent) {
    return null;
  }

  return (
    <article className="w-full max-w-[760px] mx-auto font-sans-ui text-left select-text animate-in fade-in duration-250">
      {/* 1. Markdown Renderer AST Pipeline */}
      <MarkdownRenderer content={markdownContent} />

      {/* 2. End-of-Report Sources & Export Action Bar (P3-04B) */}
      <ReportActionBar
        title={title}
        markdownContent={markdownContent}
        sources={sources}
        sourcesCount={sourcesCount}
        isCompleted={true}
        responseIndex={1}
      />

    </article>
  );
};
