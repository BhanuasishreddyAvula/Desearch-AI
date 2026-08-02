"""Session-level cancellation token registry.

Stores a threading.Event per active session_id so the orchestrator can
check at each agent boundary and stop gracefully when the user clicks Stop.

The backend server is NEVER stopped. Only the agents for that session exit.
"""

import threading
from typing import Dict

_registry: Dict[str, threading.Event] = {}
_lock = threading.Lock()


def create_cancel_token(session_id: str) -> threading.Event:
    """Register and return a cancel token for the given session_id."""
    event = threading.Event()
    with _lock:
        _registry[session_id] = event
    return event


def get_cancel_token(session_id: str) -> threading.Event | None:
    """Return the cancel token for session_id, or None if not registered."""
    with _lock:
        return _registry.get(session_id)


def request_cancel(session_id: str) -> bool:
    """Signal cancellation for session_id. Returns True if token found."""
    with _lock:
        token = _registry.get(session_id)
    if token is not None:
        token.set()
        return True
    return False


def remove_cancel_token(session_id: str) -> None:
    """Remove the cancel token after a session workflow finishes or is cancelled."""
    with _lock:
        _registry.pop(session_id, None)


def is_cancelled(session_id: str) -> bool:
    """Return True if the session has been cancelled."""
    with _lock:
        token = _registry.get(session_id)
    return token is not None and token.is_set()
