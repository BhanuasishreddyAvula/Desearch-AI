import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, PanelLeftClose, PanelLeftOpen, Compass } from 'lucide-react';
import { cn } from '../../../lib/utils/cn';
import { SessionList } from './SessionList';

export const ResearchSidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const navigate = useNavigate();

  const handleNewResearch = () => {
    navigate('/');
  };

  const toggleCollapse = () => {
    setIsCollapsed((prev) => !prev);
  };

  return (
    <aside
      aria-label="Research navigation sidebar"
      className={cn(
        'bg-sidebar border-r border-border flex flex-col h-full font-sans-ui transition-all duration-200 ease-in-out shrink-0 select-none',
        isCollapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Brand & Collapse Header */}
      <div className="h-14 px-4 border-b border-border-subtle flex items-center justify-between">
        {!isCollapsed ? (
          <>
            <div className="flex items-center gap-2">
              <Compass className="w-5 h-5 text-accent shrink-0" />
              <span className="font-serif-editorial font-bold text-lg text-foreground tracking-tight">
                Desearch AI
              </span>
            </div>
            <button
              type="button"
              onClick={toggleCollapse}
              aria-label="Collapse sidebar"
              title="Collapse sidebar"
              className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors focus:outline-none focus:ring-2 focus:ring-focus-ring"
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
          </>
        ) : (
          <div className="w-full flex items-center justify-between px-0.5">
            <Compass className="w-5 h-5 text-accent shrink-0" />
            <button
              type="button"
              onClick={toggleCollapse}
              aria-label="Expand sidebar"
              title="Expand sidebar"
              className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors focus:outline-none focus:ring-2 focus:ring-focus-ring"
            >
              <PanelLeftOpen className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>

      {/* Primary + New Research CTA Button */}
      <div className="p-3">
        <button
          type="button"
          onClick={handleNewResearch}
          aria-label="Start new research"
          title="Start new research"
          className={cn(
            'w-full flex items-center justify-center gap-2 bg-accent hover:bg-accent-hover text-accent-foreground font-medium py-2 rounded-md transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-focus-ring text-xs',
            isCollapsed ? 'px-2' : 'px-3'
          )}
        >
          <Plus className="w-4 h-4 shrink-0" />
          {!isCollapsed && <span>+ New Research</span>}
        </button>
      </div>

      {/* Session History Section — Expanded Only */}
      {!isCollapsed && (
        <nav aria-label="Recent research sessions" className="flex-1 overflow-y-auto px-3 py-2">
          <h2 className="text-[10px] uppercase font-semibold text-text-muted tracking-wider px-2 mb-2">
            Recent Research
          </h2>
          <SessionList isCollapsed={false} />
        </nav>
      )}
    </aside>
  );
};
