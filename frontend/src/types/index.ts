/**
 * Desearch AI Frontend Domain Types
 * Single source of truth for frontend domain schemas aligned with FastAPI backend.
 */

export interface BaseResponse<T> {
  success: boolean;
  message: string;
  request_id?: string;
  data: T;
  metadata?: Record<string, unknown>;
}

export type SessionStatus =
  | 'CREATED'
  | 'PLANNING'
  | 'RESEARCHING'
  | 'WRITING'
  | 'REVIEWING'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED'
  | 'DRAFT';

export type ProgressEventType =
  | 'workflow.started'
  | 'planner.started'
  | 'planner.completed'
  | 'research.started'
  | 'research.searching'
  | 'research.extracting'
  | 'research.completed'
  | 'writer.started'
  | 'writer.completed'
  | 'reviewer.started'
  | 'reviewer.completed'
  | 'report.persisted'
  | 'workflow.completed'
  | 'workflow.failed';

export interface ProgressEvent {
  event_type: ProgressEventType;
  stage: string;
  message: string;
  session_id: string;
  progress: number;
  timestamp: string;
  metadata?: Record<string, unknown>;
  step_name?: string;
  error_details?: string;
  data?: Record<string, unknown>;
}

export interface ResearchSession {
  id: string;
  title: string;
  query?: string;
  status: SessionStatus;
  created_at: string;
  updated_at: string;
  metadata?: Record<string, unknown>;
}

export interface SessionListResponseData {
  sessions: ResearchSession[];
  total: number;
}

export interface ReportSource {
  url: string;
  title: string;
  snippet?: string;
  domain?: string;
}

export interface ReportResult {
  session_id: string;
  title: string;
  executive_summary?: string;
  full_markdown: string;
  sources_cited?: ReportSource[];
  sections?: Array<{ title: string; content: string; level: number }>;
  metadata?: Record<string, unknown>;
  created_at?: string;
}

export type ExportFormat = 'pdf' | 'markdown';

export interface ApiErrorEnvelope {
  status_code: number;
  message: string;
  error_code?: string;
  detail?: string;
  request_id?: string;
}
