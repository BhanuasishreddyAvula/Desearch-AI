import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { WorkspaceLayout } from '../layouts/WorkspaceLayout';
import { NewResearchView } from '../features/research/components/NewResearchView';
import { SessionView } from '../features/research/components/SessionView';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <WorkspaceLayout />,
    children: [
      {
        index: true,
        element: <NewResearchView />,
      },
      {
        path: 'research',
        element: <NewResearchView />,
      },
      {
        path: 'research/:sessionId',
        element: <SessionView />,
      },
      {
        path: '*',
        element: <Navigate to="/" replace />,
      },
    ],
  },
]);
