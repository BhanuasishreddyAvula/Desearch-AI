import React from 'react';
import { Copy } from 'lucide-react';
import type { CodeBlockNode } from '../../utils/markdownParser';

interface CodeBlockProps {
  node: CodeBlockNode;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({ node }) => {
  const { language, code } = node;

  return (
    <div className="my-6 bg-surface-elevated border border-border-subtle rounded-xl overflow-hidden shadow-xs font-mono-code text-xs md:text-sm text-foreground select-text animate-in fade-in duration-150">
      {/* Header Bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-surface-hover/80 border-b border-border-subtle/60 text-xs text-muted-foreground select-none">
        <span className="font-mono-code text-[11px] uppercase tracking-wider text-accent font-medium">
          {language || 'code'}
        </span>
        <button
          type="button"
          disabled
          aria-label="Copy code placeholder"
          title="Copy code"
          className="flex items-center gap-1.5 px-2 py-1 rounded text-[11px] text-muted-foreground hover:text-white transition-colors opacity-70 cursor-not-allowed"
        >
          <Copy className="w-3.5 h-3.5" />
          <span>Copy</span>
        </button>
      </div>

      {/* Code Area */}
      <pre className="p-4 overflow-x-auto leading-relaxed font-mono-code text-white/90 whitespace-pre">
        <code>{code}</code>
      </pre>
    </div>
  );
};
