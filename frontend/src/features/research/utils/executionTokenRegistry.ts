/**
 * Single-Use Execution Token Registry for Desearch AI.
 * 
 * Guarantees that workflow execution (POST /api/v1/orchestrator/stream) can ONLY be
 * authorized by an explicit New Research submission, and that authorization can be
 * consumed EXACTLY ONCE across browser history events, page refreshes, and React lifecycles.
 */
class ExecutionTokenRegistry {
  private authorizedTokens = new Set<string>();

  /**
   * Generates and registers a single-use execution token for a newly created session.
   */
  public createToken(sessionId: string): string {
    const token = `exec-${sessionId}-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    this.authorizedTokens.add(token);
    return token;
  }

  /**
   * Atomically checks and consumes an execution token.
   * Returns true EXACTLY ONCE if the token was registered and unconsumed.
   * Immediately deletes the token so subsequent calls, refreshes, or navigation return false.
   */
  public consumeToken(sessionId: string, token: string | undefined | null): boolean {
    if (!token || !sessionId) {
      return false;
    }

    if (this.authorizedTokens.has(token)) {
      this.authorizedTokens.delete(token);
      return true;
    }

    return false;
  }

  /**
   * Clears all registered tokens (for testing purposes).
   */
  public clear(): void {
    this.authorizedTokens.clear();
  }
}

export const executionTokenRegistry = new ExecutionTokenRegistry();
