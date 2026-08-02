import { DocumentAST, CoverPageNode, HeadingNode, ParagraphNode, ListNode, TableNode, CodeBlockNode, CalloutNode, ReferenceCardNode } from '../ast';

/**
 * Publication Layout Engine — Presentation-Only Markdown Renderer (Ticket P4-10)
 * Renders measured AST nodes into clean GitHub Flavored Markdown (.md).
 */
export class MarkdownPresentationRenderer {
  public render(ast: DocumentAST): Blob {
    let md = `# ${ast.metadata.title}\n\n`;
    md += `> **Desearch AI Intelligence Publication**  \n`;
    md += `> **Topic:** ${ast.metadata.query || ast.metadata.title}  \n`;
    md += `> **Date:** ${ast.metadata.createdAt} | **Duration:** ${ast.metadata.duration} | **Sources:** ${ast.metadata.sourcesCount}  \n\n`;

    ast.nodes.forEach((node) => {
      switch (node.type) {
        case 'cover_page':
        case 'toc':
          // Excluded from raw markdown body to prevent duplicate cover titles
          break;
        case 'callout': {
          const c = node as CalloutNode;
          md += `> ### ${c.title}\n> ${c.text}\n\n`;
          break;
        }
        case 'heading': {
          const h = node as HeadingNode;
          const prefix = '#'.repeat(h.level + 1);
          md += `${prefix} ${h.text}\n\n`;
          break;
        }
        case 'paragraph': {
          const p = node as ParagraphNode;
          md += `${p.text}\n\n`;
          break;
        }
        case 'list': {
          const l = node as ListNode;
          l.items.forEach((item, idx) => {
            const prefix = l.ordered ? `${idx + 1}. ` : `- `;
            md += `${prefix}${item}\n`;
          });
          md += `\n`;
          break;
        }
        case 'table': {
          const tbl = node as TableNode;
          md += `| ${tbl.headers.join(' | ')} |\n`;
          md += `| ${tbl.headers.map(() => '---').join(' | ')} |\n`;
          tbl.rows.forEach((row) => {
            md += `| ${row.join(' | ')} |\n`;
          });
          md += `\n`;
          break;
        }
        case 'code_block': {
          const cb = node as CodeBlockNode;
          md += `\`\`\`${cb.language || ''}\n${cb.code}\n\`\`\`\n\n`;
          break;
        }
        case 'reference_card': {
          const ref = node as ReferenceCardNode;
          md += `### [${ref.index}] ${ref.title}\n`;
          md += `- **Domain:** \`${ref.domain}\`\n`;
          md += `- **Category:** ${ref.category}\n`;
          md += `- **URL:** ${ref.url}\n`;
          if (ref.snippet) md += `- **Evidence:** *${ref.snippet}*\n`;
          md += `\n`;
          break;
        }
      }
    });

    return new Blob([md], { type: 'text/markdown;charset=utf-8' });
  }
}
