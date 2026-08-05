import React from 'react';
import type { ParagraphNode } from '../../utils/markdownParser';
import { splitIntoSentences } from '../../utils/sentenceSplitter';
import { InlineRenderer } from './InlineRenderer';

interface ParagraphBlockProps {
  node: ParagraphNode;
}

export const ParagraphBlock: React.FC<ParagraphBlockProps> = ({ node }) => {
  const sentences = splitIntoSentences(node.text);

  return (
    <p className="font-sans-ui text-sm md:text-base leading-relaxed text-foreground/90 mb-5 select-text">
      {sentences.map((sentence, idx) => (
        <span
          key={idx}
          className="inline animate-claude-fade"
        >
          <InlineRenderer text={sentence} />
          {idx < sentences.length - 1 ? ' ' : ''}
        </span>
      ))}
    </p>
  );
};
