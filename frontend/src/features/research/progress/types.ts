import type { ProgressEventType } from '../../../types';

export type StageId = 'planning' | 'searching' | 'reading' | 'writing' | 'reviewing';
export type StageStatus = 'pending' | 'active' | 'completed';

export interface ProgressStage {
  id: StageId;
  label: string;
  status: StageStatus;
  detail?: string;
}

export type StreamStatus = 'idle' | 'streaming' | 'completed' | 'cancelled' | 'failed' | 'error';

export interface ProgressState {
  sessionId: string;
  status: StreamStatus;
  stages: Record<StageId, ProgressStage>;
  activeStageId: StageId | null;
  sources: string[];
  error: string | null;
  progressPercentage: number;
  totalExecutionTimeMs?: number;
}
