import React, { useMemo } from 'react';
import { parseMarkdownToAST } from '../../utils/markdownParser';
import { extractCleanMarkdown } from '../../../../lib/utils/sources';
import { HeadingBlock } from './HeadingBlock';
import { ParagraphBlock } from './ParagraphBlock';
import { ListBlock } from './ListBlock';
import { TableBlock } from './TableBlock';
import { CodeBlock } from './CodeBlock';
import { BlockquoteBlock } from './BlockquoteBlock';
import { HorizontalRule } from './HorizontalRule';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  const cleanContent = useMemo(() => extractCleanMarkdown(content), [content]);

  const nodes = useMemo(() => {
    try {
      return parseMarkdownToAST(cleanContent);
    } catch {
      // Fallback gracefully on parsing exception
      return [{ type: 'paragraph', text: cleanContent } as const];
    }
  }, [cleanContent]);


  if (!content || nodes.length === 0) {
    return null;
  }

  return (
    <div className="w-full space-y-4 font-sans-ui text-left text-foreground select-text">
      {nodes.map((node, index) => {
        switch (node.type) {
          case 'heading':
            return <HeadingBlock key={index} node={node} />;
          case 'paragraph':
            return <ParagraphBlock key={index} node={node} />;
          case 'list':
            return <ListBlock key={index} node={node} />;
          case 'table':
            return <TableBlock key={index} node={node} />;
          case 'code_block':
            return <CodeBlock key={index} node={node} />;
          case 'blockquote':
            return <BlockquoteBlock key={index} node={node} />;
          case 'hr':
            return <HorizontalRule key={index} />;
          default:
            return null;
        }
      })}
    </div>
  );
};
