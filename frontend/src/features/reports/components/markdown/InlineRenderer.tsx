import React from 'react';
import { ExternalLink } from 'lucide-react';
import { CitationBadge } from '../citations/CitationBadge';

interface InlineRendererProps {
  text: string;
}

/**
 * Citation Intelligence Engine Inline Renderer
 * Parses structured inline numeric citations ([1], [2], [1][2], [2-4]), bracket citations, links, and formatting.
 */
export const InlineRenderer: React.FC<InlineRendererProps> = ({ text }) => {
  if (!text) return null;

  // Regex splitting tokens:
  // 1. Numeric inline citations: [1], [2], [1][2], [2-4], [1, 2]
  // 2. Bracketed URL citations: 【https://...】
  // 3. Standard markdown links: [text](url)
  // 4. Raw URLs: https://... or http://...
  // 5. Bold: **text** or __text__
  // 6. Italic: *text* or _text_
  // 7. Code: `text`
  const tokenRegex = /(\[(?:\d+(?:[–-]\d+)?(?:,\s*\d+)*)\](?:\[(?:\d+(?:[–-]\d+)?(?:,\s*\d+)*)\])*|【https?:\/\/[^】]+】|\[[^\]]+\]\([^)]+\)|https?:\/\/[^\s<>"'\(\)]+|\*\*[^*]+\*\*|__[^_]+__|(?:\*[^*]+\*|_[^_]+_)|`[^`]+`)/g;
  const parts = text.split(tokenRegex);

  return (
    <>
      {parts.map((part, index) => {
        if (!part) return null;

        // 1. Structured Numeric Inline Citations: [1], [2], [1][2], [2-4], [1, 2]
        const numericCitationMatch = part.match(/^(\[\d+(?:[–-]\d+)?(?:,\s*\d+)*\])+$/);
        if (numericCitationMatch) {
          // Extract individual numeric citation blocks e.g. "[1]" or "[2-4]"
          const matches = part.match(/\[\d+(?:[–-]\d+)?(?:,\s*\d+)*\]/g) || [];
          const citationNumbers: number[] = [];

          matches.forEach((m) => {
            const inner = m.replace(/[\[\]]/g, '');
            if (inner.includes('-') || inner.includes('–')) {
              const range = inner.split(/[–-]/).map((n) => parseInt(n.trim(), 10));
              if (range.length === 2 && !isNaN(range[0]) && !isNaN(range[1])) {
                const start = Math.min(range[0], range[1]);
                const end = Math.max(range[0], range[1]);
                for (let num = start; num <= end; num++) {
                  citationNumbers.push(num);
                }
              }
            } else if (inner.includes(',')) {
              inner.split(',').forEach((n) => {
                const num = parseInt(n.trim(), 10);
                if (!isNaN(num)) citationNumbers.push(num);
              });
            } else {
              const num = parseInt(inner, 10);
              if (!isNaN(num)) citationNumbers.push(num);
            }
          });

          return (
            <span key={index} className="inline-flex items-center">
              {citationNumbers.map((num, i) => (
                <CitationBadge key={i} citationNumber={num} />
              ))}
            </span>
          );
        }

        // 2. Bracketed Citation: 【https://domain.com/path】
        const bracketCitationMatch = part.match(/^【(https?:\/\/[^】]+)】$/);
        if (bracketCitationMatch) {
          const rawUrl = bracketCitationMatch[1];
          let domainName = rawUrl;
          try {
            domainName = new URL(rawUrl).hostname.replace(/^www\./, '');
          } catch {
            domainName = rawUrl;
          }

          return (
            <a
              key={index}
              href={rawUrl}
              target="_blank"
              rel="noopener noreferrer"
              title={rawUrl}
              className="inline-flex items-center gap-1 mx-1 px-1.5 py-0.5 rounded bg-surface-hover hover:bg-surface-elevated text-accent hover:text-accent-hover text-xs font-mono-code border border-accent/30 hover:border-accent/60 transition-all duration-120 cursor-pointer select-none"
            >
              <span>{domainName}</span>
              <ExternalLink className="w-2.5 h-2.5 inline shrink-0 text-accent/80" />
            </a>
          );
        }

        // 3. Standard Link [text](url)
        const linkMatch = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
        if (linkMatch) {
          const [, linkText, url] = linkMatch;
          return (
            <a
              key={index}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent-hover underline underline-offset-2 transition-colors duration-fast cursor-pointer font-medium"
            >
              {linkText}
            </a>
          );
        }

        // 4. Raw URL: https://... or http://...
        if (part.startsWith('http://') || part.startsWith('https://')) {
          return (
            <a
              key={index}
              href={part}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent-hover underline underline-offset-2 transition-colors duration-fast cursor-pointer font-mono-code text-xs break-all"
            >
              {part}
            </a>
          );
        }

        // 5. Bold **text** or __text__
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={index} className="font-semibold text-white">{part.slice(2, -2)}</strong>;
        }
        if (part.startsWith('__') && part.endsWith('__')) {
          return <strong key={index} className="font-semibold text-white">{part.slice(2, -2)}</strong>;
        }

        // 6. Italic *text* or _text_
        if ((part.startsWith('*') && part.endsWith('*')) || (part.startsWith('_') && part.endsWith('_'))) {
          return <em key={index} className="italic text-foreground/90">{part.slice(1, -1)}</em>;
        }

        // 7. Inline Code `code`
        if (part.startsWith('`') && part.endsWith('`')) {
          return (
            <code
              key={index}
              className="font-mono-code text-xs bg-surface-hover text-accent px-1.5 py-0.5 rounded border border-border-subtle/60"
            >
              {part.slice(1, -1)}
            </code>
          );
        }

        // Plain text
        return <React.Fragment key={index}>{part}</React.Fragment>;
      })}
    </>
  );
};
