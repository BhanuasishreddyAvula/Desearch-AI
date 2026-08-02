import { DocumentAST, TOCNode } from './ast';
import { LayoutGrid } from './typography';

/**
 * Publication Layout Engine — Pagination Pass (Ticket P4-10)
 * Performs deterministic 2nd-pass page assignment, widow/orphan protection, and TOC page number resolution.
 */
export const computePagination = (ast: DocumentAST): DocumentAST => {
  let currentPage = 1;
  let currentY = LayoutGrid.usableHeight;

  // Map to track heading IDs to assigned page numbers
  const headingPageMap = new Map<string, number>();

  ast.nodes.forEach((node) => {
    // Cover Page is forced to Page 1
    if (node.type === 'cover_page') {
      node.assignedPageNumber = 1;
      currentPage = 2;
      currentY = LayoutGrid.usableHeight;
      return;
    }

    // TOC is forced to Page 2
    if (node.type === 'toc') {
      node.assignedPageNumber = 2;
      currentPage = 3;
      currentY = LayoutGrid.usableHeight;
      return;
    }

    const nodeHeight = node.calculatedHeight || 20;
    const minRequired = node.minRemainingSpace || nodeHeight;

    // Check if node fits on current page (Widow / Orphan protection)
    if (currentY - minRequired < 0) {
      currentPage++;
      currentY = LayoutGrid.usableHeight;
    }

    node.assignedPageNumber = currentPage;
    currentY -= nodeHeight;

    // Store page number for headings to resolve TOC page numbers
    if (node.type === 'heading') {
      headingPageMap.set(node.id, currentPage);
    }
  });

  // Automatically populate TOC item page numbers from resolved pagination pass
  const tocNode = ast.nodes.find((n) => n.type === 'toc') as TOCNode | undefined;
  if (tocNode) {
    tocNode.items.forEach((item) => {
      if (item.id === 'exec_summary_toc') {
        item.targetPageNumber = 3;
      } else if (item.id === 'references_toc') {
        const refHeading = ast.nodes.find((n) => n.id === 'heading_references');
        item.targetPageNumber = refHeading?.assignedPageNumber || currentPage;
      } else {
        item.targetPageNumber = headingPageMap.get(item.id) || 3;
      }
    });
  }

  return ast;
};
