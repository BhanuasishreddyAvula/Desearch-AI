import React from 'react';
import type { HeadingNode } from '../../utils/markdownParser';
import { InlineRenderer } from './InlineRenderer';

interface HeadingBlockProps {
  node: HeadingNode;
}

export const HeadingBlock: React.FC<HeadingBlockProps> = ({ node }) => {
  const { level, text } = node;

  if (level === 1) {
    return (
      <h1 className="font-serif-editorial text-3xl md:text-4xl font-bold text-white tracking-tight leading-tight first:mt-0 mt-8 mb-4 animate-in fade-in duration-150 select-text">
        <InlineRenderer text={text} />
      </h1>
    );
  }

  if (level === 2) {
    return (
      <h2 className="font-serif-editorial text-2xl md:text-3xl font-semibold text-white tracking-tight first:mt-0 mt-8 mb-4 pb-2 border-b border-border-subtle/50 animate-in fade-in duration-150 select-text">
        <InlineRenderer text={text} />
      </h2>
    );
  }

  return (
    <h3 className="font-sans-ui text-lg md:text-xl font-medium text-foreground tracking-tight first:mt-0 mt-6 mb-2 animate-in fade-in duration-150 select-text">
      <InlineRenderer text={text} />
    </h3>
  );
};
