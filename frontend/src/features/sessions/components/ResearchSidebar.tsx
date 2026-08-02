import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PanelLeft, SquarePen } from 'lucide-react';
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
        'bg-sidebar border-r border-border flex flex-col h-full font-sans-ui shrink-0 select-none overflow-hidden transition-[width] duration-240 ease-[cubic-bezier(0.4,0,0.2,1)]',
        isCollapsed ? 'w-[52px]' : 'w-64'
      )}
    >
      {/* Sidebar Header */}
      <div className={cn(
        'h-14 border-b border-border-subtle/50 flex items-center justify-between overflow-hidden transition-all duration-240',
        isCollapsed ? 'px-2' : 'px-3'
      )}>
        {/* Brand Container */}
        <div
          className={cn(
            'flex items-center whitespace-nowrap overflow-hidden transition-all duration-200 ease-out',
            isCollapsed ? 'max-w-0 opacity-0 pointer-events-none' : 'max-w-[180px] opacity-100'
          )}
        >
          <span className="font-serif-editorial font-bold text-xl text-white tracking-tight truncate">
            Desearch AI
          </span>
        </div>


        {/* Sidebar Toggle Button */}
        <button
          type="button"
          onClick={toggleCollapse}
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          className={cn(
            'w-8 h-8 flex items-center justify-center rounded-lg text-white hover:bg-surface-hover active:bg-surface-elevated active:scale-[0.98] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring shrink-0',
            isCollapsed && 'mx-auto'
          )}
        >
          <PanelLeft className="w-4 h-4 text-white" />
        </button>
      </div>

      {/* New Research Action (Slim Stable Anchor Layout) */}
      <div className={cn('transition-all duration-240', isCollapsed ? 'px-[9px] py-3' : 'px-3 py-3')}>
        <button
          type="button"
          onClick={handleNewResearch}
          aria-label="New Research"
          title="New Research"
          className="w-full flex items-center h-9 px-1.5 rounded-lg text-white hover:bg-surface-hover active:bg-surface-elevated active:scale-[0.98] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-focus-ring text-sm font-medium overflow-hidden"
        >
          {/* Icon Slot: Fixed X-coordinate anchor centered in 52px rail */}
          <div className="w-5 h-5 flex items-center justify-center shrink-0 text-white">
            <SquarePen className="w-4 h-4 text-white" />
          </div>

          {/* Label Slot: Smooth horizontal reveal/hide without shifting icon */}
          <span
            className={cn(
              'whitespace-nowrap transition-all duration-200 ease-out overflow-hidden text-foreground/90 font-medium',
              isCollapsed ? 'max-w-0 opacity-0 ml-0 pointer-events-none' : 'max-w-[160px] opacity-100 ml-2.5'
            )}
          >
            New Research
          </span>
        </button>
      </div>

      {/* Session History Section */}
      <nav
        aria-label="Recent research sessions"
        className={cn(
          'flex-1 overflow-y-auto px-3 py-2 transition-opacity duration-200',
          isCollapsed ? 'opacity-0 pointer-events-none hidden' : 'opacity-100'
        )}
      >
        <SessionList isCollapsed={isCollapsed} />
      </nav>
    </aside>
  );
};
