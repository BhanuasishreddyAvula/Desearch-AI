import React from 'react';
import { FileText, Printer, Globe } from 'lucide-react';
import { cn } from '../../../../lib/utils/cn';
import {
  exportAsPDF,
  exportAsMarkdown,
  exportAsHTML,
  ExportSourceItem,
} from '../../utils/exportEngine';

interface ExportMenuProps {
  markdownContent: string;
  title?: string;
  sources?: ExportSourceItem[];
  onClose: () => void;
  position?: 'top' | 'bottom';
}

export const ExportMenu: React.FC<ExportMenuProps> = ({
  markdownContent,
  title = 'Research Report',
  sources = [],
  onClose,
  position = 'top',
}) => {
  const exportData = {
    title,
    fullMarkdown: markdownContent,
    sources,
    createdAt: new Date().toISOString(),
  };

  const handleExportPDF = () => {
    exportAsPDF(exportData);
    onClose();
  };

  const handleExportHTML = () => {
    exportAsHTML(exportData);
    onClose();
  };

  const handleExportMarkdown = () => {
    exportAsMarkdown(exportData);
    onClose();
  };

  return (
    <div
      role="menu"
      aria-label="Export report menu"
      className={cn(
        'absolute right-0 z-40 w-52 bg-surface/95 backdrop-blur-md border border-border-subtle/90 rounded-2xl p-1.5 shadow-2xl font-sans-ui text-left select-none animate-popover-in',
        position === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'
      )}
    >
      <div className="px-2.5 py-1 text-[10px] font-mono-code uppercase tracking-wider text-muted-foreground/60 border-b border-border-subtle/40 mb-1">
        Export Publication
      </div>

      <button
        type="button"
        role="menuitem"
        onClick={handleExportPDF}
        className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-xl hover:bg-surface-hover text-xs font-medium text-foreground/90 hover:text-white transition-colors duration-fast cursor-pointer"
      >
        <Printer className="w-4 h-4 text-accent shrink-0" />
        <span>Publication PDF</span>
      </button>

      <button
        type="button"
        role="menuitem"
        onClick={handleExportHTML}
        className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-xl hover:bg-surface-hover text-xs font-medium text-foreground/90 hover:text-white transition-colors duration-fast cursor-pointer"
      >
        <Globe className="w-4 h-4 text-accent shrink-0" />
        <span>HTML Web Document</span>
      </button>

      <button
        type="button"
        role="menuitem"
        onClick={handleExportMarkdown}
        className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-xl hover:bg-surface-hover text-xs font-medium text-foreground/90 hover:text-white transition-colors duration-fast cursor-pointer"
      >
        <FileText className="w-4 h-4 text-accent shrink-0" />
        <span>Markdown (.md)</span>
      </button>
    </div>
  );
};
