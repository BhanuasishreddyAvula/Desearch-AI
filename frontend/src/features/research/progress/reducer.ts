import type { ProgressEvent } from '../../../types';
import type { ProgressState, StageId, StreamStatus } from './types';

export function createInitialProgressState(
  sessionId: string,
  initialStatus: StreamStatus = 'idle'
): ProgressState {
  const isCompleted = initialStatus === 'completed';
  const isFailed = initialStatus === 'failed';

  return {
    sessionId,
    status: initialStatus,
    activeStageId: initialStatus === 'streaming' ? 'planning' : null,
    sources: [],
    error: null,
    progressPercentage: isCompleted ? 100 : 0,
    stages: {
      planning: {
        id: 'planning',
        label: 'Planning research...',
        status: isCompleted ? 'completed' : 'pending',
      },
      searching: {
        id: 'searching',
        label: 'Searching sources...',
        status: isCompleted ? 'completed' : 'pending',
      },
      reading: {
        id: 'reading',
        label: 'Extracting content...',
        status: isCompleted ? 'completed' : 'pending',
      },
      writing: {
        id: 'writing',
        label: 'Drafting report...',
        status: isCompleted ? 'completed' : 'pending',
      },
      reviewing: {
        id: 'reviewing',
        label: 'Verifying report...',
        status: isCompleted ? 'completed' : 'pending',
      },
    },
  };
}

export type ProgressAction =
  | { type: 'EVENT_RECEIVED'; event: ProgressEvent }
  | { type: 'TRANSPORT_ERROR'; error: string }
  | { type: 'SET_COMPLETED' }
  | { type: 'SET_CANCELLED' }
  | { type: 'RESET'; sessionId: string };

export function progressReducer(state: ProgressState, action: ProgressAction): ProgressState {
  switch (action.type) {
    case 'RESET':
      return createInitialProgressState(action.sessionId, 'idle');

    case 'SET_COMPLETED':
      return {
        ...state,
        status: 'completed',
        activeStageId: null,
        progressPercentage: 100,
        stages: {
          planning: { ...state.stages.planning, status: 'completed' },
          searching: { ...state.stages.searching, status: 'completed' },
          reading: { ...state.stages.reading, status: 'completed' },
          writing: { ...state.stages.writing, status: 'completed' },
          reviewing: { ...state.stages.reviewing, status: 'completed' },
        },
      };

    case 'SET_CANCELLED':
      // User explicitly stopped the research — keep stage states as-is (don't fake completion)
      return {
        ...state,
        status: 'cancelled',
        activeStageId: null,
      };


    case 'TRANSPORT_ERROR':
      return {
        ...state,
        status: 'error',
        activeStageId: null,
        error: action.error,
      };

    case 'EVENT_RECEIVED': {
      const { event } = action;
      const metadata = event.metadata || {};

      switch (event.event_type) {
        case 'workflow.started':
          return {
            ...state,
            status: 'streaming',
            activeStageId: 'planning',
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'active' },
            },
          };

        case 'planner.started':
          return {
            ...state,
            status: 'streaming',
            activeStageId: 'planning',
            progressPercentage: 5,
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'active' },
            },
          };

        case 'planner.completed':
          return {
            ...state,
            progressPercentage: 15,
            stages: {
              ...state.stages,
              planning: {
                ...state.stages.planning,
                status: 'completed',
                detail: metadata.tasks_count ? `${metadata.tasks_count} tasks planned` : undefined,
              },
            },
          };

        case 'research.started':
          return {
            ...state,
            activeStageId: 'searching',
            progressPercentage: 20,
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'completed' },
              searching: { ...state.stages.searching, status: 'active' },
            },
          };

        case 'research.searching': {
          return {
            ...state,
            activeStageId: 'searching',
            progressPercentage: 25,
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'completed' },
              searching: {
                ...state.stages.searching,
                status: 'active',
                detail: metadata.query ? `Searching '${metadata.query}'` : undefined,
              },
            },
          };
        }

        case 'research.extracting': {
          let updatedSources = [...state.sources];
          if (typeof metadata.url === 'string') {
            try {
              const domain = new URL(metadata.url).hostname.replace(/^www\./, '');
              if (domain && !updatedSources.includes(domain) && updatedSources.length < 15) {
                updatedSources.push(domain);
              }
            } catch {
              // ignore invalid URL
            }
          }

          return {
            ...state,
            activeStageId: 'reading',
            progressPercentage: 40,
            sources: updatedSources,
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'completed' },
              searching: { ...state.stages.searching, status: 'completed' },
              reading: { ...state.stages.reading, status: 'active' },
            },
          };
        }

        case 'research.completed':
          return {
            ...state,
            progressPercentage: 60,
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'completed' },
              searching: { ...state.stages.searching, status: 'completed' },
              reading: { ...state.stages.reading, status: 'completed' },
            },
          };

        case 'writer.started':
          return {
            ...state,
            activeStageId: 'writing',
            progressPercentage: 65,
            stages: {
              ...state.stages,
              planning: { ...state.stages.planning, status: 'completed' },
              searching: { ...state.stages.searching, status: 'completed' },
              reading: { ...state.stages.reading, status: 'completed' },
              writing: { ...state.stages.writing, status: 'active' },
            },
          };

        case 'writer.completed':
          return {
            ...state,
            progressPercentage: 80,
            stages: {
              ...state.stages,
              writing: { ...state.stages.writing, status: 'completed' },
            },
          };

        case 'reviewer.started':
          return {
            ...state,
            activeStageId: 'reviewing',
            progressPercentage: 85,
            stages: {
              ...state.stages,
              writing: { ...state.stages.writing, status: 'completed' },
              reviewing: { ...state.stages.reviewing, status: 'active' },
            },
          };

        case 'reviewer.completed':
          return {
            ...state,
            progressPercentage: 95,
            stages: {
              ...state.stages,
              reviewing: { ...state.stages.reviewing, status: 'completed' },
            },
          };

        case 'report.persisted':
          return {
            ...state,
            progressPercentage: 98,
          };

        case 'workflow.completed':
          return {
            ...state,
            status: 'completed',
            activeStageId: null,
            progressPercentage: 100,
            totalExecutionTimeMs:
              typeof metadata.total_execution_time_ms === 'number'
                ? metadata.total_execution_time_ms
                : undefined,
            stages: {
              planning: { ...state.stages.planning, status: 'completed' },
              searching: { ...state.stages.searching, status: 'completed' },
              reading: { ...state.stages.reading, status: 'completed' },
              writing: { ...state.stages.writing, status: 'completed' },
              reviewing: { ...state.stages.reviewing, status: 'completed' },
            },
          };

        case 'workflow.failed':
          return {
            ...state,
            status: 'failed',
            activeStageId: null,
            progressPercentage: 100,
            error:
              event.message ||
              (typeof metadata.error === 'string' ? metadata.error : 'Research workflow failed.'),
          };

        default:
          return state;
      }
    }
  }
}
