import { DocumentAST, ExecSummaryCardNode } from './ast';
import { TypographySystem, LayoutGrid } from './typography';

const wrapTextLines = (text: string, maxChars: number): string[] => {
  const words = text.split(' ');
  const lines: string[] = [];
  let current = '';

  words.forEach((w) => {
    if ((current + w).length > maxChars) {
      lines.push(current.trim());
      current = w + ' ';
    } else {
      current += w + ' ';
    }
  });

  if (current.trim()) lines.push(current.trim());
  return lines;
};

/**
 * Publication Quality Report System — Measurement Pass (Ticket P4-11)
 * Computes node heights for all publication nodes before pagination.
 */
export const computeLayoutMeasurement = (ast: DocumentAST): DocumentAST => {
  ast.nodes.forEach((node) => {
    switch (node.type) {
      case 'cover_page': {
        node.calculatedHeight = LayoutGrid.pageHeight; // Fixed 1 full page
        break;
      }
      case 'toc': {
        const itemHeight = 18;
        const totalItems = node.items.length;
        node.calculatedHeight = 50 + totalItems * itemHeight;
        break;
      }
      case 'exec_summary_card': {
        const card = node as ExecSummaryCardNode;
        const sumLines = wrapTextLines(card.summary, 82);
        node.calculatedHeight = sumLines.length * 13 + 60;
        break;
      }
      case 'heading': {
        const token =
          node.level === 1
            ? TypographySystem.heading1
            : node.level === 2
            ? TypographySystem.heading2
            : TypographySystem.heading3;
        const lines = wrapTextLines(node.text, 50);
        node.calculatedHeight = lines.length * (token.fontSize * token.lineHeight) + token.marginTop + token.marginBottom;
        break;
      }
      case 'paragraph': {
        const token = TypographySystem.body;
        const lines = wrapTextLines(node.text, 84);
        node.calculatedHeight = lines.length * (token.fontSize * token.lineHeight) + token.marginBottom;
        break;
      }
      case 'list': {
        const token = TypographySystem.listItem;
        let totalLines = 0;
        node.items.forEach((item) => {
          const lines = wrapTextLines(item, 80);
          totalLines += lines.length;
        });
        node.calculatedHeight = totalLines * (token.fontSize * token.lineHeight) + node.items.length * token.marginBottom;
        break;
      }
      case 'table': {
        const rowHeight = 22;
        const headerHeight = 24;
        node.calculatedHeight = headerHeight + node.rows.length * rowHeight + 12;
        break;
      }
      case 'code_block': {
        const codeLines = node.code.split('\n').length;
        node.calculatedHeight = codeLines * 13 + 24;
        break;
      }
      case 'callout': {
        const lines = wrapTextLines(node.text, 82);
        node.calculatedHeight = lines.length * 13 + 36;
        break;
      }
      case 'reference_card': {
        node.calculatedHeight = 44;
        break;
      }
      case 'document_metadata': {
        node.calculatedHeight = 55;
        break;
      }
      case 'divider': {
        node.calculatedHeight = 12;
        break;
      }
    }
  });

  return ast;
};
