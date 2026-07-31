import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../components/common/Header';
import { ResearchSidebar } from '../features/sessions/components/ResearchSidebar';

export const WorkspaceLayout: React.FC = () => {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground">
      {/* Desktop Research Sidebar */}
      <div className="hidden md:block h-full shrink-0">
        <ResearchSidebar />
      </div>

      {/* Main Research Workspace Shell */}
      <div className="flex-1 flex flex-col h-full min-w-0 overflow-hidden">
        <Header />

        <main className="flex-1 overflow-y-auto min-h-0 bg-background">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
