/**
 * Publication Layout Engine — Typography Tokens & Spacing System (Ticket P4-10)
 * Centralized typography hierarchy. Renderers must consume these tokens instead of guessing font sizes or margins.
 */

export interface TypographyToken {
  fontFamily: 'Helvetica' | 'Helvetica-Bold' | 'Courier' | 'Times-Roman';
  fontSize: number;       // In points (pt)
  lineHeight: number;     // Multiplier e.g. 1.3
  marginTop: number;      // Spacing above in pt
  marginBottom: number;   // Spacing below in pt
  color: string;          // PDF RGB hex or array
}

export const TypographySystem: Record<string, TypographyToken> = {
  coverTitle: {
    fontFamily: 'Helvetica-Bold',
    fontSize: 22,
    lineHeight: 1.25,
    marginTop: 0,
    marginBottom: 24,
    color: '0.07 0.07 0.07',
  },
  coverSubtitle: {
    fontFamily: 'Helvetica',
    fontSize: 11,
    lineHeight: 1.4,
    marginTop: 0,
    marginBottom: 16,
    color: '0.874 0.341 0.235',
  },
  heading1: {
    fontFamily: 'Helvetica-Bold',
    fontSize: 17,
    lineHeight: 1.3,
    marginTop: 18,
    marginBottom: 10,
    color: '0.07 0.07 0.07',
  },
  heading2: {
    fontFamily: 'Helvetica-Bold',
    fontSize: 13.5,
    lineHeight: 1.3,
    marginTop: 16,
    marginBottom: 8,
    color: '0.07 0.07 0.07',
  },
  heading3: {
    fontFamily: 'Helvetica-Bold',
    fontSize: 11,
    lineHeight: 1.3,
    marginTop: 12,
    marginBottom: 6,
    color: '0.15 0.15 0.15',
  },
  body: {
    fontFamily: 'Helvetica',
    fontSize: 9.5,
    lineHeight: 1.45,
    marginTop: 0,
    marginBottom: 7,
    color: '0.15 0.15 0.15',
  },
  listItem: {
    fontFamily: 'Helvetica',
    fontSize: 9.5,
    lineHeight: 1.4,
    marginTop: 0,
    marginBottom: 3.5,
    color: '0.15 0.15 0.15',
  },
  tableHeader: {
    fontFamily: 'Helvetica-Bold',
    fontSize: 9,
    lineHeight: 1.2,
    marginTop: 0,
    marginBottom: 0,
    color: '1 1 1',
  },
  tableCell: {
    fontFamily: 'Helvetica',
    fontSize: 8.5,
    lineHeight: 1.3,
    marginTop: 0,
    marginBottom: 0,
    color: '0.15 0.15 0.15',
  },
  code: {
    fontFamily: 'Courier',
    fontSize: 8.5,
    lineHeight: 1.4,
    marginTop: 10,
    marginBottom: 10,
    color: '0.98 0.98 0.98',
  },
  caption: {
    fontFamily: 'Helvetica',
    fontSize: 8,
    lineHeight: 1.3,
    marginTop: 4,
    marginBottom: 8,
    color: '0.55 0.54 0.52',
  },
};

export const LayoutGrid = {
  pageWidth: 595,     // A4 width pt
  pageHeight: 842,    // A4 height pt
  marginX: 38,        // 18mm side margin
  marginTop: 45,
  marginBottom: 45,
  usableWidth: 519,   // 595 - 38*2
  usableHeight: 752,  // 842 - 45*2
};
