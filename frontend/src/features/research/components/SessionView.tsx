import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { sessionsApi } from '../../../lib/api/sessions';
import { FileText, Clock, AlertCircle } from 'lucide-react';

export const SessionView: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();

  const { data: session, isLoading, isError } = useQuery({
    queryKey: ['session', sessionId],
    queryFn: ({ signal }) => sessionsApi.getSession(sessionId!, signal),
    enabled: Boolean(sessionId),
  });

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto py-12 px-4 space-y-4 font-sans-ui">
        <div className="h-6 w-3/4 rounded bg-surface/60 animate-pulse" />
        <div className="h-4 w-1/2 rounded bg-surface/40 animate-pulse" />
      </div>
    );
  }

  if (isError || !session) {
    return (
      <div className="max-w-md mx-auto my-16 p-6 rounded-lg bg-surface border border-border text-center space-y-3 font-sans-ui">
        <AlertCircle className="w-8 h-8 text-destructive mx-auto" />
        <h2 className="text-base font-medium text-foreground">Session Not Found</h2>
        <p className="text-xs text-muted-foreground">
          The requested research session could not be retrieved from the server.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 font-sans-ui space-y-6">
      {/* Session Title Header */}
      <div className="border-b border-border pb-4 space-y-2">
        <div className="flex items-center gap-2 text-xs font-mono-code text-muted-foreground">
          <Clock className="w-3.5 h-3.5 text-accent" />
          <span>Session ID: {session.id}</span>
          <span className="px-2 py-0.5 rounded bg-surface border border-border-subtle text-foreground text-[10px]">
            {session.status}
          </span>
        </div>
        <h1 className="font-serif-editorial text-2xl md:text-3xl font-semibold text-foreground tracking-tight">
          {session.title || session.query}
        </h1>
      </div>

      {/* Workspace Placeholder Banner */}
      <div className="p-4 rounded-lg bg-surface border border-border-subtle flex items-start gap-3">
        <FileText className="w-5 h-5 text-accent shrink-0 mt-0.5" />
        <div className="space-y-1 text-xs text-muted-foreground">
          <p className="text-foreground font-medium">Research Workspace Shell (Session Active)</p>
          <p>
            Real-time SSE progress streaming (P3-04) and synthesized markdown report renderer (P3-05) will populate this reading area.
          </p>
        </div>
      </div>
    </div>
  );
};
