/**
 * Stream Execution Registry
 * Browser tab-scoped registry tracking initiated research streams.
 * Prevents duplicate stream execution across React StrictMode remounts,
 * query refetches, rerenders, and component updates.
 */

const initiatedSessions = new Set<string>();
const activeAbortControllers = new Map<string, AbortController>();

export const streamRegistry = {
  /**
   * Check if an SSE stream has already been initiated for this session ID.
   */
  hasInitiated(sessionId: string): boolean {
    return initiatedSessions.has(sessionId);
  },

  /**
   * Mark a session ID as having initiated an SSE stream.
   */
  markInitiated(sessionId: string): void {
    initiatedSessions.add(sessionId);
  },

  /**
   * Check if a stream is currently active for this session ID.
   */
  isStreamActive(sessionId: string): boolean {
    return activeAbortControllers.has(sessionId);
  },

  /**
   * Register the active AbortController for a running stream.
   */
  setActiveController(sessionId: string, controller: AbortController): void {
    activeAbortControllers.set(sessionId, controller);
  },

  /**
   * Abort an active stream for a session ID.
   */
  abortStream(sessionId: string): void {
    const controller = activeAbortControllers.get(sessionId);
    if (controller) {
      controller.abort();
      activeAbortControllers.delete(sessionId);
    }
  },

  /**
   * Clear session registry and abort stream if running.
   */
  clear(sessionId: string): void {
    this.abortStream(sessionId);
    initiatedSessions.delete(sessionId);
  },
};
