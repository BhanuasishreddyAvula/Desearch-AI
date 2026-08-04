/**
 * Anonymous Device Identity Utility
 *
 * Provides a permanent, device-scoped UUID that persists in localStorage.
 * This ID is used to scope all research sessions to the current browser/device
 * without requiring user authentication or accounts.
 *
 * Lifecycle:
 *   - First launch: generate UUID v4 → store in localStorage
 *   - Subsequent launches: read existing UUID from localStorage
 *   - Never regenerated unless localStorage is cleared
 */

const DEVICE_ID_KEY = 'desearch_device_id';

/**
 * Returns the persistent anonymous device ID for this browser.
 * Generates and stores a new UUID v4 on first call.
 */
export function getDeviceId(): string {
  let id = localStorage.getItem(DEVICE_ID_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(DEVICE_ID_KEY, id);
  }
  return id;
}
