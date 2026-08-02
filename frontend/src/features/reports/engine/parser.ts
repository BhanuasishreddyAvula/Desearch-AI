import { DocumentAST, ASTNode, TOCItem, ReferenceCardNode, ExecSummaryCardNode, DocumentMetadataNode } from './ast';

export interface ParseOptions {
  title: string;
  query?: string;
  executiveSummary?: string;
  fullMarkdown: string;
  sources?: Array<{ title?: string; domain?: string; url?: string; snippet?: string; category?: string }>;
  createdAt?: string;
  executionTimeMs?: number;
}

const computeWordCount = (text: string): number => {
  return text.trim().split(/\s+/).filter(Boolean).length;
};

const computeReadingTime = (wordCount: number): string => {
  const mins = Math.max(1, Math.ceil(wordCount / 200));
  return `${mins} min read`;
};

const generateReportId = (title: string): string => {
  const hash = title.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  return `RPT-2026-${(hash % 9000 + 1000)}`;
};

/**
 * Publication Quality Report Parser (Ticket P4-11)
 * Converts raw research input into a publication-grade Document AST.
 */
export const parseMarkdownToAST = (options: ParseOptions): DocumentAST => {
  const dateStr = options.createdAt ? new Date(options.createdAt).toISOString().split('T')[0] : new Date().toISOString().split('T')[0];
  const sourcesCount = options.sources?.length || 0;
  const wordCount = computeWordCount(options.title + ' ' + (options.executiveSummary || '') + ' ' + options.fullMarkdown);
  const readingTime = computeReadingTime(wordCount);
  const reportId = generateReportId(options.title);
  const subtitle = `Comprehensive Technical Analysis & Evidence-Backed Research Report on ${options.query || options.title}`;
  const version = '1.0.0';
  const engineVersion = 'Desearch Engine v2.4 (Publication Spec)';

  const nodes: ASTNode[] = [];
  const tocItems: TOCItem[] = [];

  // 1. Redesigned Cover Page Node
  nodes.push({
    id: 'cover_page_node',
    type: 'cover_page',
    title: options.title,
    subtitle,
    query: options.query || options.title,
    date: dateStr,
    reportId,
    version,
    readingTime,
    sourcesCount,
    researchType: 'Intelligence Publication',
    publisher: 'Desearch AI Intelligence Engine',
    keepTogether: true,
  });

  // 2. TOC Node
  const tocNode: ASTNode = {
    id: 'toc_node',
    type: 'toc',
    items: tocItems,
    keepTogether: true,
  };
  nodes.push(tocNode);

  // 3. Executive Summary Card Node
  if (options.executiveSummary) {
    tocItems.push({
      id: 'exec_summary_toc',
      title: 'Executive Summary',
      level: 1,
    });

    const keyTakeaways = options.executiveSummary
      .split(/(?<=[.!?])\s+/)
      .filter((s) => s.length > 20)
      .slice(0, 3);

    const execCard: ExecSummaryCardNode = {
      id: 'exec_summary_card_node',
      type: 'exec_summary_card',
      summary: options.executiveSummary,
      keyTakeaways: keyTakeaways.length > 0 ? keyTakeaways : ['Comprehensive evidence-backed analysis compiled from cited sources.'],
      confidenceLevel: 'High',
      readingTime,
      keepTogether: true,
      minRemainingSpace: 120,
    };
    nodes.push(execCard);
  }

  // 4. Parse Body Markdown
  const rawLines = options.fullMarkdown.split('\n');
  let i = 0;
  let nodeCounter = 1;

  while (i < rawLines.length) {
    const line = rawLines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      i++;
      continue;
    }

    // Markdown Table Detection
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      const tableLines: string[] = [];
      while (i < rawLines.length && rawLines[i].trim().startsWith('|')) {
        tableLines.push(rawLines[i].trim());
        i++;
      }

      const parsedRows = tableLines
        .filter((l) => !l.includes('---'))
        .map((l) =>
          l
            .split('|')
            .slice(1, -1)
            .map((c) => c.trim())
        );

      if (parsedRows.length > 0) {
        nodes.push({
          id: `node_table_${nodeCounter++}`,
          type: 'table',
          headers: parsedRows[0],
          rows: parsedRows.slice(1),
          keepTogether: true,
          minRemainingSpace: 80,
        });
      }
      continue;
    }

    // Code Block Detection
    if (trimmed.startsWith('```')) {
      const lang = trimmed.substring(3).trim();
      const codeLines: string[] = [];
      i++;
      while (i < rawLines.length && !rawLines[i].trim().startsWith('```')) {
        codeLines.push(rawLines[i]);
        i++;
      }
      i++;

      nodes.push({
        id: `node_code_${nodeCounter++}`,
        type: 'code_block',
        language: lang || 'plaintext',
        code: codeLines.join('\n'),
        keepTogether: true,
        minRemainingSpace: 60,
      });
      continue;
    }

    // Headings Detection
    if (trimmed.startsWith('# ')) {
      const hText = trimmed.substring(2).trim();
      const hId = `heading_${nodeCounter++}`;
      tocItems.push({ id: hId, title: hText, level: 1 });
      nodes.push({
        id: hId,
        type: 'heading',
        level: 1,
        text: hText,
        keepTogether: true,
        minRemainingSpace: 55,
      });
    } else if (trimmed.startsWith('## ')) {
      const hText = trimmed.substring(3).trim();
      const hId = `heading_${nodeCounter++}`;
      tocItems.push({ id: hId, title: hText, level: 2 });
      nodes.push({
        id: hId,
        type: 'heading',
        level: 2,
        text: hText,
        keepTogether: true,
        minRemainingSpace: 45,
      });
    } else if (trimmed.startsWith('### ')) {
      const hText = trimmed.substring(4).trim();
      nodes.push({
        id: `heading_${nodeCounter++}`,
        type: 'heading',
        level: 3,
        text: hText,
        keepTogether: true,
        minRemainingSpace: 35,
      });
    } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ') || /^\d+\.\s/.test(trimmed)) {
      // List Detection
      const isOrdered = /^\d+\.\s/.test(trimmed);
      const listItems: string[] = [];
      while (
        i < rawLines.length &&
        (rawLines[i].trim().startsWith('- ') || rawLines[i].trim().startsWith('* ') || /^\d+\.\s/.test(rawLines[i].trim()))
      ) {
        listItems.push(rawLines[i].trim().replace(/^[-*]\s+|\d+\.\s+/, ''));
        i++;
      }
      i--;

      nodes.push({
        id: `node_list_${nodeCounter++}`,
        type: 'list',
        ordered: isOrdered,
        items: listItems,
        keepTogether: true,
        minRemainingSpace: 40,
      });
    } else {
      nodes.push({
        id: `node_para_${nodeCounter++}`,
        type: 'paragraph',
        text: trimmed,
      });
    }

    i++;
  }

  // 5. Reference Cards Nodes
  if (options.sources && options.sources.length > 0) {
    tocItems.push({
      id: 'references_toc',
      title: 'References & Cited Sources',
      level: 1,
    });

    nodes.push({
      id: 'heading_references',
      type: 'heading',
      level: 2,
      text: 'References & Cited Sources',
      keepTogether: true,
      minRemainingSpace: 45,
    });

    options.sources.forEach((s, idx) => {
      const cleanDomain = s.domain || (s.url ? new URL(s.url).hostname : 'source');
      const refNode: ReferenceCardNode = {
        id: `ref_card_${idx + 1}`,
        type: 'reference_card',
        index: idx + 1,
        title: s.title || `${cleanDomain} Research Reference`,
        domain: cleanDomain,
        url: s.url || `https://${cleanDomain}`,
        category: s.category || 'Official Documentation',
        snippet: s.snippet,
        keepTogether: true,
        minRemainingSpace: 45,
      };
      nodes.push(refNode);
    });
  }

  // 6. Document Metadata End Node
  const metaNode: DocumentMetadataNode = {
    id: 'document_metadata_node',
    type: 'document_metadata',
    generationTime: new Date().toLocaleTimeString(),
    generationDate: dateStr,
    version,
    wordCount,
    sourcesCount,
    readingTime,
    engineVersion,
    keepTogether: true,
    minRemainingSpace: 50,
  };
  nodes.push(metaNode);

  return {
    metadata: {
      title: options.title,
      subtitle,
      query: options.query || options.title,
      createdAt: dateStr,
      reportId,
      version,
      sourcesCount,
      wordCount,
      readingTime,
      engineVersion,
    },
    nodes,
  };
};
