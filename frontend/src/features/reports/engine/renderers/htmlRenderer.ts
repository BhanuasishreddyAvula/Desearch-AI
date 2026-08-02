import { DocumentAST, CoverPageNode, TOCNode, HeadingNode, ParagraphNode, ListNode, TableNode, CodeBlockNode, ExecSummaryCardNode, ReferenceCardNode, DocumentMetadataNode } from '../ast';

/**
 * Publication Quality Report System — Presentation-Only HTML Renderer (Ticket P4-11)
 * Renders measured & paginated Document AST into clean responsive HTML publication markup.
 */
export class HTMLPresentationRenderer {
  public render(ast: DocumentAST): Blob {
    let html = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>${ast.metadata.title}</title>
        <style>
          body { font-family: 'Inter', system-ui, sans-serif; line-height: 1.6; color: #1a1a19; background: #faf9f6; margin: 0; padding: 40px 20px; }
          .container { max-width: 760px; margin: 0 auto; background: #ffffff; border: 1px solid #e5e2dc; border-radius: 12px; padding: 48px; box-shadow: 0 4px 24px rgba(0,0,0,0.04); }
          .cover-brand { font-family: Georgia, serif; font-size: 13px; text-transform: uppercase; color: #DF573C; letter-spacing: 2px; font-weight: 600; text-align: center; }
          .cover-title { font-family: Georgia, serif; font-size: 32px; font-weight: 400; text-align: center; margin: 20px 0 12px 0; color: #111; }
          .cover-subtitle { font-size: 14px; text-align: center; color: #666; max-width: 580px; margin: 0 auto 24px auto; line-height: 1.5; }
          .cover-divider { width: 60px; height: 2px; background: #DF573C; margin: 20px auto 32px auto; }
          .cover-meta { background: #faf8f5; border: 1px solid #e8e4df; border-radius: 8px; padding: 16px 20px; font-size: 13px; color: #444; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 40px; }
          h1, h2, h3 { font-family: Georgia, serif; color: #111; }
          h1 { font-size: 26px; border-bottom: 2px solid #DF573C; padding-bottom: 8px; margin-top: 40px; }
          h2 { font-size: 20px; border-bottom: 1px solid #DF573C; padding-bottom: 6px; margin-top: 32px; }
          h3 { font-size: 16px; margin-top: 24px; }
          .exec-card { background: #faf8f5; border-left: 4px solid #DF573C; border-radius: 8px; padding: 20px 24px; margin: 24px 0; }
          .exec-card h3 { margin-top: 0; color: #DF573C; }
          table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #e2dfd9; border-radius: 8px; overflow: hidden; margin: 20px 0; font-size: 13px; }
          th { background: #23211f; color: #fff; padding: 10px 14px; text-align: left; }
          td { border-bottom: 1px solid #ebe8e3; padding: 10px 14px; }
          tr:nth-child(even) td { background: #faf8f5; }
          pre { background: #1b1a19; color: #fbf9f5; padding: 16px; border-radius: 8px; font-family: monospace; font-size: 13px; overflow-x: auto; }
          .ref-card { background: #faf8f5; border: 1px solid #e5e2dc; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; }
          .ref-title { font-weight: 600; font-size: 14px; color: #111; }
          .ref-url { font-size: 12px; color: #DF573C; text-decoration: none; word-break: break-all; }
          .doc-footer { margin-top: 48px; border-top: 1px solid #e8e4df; padding-top: 20px; font-size: 12px; color: #777; text-align: center; }
        </style>
      </head>
      <body>
        <div className="container">
    `;

    ast.nodes.forEach((node) => {
      switch (node.type) {
        case 'cover_page': {
          const c = node as CoverPageNode;
          html += `
            <div className="cover-brand">DESEARCH AI PUBLICATION</div>
            <div className="cover-title">${c.title}</div>
            <div className="cover-subtitle">${c.subtitle}</div>
            <div className="cover-divider"></div>
            <div className="cover-meta">
              <div><strong>Report ID:</strong> ${c.reportId}</div>
              <div><strong>Publication Date:</strong> ${c.date}</div>
              <div><strong>Research Duration:</strong> ${c.duration}</div>
              <div><strong>Total Sources:</strong> ${c.sourcesCount}</div>
              <div><strong>Reading Time:</strong> ${c.readingTime}</div>
              <div><strong>Version:</strong> ${c.version}</div>
            </div>
          `;
          break;
        }
        case 'toc': {
          const t = node as TOCNode;
          html += `<h2>Table of Contents</h2><ul>`;
          t.items.forEach((item) => {
            html += `<li>${item.title} .................... Page ${item.targetPageNumber || 3}</li>`;
          });
          html += `</ul>`;
          break;
        }
        case 'exec_summary_card': {
          const exec = node as ExecSummaryCardNode;
          html += `
            <div className="exec-card">
              <h3>Executive Summary</h3>
              <p>${exec.summary}</p>
              <strong>Key Takeaways:</strong>
              <ul>
                ${exec.keyTakeaways.map((k) => `<li>${k}</li>`).join('')}
              </ul>
            </div>
          `;
          break;
        }
        case 'heading': {
          const h = node as HeadingNode;
          html += `<h${h.level}>${h.text}</h${h.level}>`;
          break;
        }
        case 'paragraph': {
          const p = node as ParagraphNode;
          html += `<p>${p.text}</p>`;
          break;
        }
        case 'list': {
          const l = node as ListNode;
          const tag = l.ordered ? 'ol' : 'ul';
          html += `<${tag}>${l.items.map((i) => `<li>${i}</li>`).join('')}</${tag}>`;
          break;
        }
        case 'table': {
          const tbl = node as TableNode;
          html += `<table><thead><tr>${tbl.headers.map((hdr) => `<th>${hdr}</th>`).join('')}</tr></thead><tbody>`;
          tbl.rows.forEach((row) => {
            html += `<tr>${row.map((cell) => `<td>${cell}</td>`).join('')}</tr>`;
          });
          html += `</tbody></table>`;
          break;
        }
        case 'code_block': {
          const cb = node as CodeBlockNode;
          html += `<pre><code>${cb.code}</code></pre>`;
          break;
        }
        case 'reference_card': {
          const ref = node as ReferenceCardNode;
          html += `
            <div className="ref-card">
              <div className="ref-title">[${ref.index}] ${ref.title}</div>
              <div style="font-size:12px; color:#666; margin:4px 0;">Domain: ${ref.domain} | Category: ${ref.category}</div>
              <a href="${ref.url}" className="ref-url" target="_blank">${ref.url}</a>
              ${ref.snippet ? `<div style="font-size:12px; color:#666; margin-top:4px;"><em>"${ref.snippet}"</em></div>` : ''}
            </div>
          `;
          break;
        }
        case 'document_metadata': {
          const meta = node as DocumentMetadataNode;
          html += `
            <div className="doc-footer">
              Generated by Desearch AI Engine • ${meta.engineVersion} • ${meta.generationDate} • Word Count: ${meta.wordCount}
            </div>
          `;
          break;
        }
      }
    });

    html += `
        </div>
      </body>
      </html>
    `;

    return new Blob([html], { type: 'text/html;charset=utf-8' });
  }
}
