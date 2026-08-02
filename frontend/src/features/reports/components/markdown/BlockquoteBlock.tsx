import React from 'react';
import type { BlockquoteNode } from '../../utils/markdownParser';
import { InlineRenderer } from './InlineRenderer';

interface BlockquoteBlockProps {
  node: BlockquoteNode;
}

export const BlockquoteBlock: React.FC<BlockquoteBlockProps> = ({ node }) => {
  return (
    <blockquote className="my-5 border-l-2 border-accent bg-accent-subtle/20 text-foreground/90 italic pl-4 py-2 rounded-r-lg font-sans-ui text-sm md:text-base leading-relaxed select-text animate-in fade-in duration-150">
      <InlineRenderer text={node.text} />
    </blockquote>
  );
};
