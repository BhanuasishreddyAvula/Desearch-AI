/**
 * Publication Quality Report System — AST Node Definitions (Ticket P4-11)
 * Enterprise Document AST Supporting PDF, HTML, DOCX, and Markdown publishing.
 */

export type NodeType =
  | 'cover_page'
  | 'toc'
  | 'heading'
  | 'paragraph'
  | 'list'
  | 'table'
  | 'code_block'
  | 'callout'
  | 'exec_summary_card'
  | 'risk_card'
  | 'recommendation_card'
  | 'reference_card'
  | 'document_metadata'
  | 'divider';

export interface BaseNode {
  id: string;
  type: NodeType;
  keepTogether?: boolean;
  minRemainingSpace?: number; // Height in pt required on page
  calculatedHeight?: number;  // Computed during Measurement pass
  assignedPageNumber?: number; // Computed during Pagination pass
}

export interface CoverPageNode extends BaseNode {
  type: 'cover_page';
  title: string;
  subtitle: string;
  query?: string;
  date: string;
  reportId: string;
  version: string;
  readingTime: string;
  sourcesCount: number;
  researchType: string;
  publisher: string;
}

export interface TOCItem {
  id: string;
  title: string;
  level: number;
  targetPageNumber?: number;
}

export interface TOCNode extends BaseNode {
  type: 'toc';
  items: TOCItem[];
}

export interface HeadingNode extends BaseNode {
  type: 'heading';
  level: 1 | 2 | 3;
  text: string;
}

export interface ParagraphNode extends BaseNode {
  type: 'paragraph';
  text: string;
}

export interface ListNode extends BaseNode {
  type: 'list';
  ordered: boolean;
  items: string[];
}

export interface TableNode extends BaseNode {
  type: 'table';
  headers: string[];
  rows: string[][];
}

export interface CodeBlockNode extends BaseNode {
  type: 'code_block';
  language?: string;
  code: string;
}

export interface CalloutNode extends BaseNode {
  type: 'callout';
  variant: 'info' | 'summary' | 'warning' | 'recommendation';
  title: string;
  text: string;
}

export interface ExecSummaryCardNode extends BaseNode {
  type: 'exec_summary_card';
  summary: string;
  keyTakeaways: string[];
  confidenceLevel: 'High' | 'Medium' | 'Low';
  readingTime: string;
}

export interface RiskCardNode extends BaseNode {
  type: 'risk_card';
  title: string;
  severity: 'High' | 'Medium' | 'Low';
  impact: string;
  mitigation: string;
}

export interface RecommendationCardNode extends BaseNode {
  type: 'recommendation_card';
  index: number;
  title: string;
  description: string;
  expectedBenefit: string;
}

export interface ReferenceCardNode extends BaseNode {
  type: 'reference_card';
  index: number;
  title: string;
  domain: string;
  url: string;
  category: string;
  snippet?: string;
}

export interface DocumentMetadataNode extends BaseNode {
  type: 'document_metadata';
  generationTime: string;
  generationDate: string;
  version: string;
  wordCount: number;
  sourcesCount: number;
  readingTime: string;
  engineVersion: string;
}

export interface DividerNode extends BaseNode {
  type: 'divider';
}

export type ASTNode =
  | CoverPageNode
  | TOCNode
  | HeadingNode
  | ParagraphNode
  | ListNode
  | TableNode
  | CodeBlockNode
  | CalloutNode
  | ExecSummaryCardNode
  | RiskCardNode
  | RecommendationCardNode
  | ReferenceCardNode
  | DocumentMetadataNode
  | DividerNode;

export interface DocumentAST {
  metadata: {
    title: string;
    subtitle: string;
    query?: string;
    createdAt: string;
    reportId: string;
    version: string;
    sourcesCount: number;
    wordCount: number;
    readingTime: string;
    engineVersion: string;
  };
  nodes: ASTNode[];
}
