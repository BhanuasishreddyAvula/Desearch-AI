/**
 * Universal Source Resolution & Content Formatting Utility
 * Consolidates sources across report metadata, markdown citations, and execution timelines.
 */

import type { ReportSource } from '../../types';

export function normalizeSourceItem(item: any): ReportSource | null {
  if (!item) return null;
  let domainStr = '';
  let urlStr = '';
  let title = '';
  let snippet = '';

  if (typeof item === 'string') {
    urlStr = item.startsWith('http') ? item : `https://${item}`;
    try {
      domainStr = new URL(urlStr).hostname.replace(/^www\./, '');
    } catch {
      domainStr = item;
    }
    title = `${domainStr} - Research Reference Source`;
    snippet = `Cited evidence extracted from ${domainStr} for this report.`;
  } else if (typeof item === 'object') {
    urlStr = item.url || '';
    domainStr = item.domain || '';
    try {
      if (urlStr.startsWith('http')) {
        domainStr = new URL(urlStr).hostname.replace(/^www\./, '');
      } else if (domainStr.startsWith('http')) {
        domainStr = new URL(domainStr).hostname.replace(/^www\./, '');
      }
    } catch {
      /* keep raw */
    }
    if (!urlStr && domainStr) urlStr = `https://${domainStr}`;
    title = item.title || `${domainStr} - Research Reference Source`;
    snippet = item.snippet || item.description || `Evidence reference from ${domainStr}.`;
  }

  if (!domainStr) return null;

  return {
    domain: domainStr,
    url: urlStr || `https://${domainStr}`,
    title,
    snippet,
    category: domainStr.includes('github') ? 'GitHub' : 'Official Documentation',
    confidence: 'High',
  };
}

/**
 * Resolve, merge, and deduplicate all sources for a specific research response turn.
 * Combines explicit report sources_cited, execution timeline sources, and markdown URLs.
 */
export function resolveSourcesForResponse(
  explicitSources?: any[],
  markdownContent?: string,
  timelineSources?: any[]
): ReportSource[] {
  const uniqueMap = new Map<string, ReportSource>();

  const add = (item: any) => {
    const norm = normalizeSourceItem(item);
    if (norm && norm.domain && !uniqueMap.has(norm.domain)) {
      uniqueMap.set(norm.domain, norm);
    }
  };

  // 1. Explicit sources from report_result / metadata
  if (Array.isArray(explicitSources)) {
    explicitSources.forEach(add);
  }

  // 2. Timeline sources gathered during research execution
  if (Array.isArray(timelineSources)) {
    timelineSources.forEach(add);
  }

  // 3. Extract any additional HTTP URLs cited in Markdown text
  if (markdownContent) {
    const urlRegex = /(https?:\/\/[^\s<>"'()\]]+)/g;
    const matches = markdownContent.match(urlRegex) || [];
    matches.forEach(add);
  }

  return Array.from(uniqueMap.values());
}

/**
 * Safely extracts raw Markdown string from JSON content payloads or raw strings.
 * Recursively parses stringified JSON objects to isolate full_markdown text.
 */
export function extractCleanMarkdown(content: any): string {
  if (!content) return '';

  if (typeof content !== 'string') {
    if (typeof content === 'object' && content !== null) {
      const report = content.report_result || content.reportResult || content;

      if (report.full_markdown || report.fullMarkdown) {
        return extractCleanMarkdown(report.full_markdown || report.fullMarkdown);
      }
      if (report.content || report.text) {
        return extractCleanMarkdown(report.content || report.text);
      }

      // Format structured sections array into clean Markdown
      if (Array.isArray(report.sections) && report.sections.length > 0) {
        const title = report.title ? `# ${report.title}\n\n` : '';
        const execSummary = report.executive_summary ? `${report.executive_summary}\n\n` : '';
        const secsMd = report.sections
          .map((s: any) => {
            if (typeof s === 'string') return s;
            const lvl = '#'.repeat(s.level || 2);
            return `${lvl} ${s.title || 'Section'}\n\n${s.content || ''}`;
          })
          .join('\n\n');
        return `${title}${execSummary}${secsMd}`.trim();
      }

      if (report.executive_summary || report.summary) {
        const title = report.title ? `# ${report.title}\n\n` : '';
        return `${title}${report.executive_summary || report.summary}`;
      }
    }
    return '';
  }

  const trimmed = content.trim();
  if (trimmed === '[object Object]') return '';

  if (trimmed.startsWith('{') && trimmed.endsWith('}')) {
    try {
      const parsed = JSON.parse(trimmed);
      const res = extractCleanMarkdown(parsed);
      if (res) return res;
    } catch {
      /* not valid JSON, return raw text */
    }
  }

  return content;
}
