import { DocumentAST, CoverPageNode, TOCNode, HeadingNode, ParagraphNode, ListNode, TableNode, CodeBlockNode, CalloutNode, ReferenceCardNode } from '../ast';
import { LayoutGrid } from '../typography';

/**
 * Publication Layout Engine — Presentation-Only PDF Renderer (Ticket P4-10)
 * Responsible ONLY for drawing AST nodes onto binary PDF streams.
 * Does NOT perform spacing estimations, markdown parsing, or pagination logic.
 */
export class PDFPresentationRenderer {
  private objects: string[] = [];
  private pageObjectIds: number[] = [];
  private currentStream: string[] = [];
  private pageCount = 0;
  private currentY = 780;

  private escapePdfText(text: string): string {
    return text
      .replace(/\\/g, '\\\\')
      .replace(/\(/g, '\\(')
      .replace(/\)/g, '\\)')
      .replace(/[^\x20-\x7E]/g, '');
  }

  private startPage() {
    if (this.currentStream.length > 0) {
      this.flushPageStream();
    }
    this.pageCount++;
    this.currentY = 780;

    // Draw Running Page Header (Pages 2+)
    if (this.pageCount > 1) {
      this.currentStream.push('0.55 0.54 0.52 rg');
      this.currentStream.push('BT /F1 8 Tf 38 812 Td (Desearch AI | Research Publication) Tj ET');
      this.currentStream.push('0.88 0.86 0.84 RG');
      this.currentStream.push('38 804 m 557 804 l S');

      // Running Page Footer
      this.currentStream.push('0.55 0.54 0.52 rg');
      this.currentStream.push(`BT /F1 8 Tf 265 25 Td (Page ${this.pageCount}) Tj ET`);
      this.currentStream.push('38 35 m 557 35 l S');
    }
  }

  private flushPageStream() {
    const streamContent = this.currentStream.join('\n');
    const streamObj = `${this.objects.length + 3} 0 obj\n<< /Length ${streamContent.length} >>\nstream\n${streamContent}\nendstream\nendobj`;
    this.objects.push(streamObj);

    const pageObj = `${this.objects.length + 3} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R /F4 6 0 R >> >> /Contents ${this.objects.length + 2} 0 R >>\nendobj`;
    this.objects.push(pageObj);
    this.pageObjectIds.push(this.objects.length + 2);
    this.currentStream = [];
  }

  public render(ast: DocumentAST): Blob {
    let activePage = 0;

    ast.nodes.forEach((node) => {
      const pageNum = node.assignedPageNumber || 1;
      while (activePage < pageNum) {
        this.startPage();
        activePage++;
      }

      switch (node.type) {
        case 'cover_page':
          this.drawCoverPage(node as CoverPageNode);
          break;
        case 'toc':
          this.drawTOC(node as TOCNode);
          break;
        case 'heading':
          this.drawHeading(node as HeadingNode);
          break;
        case 'paragraph':
          this.drawParagraph(node as ParagraphNode);
          break;
        case 'list':
          this.drawList(node as ListNode);
          break;
        case 'table':
          this.drawTable(node as TableNode);
          break;
        case 'code_block':
          this.drawCodeBlock(node as CodeBlockNode);
          break;
        case 'callout':
          this.drawCallout(node as CalloutNode);
          break;
        case 'reference_card':
          this.drawReferenceCard(node as ReferenceCardNode);
          break;
      }
    });

    this.flushPageStream();
    return this.assemblePdfBlob();
  }

  private drawCoverPage(node: CoverPageNode) {
    this.currentY = 640;
    this.currentStream.push('0.874 0.341 0.235 rg');
    this.currentStream.push('BT /F2 11 Tf 205 700 Td (DESEARCH AI PUBLICATION) Tj ET');

    this.currentStream.push('0.07 0.07 0.07 rg');
    const titleLines = this.wrapText(node.title, 42);
    let titleY = 640;
    titleLines.forEach((line) => {
      this.currentStream.push(`BT /F2 22 Tf 38 ${titleY} Td (${this.escapePdfText(line)}) Tj ET`);
      titleY -= 28;
    });

    titleY -= 12;
    this.currentStream.push('0.874 0.341 0.235 RG');
    this.currentStream.push(`247.5 ${titleY} m 347.5 ${titleY} l 2 w S 1 w`);

    titleY -= 36;
    this.currentStream.push('0.98 0.97 0.96 rg');
    this.currentStream.push(`110 ${titleY - 75} 375 85 re f`);
    this.currentStream.push('0.88 0.86 0.84 RG');
    this.currentStream.push(`110 ${titleY - 75} 375 85 re S`);

    this.currentStream.push('0.2 0.2 0.2 rg');
    this.currentStream.push(`BT /F1 9.5 Tf 125 ${titleY - 18} Td (Topic: ${this.escapePdfText(node.query || node.title)}) Tj ET`);
    this.currentStream.push(`BT /F1 9.5 Tf 125 ${titleY - 34} Td (Date: ${node.date} | Sources Consulted: ${node.sourcesCount}) Tj ET`);
    this.currentStream.push(`BT /F1 9.5 Tf 125 ${titleY - 50} Td (Publisher: ${this.escapePdfText(node.publisher)}) Tj ET`);
    this.currentStream.push(`BT /F1 9.5 Tf 125 ${titleY - 66} Td (Format: McKinsey / Gartner Research Specification) Tj ET`);
  }

  private drawTOC(node: TOCNode) {
    this.currentStream.push('0.07 0.07 0.07 rg');
    this.currentStream.push('BT /F2 18 Tf 38 760 Td (Table of Contents) Tj ET');
    this.currentStream.push('0.874 0.341 0.235 RG');
    this.currentStream.push('38 748 m 557 748 l S');

    let tocY = 710;
    node.items.forEach((item) => {
      const pageNum = item.targetPageNumber || 3;
      const dots = '.'.repeat(Math.max(10, 72 - item.title.length));
      this.currentStream.push(`BT /F1 9.5 Tf 38 ${tocY} Td (${this.escapePdfText(item.title)} ${dots} Page ${pageNum}) Tj ET`);
      tocY -= 18;
    });
  }

  private drawHeading(node: HeadingNode) {
    this.currentStream.push('0.07 0.07 0.07 rg');
    if (node.level === 1) {
      this.currentStream.push(`BT /F2 17 Tf 38 ${this.currentY} Td (${this.escapePdfText(node.text)}) Tj ET`);
      this.currentY -= 24;
    } else if (node.level === 2) {
      this.currentStream.push(`BT /F2 13.5 Tf 38 ${this.currentY} Td (${this.escapePdfText(node.text)}) Tj ET`);
      this.currentStream.push('0.874 0.341 0.235 RG');
      this.currentStream.push(`38 ${this.currentY - 3} m 557 ${this.currentY - 3} l S`);
      this.currentY -= 20;
    } else {
      this.currentStream.push(`BT /F2 11 Tf 38 ${this.currentY} Td (${this.escapePdfText(node.text)}) Tj ET`);
      this.currentY -= 16;
    }
  }

  private drawParagraph(node: ParagraphNode) {
    const wrapped = this.wrapText(node.text, 84);
    wrapped.forEach((wLine) => {
      this.currentStream.push('0.15 0.15 0.15 rg');
      this.currentStream.push(`BT /F1 9.5 Tf 38 ${this.currentY} Td (${this.escapePdfText(wLine)}) Tj ET`);
      this.currentY -= 13.5;
    });
    this.currentY -= 4;
  }

  private drawList(node: ListNode) {
    node.items.forEach((item) => {
      const bullet = node.ordered ? '1. ' : '• ';
      const wrapped = this.wrapText(bullet + item, 82);
      wrapped.forEach((wLine) => {
        this.currentStream.push('0.15 0.15 0.15 rg');
        this.currentStream.push(`BT /F1 9.5 Tf 48 ${this.currentY} Td (${this.escapePdfText(wLine)}) Tj ET`);
        this.currentY -= 11;
      });
    });
    this.currentY -= 4;
  }

  private drawTable(node: TableNode) {
    const colCount = node.headers.length || 1;
    const colWidth = Math.floor(LayoutGrid.usableWidth / colCount);
    const rowHeight = 22;

    const headerY = this.currentY - rowHeight;
    this.currentStream.push('0.14 0.13 0.12 rg');
    this.currentStream.push(`38 ${headerY} ${LayoutGrid.usableWidth} ${rowHeight} re f`);

    node.headers.forEach((hText, colIdx) => {
      const cellX = 38 + colIdx * colWidth + 6;
      this.currentStream.push('1 1 1 rg');
      this.currentStream.push(`BT /F2 9 Tf ${cellX} ${headerY + 6} Td (${this.escapePdfText(hText.substring(0, 22))}) Tj ET`);
    });

    this.currentY -= rowHeight;

    node.rows.forEach((rowCells, rowIdx) => {
      const rY = this.currentY - rowHeight;
      if (rowIdx % 2 === 1) {
        this.currentStream.push('0.98 0.97 0.96 rg');
        this.currentStream.push(`38 ${rY} ${LayoutGrid.usableWidth} ${rowHeight} re f`);
      }

      this.currentStream.push('0.88 0.86 0.84 RG');
      this.currentStream.push(`38 ${rY} ${LayoutGrid.usableWidth} ${rowHeight} re S`);

      rowCells.forEach((cText, colIdx) => {
        const cellX = 38 + colIdx * colWidth + 6;
        this.currentStream.push('0.15 0.15 0.15 rg');
        this.currentStream.push(`BT /F1 8.5 Tf ${cellX} ${rY + 6} Td (${this.escapePdfText(cText.substring(0, 26))}) Tj ET`);
      });

      this.currentY -= rowHeight;
    });

    this.currentY -= 12;
  }

  private drawCodeBlock(node: CodeBlockNode) {
    const codeLines = node.code.split('\n');
    const h = codeLines.length * 13 + 16;
    this.currentStream.push('0.11 0.10 0.10 rg');
    this.currentStream.push(`38 ${this.currentY - h} ${LayoutGrid.usableWidth} ${h} re f`);

    let cY = this.currentY - 14;
    codeLines.forEach((cLine) => {
      this.currentStream.push('0.98 0.98 0.98 rg');
      this.currentStream.push(`BT /F3 8.5 Tf 48 ${cY} Td (${this.escapePdfText(cLine.substring(0, 85))}) Tj ET`);
      cY -= 13;
    });
    this.currentY -= h + 10;
  }

  private drawCallout(node: CalloutNode) {
    const lines = this.wrapText(node.text, 82);
    const h = lines.length * 13 + 32;

    this.currentStream.push('0.98 0.97 0.96 rg');
    this.currentStream.push(`38 ${this.currentY - h} ${LayoutGrid.usableWidth} ${h} re f`);
    this.currentStream.push('0.874 0.341 0.235 rg');
    this.currentStream.push(`38 ${this.currentY - h} 3.5 ${h} re f`);
    this.currentStream.push('0.874 0.341 0.235 rg');
    this.currentStream.push(`BT /F2 12 Tf 52 ${this.currentY - 16} Td (${this.escapePdfText(node.title)}) Tj ET`);

    let sY = this.currentY - 32;
    lines.forEach((line) => {
      this.currentStream.push('0.2 0.2 0.2 rg');
      this.currentStream.push(`BT /F1 9.5 Tf 52 ${sY} Td (${this.escapePdfText(line)}) Tj ET`);
      sY -= 13;
    });
    this.currentY -= h + 14;
  }

  private drawReferenceCard(node: ReferenceCardNode) {
    const titleText = `[${node.index}] ${node.title}`;
    this.currentStream.push('0.98 0.98 0.98 rg');
    this.currentStream.push(`38 ${this.currentY - 36} ${LayoutGrid.usableWidth} 40 re f`);
    this.currentStream.push('0.88 0.86 0.84 RG');
    this.currentStream.push(`38 ${this.currentY - 36} ${LayoutGrid.usableWidth} 40 re S`);

    this.currentStream.push('0.1 0.1 0.1 rg');
    this.currentStream.push(`BT /F2 9.5 Tf 46 ${this.currentY - 14} Td (${this.escapePdfText(titleText)}) Tj ET`);
    this.currentStream.push('0.874 0.341 0.235 rg');
    this.currentStream.push(`BT /F3 8.5 Tf 46 ${this.currentY - 27} Td (${this.escapePdfText(node.domain)} | ${this.escapePdfText(node.url)}) Tj ET`);
    this.currentY -= 46;
  }

  private wrapText(text: string, maxCharsPerLine: number): string[] {
    const words = text.split(' ');
    const lines: string[] = [];
    let current = '';

    words.forEach((word) => {
      if ((current + word).length > maxCharsPerLine) {
        lines.push(current.trim());
        current = word + ' ';
      } else {
        current += word + ' ';
      }
    });

    if (current.trim()) lines.push(current.trim());
    return lines;
  }

  private assemblePdfBlob(): Blob {
    let pdfStr = `%PDF-1.7\n`;
    pdfStr += `1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n`;
    pdfStr += `2 0 obj\n<< /Type /Pages /Kids [${this.pageObjectIds.map((id) => `${id} 0 R`).join(' ')}] /Count ${this.pageObjectIds.length} >>\nendobj\n`;

    pdfStr += `3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n`;
    pdfStr += `4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n`;
    pdfStr += `5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n`;
    pdfStr += `6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>\nendobj\n`;

    this.objects.forEach((obj) => {
      pdfStr += `${obj}\n`;
    });

    const xrefOffset = pdfStr.length;
    pdfStr += `xref\n0 ${this.objects.length + 7}\n0000000000 65535 f \n`;

    let currentPos = 16;
    pdfStr += `${currentPos.toString().padStart(10, '0')} 00000 n \n`;
    pdfStr += `trailer\n<< /Size ${this.objects.length + 7} /Root 1 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`;

    const encoder = new TextEncoder();
    const byteArray = encoder.encode(pdfStr);
    return new Blob([byteArray], { type: 'application/pdf' });
  }
}
