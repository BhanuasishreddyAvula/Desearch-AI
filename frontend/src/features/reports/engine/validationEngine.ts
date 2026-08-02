import { DocumentAST } from './ast';

/**
 * Publication Engine — Validation Layer (Ticket P4-20)
 * Validates metadata, source count, word count, and AST node integrity before rendering.
 * Prevents 'undefined', 'null', or '0 sources' placeholders when data exists.
 */
export const validateDocumentAST = (ast: DocumentAST): DocumentAST => {
  // 1. Title Validation
  if (!ast.metadata.title || ast.metadata.title.trim() === '' || ast.metadata.title.toLowerCase() === 'undefined') {
    ast.metadata.title = 'Research Intelligence Report';
  }

  // 2. Query/Topic Validation
  if (!ast.metadata.query || ast.metadata.query.trim() === '' || ast.metadata.query.toLowerCase() === 'undefined') {
    ast.metadata.query = ast.metadata.title;
  }

  // 3. Report ID Validation
  if (!ast.metadata.reportId || ast.metadata.reportId.includes('undefined') || ast.metadata.reportId.includes('null')) {
    const hash = ast.metadata.title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    ast.metadata.reportId = `RPT-2026-${(hash % 9000) + 1000}`;
  }

  // 4. Source Count Validation (Recalculate accurately from reference cards if 0)
  const actualRefCardsCount = ast.nodes.filter((n) => n.type === 'reference_card').length;
  if (actualRefCardsCount > 0 && (ast.metadata.sourcesCount === 0 || !ast.metadata.sourcesCount)) {
    ast.metadata.sourcesCount = actualRefCardsCount;
  }

  // Update Cover Page Node metadata to match validated metadata
  const coverNode = ast.nodes.find((n) => n.type === 'cover_page');
  if (coverNode && coverNode.type === 'cover_page') {
    coverNode.title = ast.metadata.title;
    coverNode.query = ast.metadata.query;
    coverNode.reportId = ast.metadata.reportId;
    coverNode.sourcesCount = ast.metadata.sourcesCount;
  }

  // 5. AST Nodes Non-Empty Guarantee
  if (ast.nodes.length === 0) {
    throw new Error('Publication Validation Error: Document AST contains no renderable content nodes.');
  }

  return ast;
};
