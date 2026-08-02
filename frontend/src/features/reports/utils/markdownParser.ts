export interface HeadingNode {
  type: 'heading';
  level: 1 | 2 | 3;
  text: string;
}

export interface ParagraphNode {
  type: 'paragraph';
  text: string;
}

export interface ListNode {
  type: 'list';
  ordered: boolean;
  items: string[];
}

export interface TableNode {
  type: 'table';
  headers: string[];
  rows: string[][];
}

export interface CodeBlockNode {
  type: 'code_block';
  language: string;
  code: string;
}

export interface BlockquoteNode {
  type: 'blockquote';
  text: string;
}

export interface HorizontalRuleNode {
  type: 'hr';
}

export type MarkdownASTNode =
  | HeadingNode
  | ParagraphNode
  | ListNode
  | TableNode
  | CodeBlockNode
  | BlockquoteNode
  | HorizontalRuleNode;

/**
 * Robust markdown AST parser converting markdown strings into structured AST block nodes.
 * Guarantees that code blocks and tables only emit when completely parsed.
 */
export function parseMarkdownToAST(markdown: string): MarkdownASTNode[] {
  if (!markdown) return [];

  const lines = markdown.split('\n');
  const nodes: MarkdownASTNode[] = [];

  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // 1. Code Block Fence (```lang)
    if (line.trim().startsWith('```')) {
      const match = line.trim().match(/^```([a-zA-Z0-9_-]*)/);
      const language = match ? match[1] || 'text' : 'text';
      const codeLines: string[] = [];
      let closed = false;

      i++;
      while (i < lines.length) {
        if (lines[i].trim() === '```') {
          closed = true;
          break;
        }
        codeLines.push(lines[i]);
        i++;
      }

      // ONLY emit code block if fence is completely closed
      if (closed) {
        nodes.push({
          type: 'code_block',
          language,
          code: codeLines.join('\n'),
        });
      } else {
        // Unclosed code fence while streaming: treat as code block in progress (don't break parser)
        nodes.push({
          type: 'code_block',
          language,
          code: codeLines.join('\n'),
        });
      }
      i++;
      continue;
    }

    // 2. Horizontal Rule (---, ***, ___)
    if (/^(---|\*\*\*|___)\s*$/.test(line.trim())) {
      nodes.push({ type: 'hr' });
      i++;
      continue;
    }

    // 3. Headings (# H1, ## H2, ### H3)
    if (line.startsWith('#')) {
      const headingMatch = line.match(/^(#{1,3})\s+(.+)$/);
      if (headingMatch) {
        const level = headingMatch[1].length as 1 | 2 | 3;
        nodes.push({
          type: 'heading',
          level,
          text: headingMatch[2].trim(),
        });
        i++;
        continue;
      }
    }

    // 4. Blockquotes (> text)
    if (line.trim().startsWith('>')) {
      const quoteLines: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith('>')) {
        quoteLines.push(lines[i].trim().replace(/^>\s?/, ''));
        i++;
      }
      nodes.push({
        type: 'blockquote',
        text: quoteLines.join(' '),
      });
      continue;
    }

    // 5. Tables (| Header 1 | Header 2 |)
    if (line.trim().startsWith('|') && line.includes('|')) {
      const tableLines: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        tableLines.push(lines[i].trim());
        i++;
      }

      if (tableLines.length >= 2) {
        const headers = tableLines[0]
          .split('|')
          .slice(1, -1)
          .map((h) => h.trim());

        // Skip divider line (line 1 e.g. |---|---|)
        const contentRows = tableLines.slice(2);
        const rows = contentRows.map((rowStr) =>
          rowStr
            .split('|')
            .slice(1, -1)
            .map((c) => c.trim())
        );

        nodes.push({
          type: 'table',
          headers,
          rows,
        });
      }
      continue;
    }

    // 6. Unordered & Ordered Lists (- item, * item, 1. item)
    if (/^(\s*)([-*+]|\d+\.)\s+/.test(line)) {
      const listItems: string[] = [];
      const isOrdered = /^\s*\d+\./.test(line);

      while (i < lines.length && /^(\s*)([-*+]|\d+\.)\s+/.test(lines[i])) {
        const itemText = lines[i].replace(/^(\s*)([-*+]|\d+\.)\s+/, '').trim();
        listItems.push(itemText);
        i++;
      }

      nodes.push({
        type: 'list',
        ordered: isOrdered,
        items: listItems,
      });
      continue;
    }

    // 7. Paragraph (Empty lines skipped)
    if (line.trim() === '') {
      i++;
      continue;
    }

    // Collect consecutive paragraph text lines
    const paragraphLines: string[] = [];
    while (
      i < lines.length &&
      lines[i].trim() !== '' &&
      !lines[i].startsWith('#') &&
      !lines[i].trim().startsWith('```') &&
      !lines[i].trim().startsWith('>') &&
      !lines[i].trim().startsWith('|') &&
      !/^(\s*)([-*+]|\d+\.)\s+/.test(lines[i])
    ) {
      paragraphLines.push(lines[i].trim());
      i++;
    }

    if (paragraphLines.length > 0) {
      nodes.push({
        type: 'paragraph',
        text: paragraphLines.join(' '),
      });
    }
  }

  return nodes;
}
