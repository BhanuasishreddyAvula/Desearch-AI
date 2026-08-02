import { DocumentAST, CoverPageNode, TOCNode, HeadingNode, ParagraphNode, ListNode, TableNode, CodeBlockNode, CalloutNode, ReferenceCardNode } from '../ast';

/**
 * Publication Layout Engine — Presentation-Only DOCX Renderer (Ticket P4-10)
 * Renders measured & paginated Document AST into native Word document payload.
 */
export class DocxPresentationRenderer {
  public render(ast: DocumentAST): Blob {
    let htmlContent = `
      <html xmlns:o='urn:schemas-microsoft-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
        <meta charset='utf-8'>
        <title>${ast.metadata.title}</title>
        <style>
          body { font-family: 'Calibri', 'Inter', sans-serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; margin: 1in; }
          .cover-page { text-align: center; padding: 40pt 0 60pt 0; page-break-after: always; }
          .cover-title { font-family: 'Georgia', serif; font-size: 26pt; font-weight: normal; color: #111; margin-bottom: 24pt; line-height: 1.25; }
          .cover-divider { width: 80pt; border-bottom: 2pt solid #DF573C; margin: 20pt auto; }
          .cover-meta { font-size: 10pt; color: #555; line-height: 1.8; }
          h2 { font-family: 'Georgia', serif; font-size: 16pt; color: #DF573C; border-bottom: 1.5pt solid #DF573C; padding-bottom: 4pt; margin-top: 24pt; }
          h3 { font-family: 'Georgia', serif; font-size: 13pt; color: #222; margin-top: 16pt; }
          .exec-callout { background: #faf8f5; border: 1pt solid #e8e4df; border-left: 3pt solid #DF573C; padding: 14pt; margin: 16pt 0; border-radius: 4pt; }
          table { width: 100%; border-collapse: collapse; margin: 14pt 0; font-size: 10pt; }
          th { background: #2b2b2b; color: #ffffff; padding: 8pt; text-align: left; }
          td { border: 1pt solid #dee2e6; padding: 7pt; }
          tr:nth-child(even) { background: #f8f9fa; }
          pre { background: #1b1a19; color: #fbf9f5; padding: 10pt; font-family: 'Consolas', monospace; font-size: 9pt; border-radius: 4pt; }
          .ref-card { background: #fdfdfd; border: 1pt solid #e0deda; border-radius: 6pt; padding: 10pt 12pt; margin-bottom: 10pt; }
          .ref-title { font-weight: bold; color: #111; font-size: 10.5pt; }
          .ref-domain { color: #DF573C; font-size: 9.5pt; font-family: monospace; }
          .footer { font-size: 8.5pt; color: #777; border-top: 1pt solid #ddd; padding-top: 8pt; margin-top: 30pt; text-align: center; }
        </style>
      </head>
      <body>
    `;

    ast.nodes.forEach((node) => {
      switch (node.type) {
        case 'cover_page': {
          const c = node as CoverPageNode;
          htmlContent += `
            <div className="cover-page">
              <p style="font-size:12pt; color:#DF573C; font-weight:bold; letter-spacing:1pt;">DESEARCH AI RESEARCH PUBLICATION</p>
              <div className="cover-title">${c.title}</div>
              <div className="cover-divider"></div>
              <div className="cover-meta">
                <strong>Research Topic:</strong> ${c.query || c.title}<br/>
                <strong>Generation Date:</strong> ${c.date}<br/>
                <strong>Research Duration:</strong> ${c.duration}<br/>
                <strong>Total Sources Consulted:</strong> ${c.sourcesCount}<br/>
                <strong>Publisher:</strong> ${c.publisher}
              </div>
            </div>
          `;
          break;
        }
        case 'toc': {
          const t = node as TOCNode;
          htmlContent += `<h2>Table of Contents</h2><ul>`;
          t.items.forEach((item) => {
            htmlContent += `<li>${item.title} .................... Page ${item.targetPageNumber || 3}</li>`;
          });
          htmlContent += `</ul>`;
          break;
        }
        case 'heading': {
          const h = node as HeadingNode;
          htmlContent += `<h${h.level}>${h.text}</h${h.level}>`;
          break;
        }
        case 'paragraph': {
          const p = node as ParagraphNode;
          htmlContent += `<p>${p.text}</p>`;
          break;
        }
        case 'list': {
          const l = node as ListNode;
          const tag = l.ordered ? 'ol' : 'ul';
          htmlContent += `<${tag}>`;
          l.items.forEach((item) => {
            htmlContent += `<li>${item}</li>`;
          });
          htmlContent += `</${tag}>`;
          break;
        }
        case 'table': {
          const tbl = node as TableNode;
          htmlContent += `<table><thead><tr>`;
          tbl.headers.forEach((hdr) => {
            htmlContent += `<th>${hdr}</th>`;
          });
          htmlContent += `</tr></thead><tbody>`;
          tbl.rows.forEach((row) => {
            htmlContent += `<tr>`;
            row.forEach((cell) => {
              htmlContent += `<td>${cell}</td>`;
            });
            htmlContent += `</tr>`;
          });
          htmlContent += `</tbody></table>`;
          break;
        }
        case 'code_block': {
          const codeNode = node as CodeBlockNode;
          htmlContent += `<pre><code>${codeNode.code}</code></pre>`;
          break;
        }
        case 'callout': {
          const callout = node as CalloutNode;
          htmlContent += `<div className="exec-callout"><h3>${callout.title}</h3><p>${callout.text}</p></div>`;
          break;
        }
        case 'reference_card': {
          const refNode = node as ReferenceCardNode;
          htmlContent += `
            <div className="ref-card">
              <span className="ref-title">[${refNode.index}] ${refNode.title}</span><br/>
              <span className="ref-domain">${refNode.domain}</span> | <span>${refNode.category}</span><br/>
              <a href="${refNode.url}">${refNode.url}</a>
              ${refNode.snippet ? `<br/><small style="color:#666;"><em>"${refNode.snippet}"</em></small>` : ''}
            </div>
          `;
          break;
        }
      }
    });

    htmlContent += `
        <div className="footer">
          Generated by Desearch AI | ${ast.metadata.createdAt}
        </div>
      </body>
      </html>
    `;

    return new Blob([htmlContent], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  }
}
