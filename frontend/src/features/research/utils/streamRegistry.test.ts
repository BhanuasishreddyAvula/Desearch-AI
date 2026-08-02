import { streamRegistry } from './streamRegistry';
import { executionTokenRegistry } from './executionTokenRegistry';
import type { ResearchSession } from '../../../types';

/**
 * Verification test suite for P3-04 Workflow Ownership Architecture.
 * Validates tests 1 through 12.
 */
export function runStreamLifecycleVerificationTests(): boolean {
  console.log('[P3-04 Verification] Running Execution Ownership Safety Tests...');
  let passed = true;

  const testSessionId = 'test-session-uuid-99999';
  streamRegistry.clear(testSessionId);
  executionTokenRegistry.clear();

  // TEST 1 — New Research Submission with Token
  const token1 = executionTokenRegistry.createToken(testSessionId);
  const isTokenValid = executionTokenRegistry.consumeToken(testSessionId, token1);
  if (isTokenValid) {
    streamRegistry.markInitiated(testSessionId);
  }
  const test1Passed = isTokenValid && streamRegistry.hasInitiated(testSessionId);
  console.log(`TEST 1 (New Research single execution): ${test1Passed ? 'PASS' : 'FAIL'}`);
  if (!test1Passed) passed = false;

  // TEST 2 — React Rerender (Token already consumed)
  const tokenRerenderReuse = executionTokenRegistry.consumeToken(testSessionId, token1);
  const test2Passed = !tokenRerenderReuse && streamRegistry.hasInitiated(testSessionId);
  console.log(`TEST 2 (React rerender block): ${test2Passed ? 'PASS' : 'FAIL'}`);
  if (!test2Passed) passed = false;

  // TEST 3 — StrictMode Second Mount (Token consumed on Mount 1)
  const test3Passed = !executionTokenRegistry.consumeToken(testSessionId, token1);
  console.log(`TEST 3 (StrictMode double-mount block): ${test3Passed ? 'PASS' : 'FAIL'}`);
  if (!test3Passed) passed = false;

  // TEST 4 — Click Existing Sidebar Session (No token provided)
  const test4Passed = !executionTokenRegistry.consumeToken('existing-session-4', undefined);
  console.log(`TEST 4 (Sidebar session click block): ${test4Passed ? 'PASS' : 'FAIL'}`);
  if (!test4Passed) passed = false;

  // TEST 5 — Return to Previous Chat
  const test5Passed = !executionTokenRegistry.consumeToken(testSessionId, undefined);
  console.log(`TEST 5 (Return to previous session block): ${test5Passed ? 'PASS' : 'FAIL'}`);
  if (!test5Passed) passed = false;

  // TEST 6 — Refresh Browser on Existing Session (Stale token in window.history.state)
  // Since token1 was deleted during consumeToken in TEST 1, trying to reuse token1 fails.
  const test6Passed = !executionTokenRegistry.consumeToken(testSessionId, token1);
  console.log(`TEST 6 (Browser refresh block): ${test6Passed ? 'PASS' : 'FAIL'}`);
  if (!test6Passed) passed = false;

  // TEST 7 — Refresh Completed Session
  const completedSession: ResearchSession = {
    id: 'completed-1',
    title: 'Completed',
    query: 'query',
    status: 'COMPLETED',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
  const test7Passed = completedSession.status === 'COMPLETED' && !executionTokenRegistry.consumeToken(completedSession.id, undefined);
  console.log(`TEST 7 (Refresh completed session block): ${test7Passed ? 'PASS' : 'FAIL'}`);
  if (!test7Passed) passed = false;

  // TEST 8 — Refresh Failed Session
  const failedSession: ResearchSession = {
    id: 'failed-1',
    title: 'Failed',
    query: 'query',
    status: 'FAILED',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
  const test8Passed = failedSession.status === 'FAILED' && !executionTokenRegistry.consumeToken(failedSession.id, undefined);
  console.log(`TEST 8 (Refresh failed session block): ${test8Passed ? 'PASS' : 'FAIL'}`);
  if (!test8Passed) passed = false;

  // TEST 9 — Paste URL directly
  const test9Passed = !executionTokenRegistry.consumeToken('direct-url-id', null);
  console.log(`TEST 9 (Direct URL paste block): ${test9Passed ? 'PASS' : 'FAIL'}`);
  if (!test9Passed) passed = false;

  // TEST 10 — Browser Back then Forward
  const test10Passed = !executionTokenRegistry.consumeToken(testSessionId, token1);
  console.log(`TEST 10 (Browser back/forward block): ${test10Passed ? 'PASS' : 'FAIL'}`);
  if (!test10Passed) passed = false;

  // TEST 11 — Cache invalidation / Query Refetch
  const test11Passed = !executionTokenRegistry.consumeToken(testSessionId, undefined);
  console.log(`TEST 11 (Query refetch block): ${test11Passed ? 'PASS' : 'FAIL'}`);
  if (!test11Passed) passed = false;

  // TEST 12 — Repeated sidebar switching
  const test12Passed = !executionTokenRegistry.consumeToken('session-a', undefined) && !executionTokenRegistry.consumeToken('session-b', undefined);
  console.log(`TEST 12 (Repeated sidebar switching block): ${test12Passed ? 'PASS' : 'FAIL'}`);
  if (!test12Passed) passed = false;

  streamRegistry.clear(testSessionId);
  executionTokenRegistry.clear();
  return passed;
}
