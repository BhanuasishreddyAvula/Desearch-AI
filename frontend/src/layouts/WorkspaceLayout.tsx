import React, { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { FloatingHeaderActions } from '../components/common/FloatingHeaderActions';
import { ResearchSidebar } from '../features/sessions/components/ResearchSidebar';

export const WorkspaceLayout: React.FC = () => {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const location = useLocation();

  // Listen for toggle-mobile-sidebar custom events emitted by the mobile header button
  useEffect(() => {
    const handleToggle = () => setIsMobileSidebarOpen((prev) => !prev);
    const handleClose = () => setIsMobileSidebarOpen(false);

    window.addEventListener('toggle-mobile-sidebar', handleToggle);
    window.addEventListener('close-mobile-sidebar', handleClose);
    return () => {
      window.removeEventListener('toggle-mobile-sidebar', handleToggle);
      window.removeEventListener('close-mobile-sidebar', handleClose);
    };
  }, []);

  // Auto-close mobile drawer on route navigation
  useEffect(() => {
    setIsMobileSidebarOpen(false);
  }, [location.pathname]);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground relative font-sans-ui">
      {/* Desktop Research Sidebar */}
      <div className="hidden md:flex h-full shrink-0 z-20">
        <ResearchSidebar />
      </div>

      {/* Mobile Research Sidebar Drawer Overlay */}
      {isMobileSidebarOpen && (
        <>
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-xs z-40 md:hidden animate-in fade-in duration-200"
            onClick={() => setIsMobileSidebarOpen(false)}
          />
          <div className="fixed inset-y-0 left-0 z-50 w-72 md:hidden animate-in slide-in-from-left duration-250 shadow-2xl">
            <ResearchSidebar onSelectSession={() => setIsMobileSidebarOpen(false)} />
          </div>
        </>
      )}

      {/* Main Research Workspace Shell (Full Bleed Full Height) */}
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

