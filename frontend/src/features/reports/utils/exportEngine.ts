import { parseMarkdownToAST, ParseOptions } from '../engine/parser';
import { validateDocumentAST } from '../engine/validationEngine';
import { computeLayoutMeasurement } from '../engine/layoutEngine';
import { computePagination } from '../engine/paginationEngine';
import { PDFPresentationRenderer } from '../engine/renderers/pdfRenderer';
import { MarkdownPresentationRenderer } from '../engine/renderers/markdownRenderer';
import { HTMLPresentationRenderer } from '../engine/renderers/htmlRenderer';

export interface ExportSourceItem {
  title?: string;
  domain?: string;
  url?: string;
  snippet?: string;
  category?: string;
}

export interface ExportReportData {
  title: string;
  query?: string;
  executiveSummary?: string;
  fullMarkdown: string;
  sources?: ExportSourceItem[];
  createdAt?: string;
  executionTimeMs?: number;
}

const sanitizeFilename = (title: string, dateStr?: string): string => {
  const cleanTitle = title.replace(/[^a-zA-Z0-9_-]/g, '_').replace(/_+/g, '_').substring(0, 50);
  const date = dateStr ? new Date(dateStr).toISOString().split('T')[0] : new Date().toISOString().split('T')[0];
  return `${cleanTitle}_-_${date}`;
};

const triggerDownload = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

/**
 * Enterprise Publication Engine Core Pipeline
 * Pipeline: Parse Markdown -> AST -> Validation Layer -> Layout Measurement Pass -> Pagination Pass -> Renderers (PDF / HTML / MD)
 */
const buildAndProcessAST = (data: ExportReportData) => {
  const parseOpts: ParseOptions = {
    title: data.title,
    query: data.query,
    executiveSummary: data.executiveSummary,
    fullMarkdown: data.fullMarkdown,
    sources: data.sources,
    createdAt: data.createdAt,
    executionTimeMs: data.executionTimeMs,
  };

  const ast = parseMarkdownToAST(parseOpts);
  const validatedAST = validateDocumentAST(ast);
  const measuredAST = computeLayoutMeasurement(validatedAST);
  const paginatedAST = computePagination(measuredAST);

  return paginatedAST;
};

/**
 * 1. Programmatic PDF Export (Direct Download, Zero Print Window)
 */
export const exportAsPDF = (data: ExportReportData): void => {
  const ast = buildAndProcessAST(data);
  const renderer = new PDFPresentationRenderer();
  const pdfBlob = renderer.render(ast);
  const filename = `${sanitizeFilename(data.title, data.createdAt)}.pdf`;
  triggerDownload(pdfBlob, filename);
};

/**
 * 2. HTML Web Document Export
 */
export const exportAsHTML = (data: ExportReportData): void => {
  const ast = buildAndProcessAST(data);
  const renderer = new HTMLPresentationRenderer();
  const htmlBlob = renderer.render(ast);
  const filename = `${sanitizeFilename(data.title, data.createdAt)}.html`;
  triggerDownload(htmlBlob, filename);
};

/**
 * 3. Clean GitHub Markdown Export
 */
export const exportAsMarkdown = (data: ExportReportData): void => {
  const ast = buildAndProcessAST(data);
  const renderer = new MarkdownPresentationRenderer();
  const mdBlob = renderer.render(ast);
  const filename = `${sanitizeFilename(data.title, data.createdAt)}.md`;
  triggerDownload(mdBlob, filename);
};
