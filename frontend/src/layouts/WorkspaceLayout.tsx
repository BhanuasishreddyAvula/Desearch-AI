import React from 'react';
import { Outlet } from 'react-router-dom';
import { FloatingHeaderActions } from '../components/common/FloatingHeaderActions';
import { ResearchSidebar } from '../features/sessions/components/ResearchSidebar';

export const WorkspaceLayout: React.FC = () => {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground relative font-sans-ui">
      {/* Desktop Research Sidebar */}
      <div className="hidden md:block h-full shrink-0 z-20">
        <ResearchSidebar />
      </div>

      {/* Main Research Workspace Shell (Full Bleed Full Height, Header Removed) */}
      <div className="flex-1 flex flex-col h-full min-w-0 overflow-hidden relative">
        {/* Floating Top Right Reports Button */}
        <FloatingHeaderActions />

        {/* Full-Height Content Canvas */}
        <main className="flex-1 h-full min-h-0 bg-background overflow-hidden relative">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
