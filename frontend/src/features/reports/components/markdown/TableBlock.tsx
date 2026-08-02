import React from 'react';
import type { TableNode } from '../../utils/markdownParser';
import { InlineRenderer } from './InlineRenderer';

interface TableBlockProps {
  node: TableNode;
}

export const TableBlock: React.FC<TableBlockProps> = ({ node }) => {
  const { headers, rows } = node;

  if (!headers.length && !rows.length) {
    return null;
  }

  return (
    <div className="w-full overflow-x-auto my-6 border border-border-subtle rounded-xl shadow-xs select-text animate-in fade-in duration-200">
      <table className="w-full text-left font-sans-ui text-xs md:text-sm border-collapse">
        {headers.length > 0 && (
          <thead>
            <tr className="bg-surface-hover border-b border-border-subtle">
              {headers.map((headerText, idx) => (
                <th
                  key={idx}
                  className="p-3 text-xs font-semibold uppercase tracking-wider text-white border-r border-border-subtle/50 last:border-r-0"
                >
                  <InlineRenderer text={headerText} />
                </th>
              ))}
            </tr>
          </thead>
        )}
        <tbody>
          {rows.map((row, rowIdx) => (
            <tr
              key={rowIdx}
              className="border-b border-border-subtle/40 last:border-b-0 hover:bg-surface/50 transition-colors"
            >
              {row.map((cellText, cellIdx) => (
                <td
                  key={cellIdx}
                  className="p-3 text-foreground/90 border-r border-border-subtle/40 last:border-r-0 leading-relaxed"
                >
                  <InlineRenderer text={cellText} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
