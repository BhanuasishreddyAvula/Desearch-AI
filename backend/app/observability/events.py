"""System observability event constants."""


class SystemEvents:
    """Standardized event name constants across Desearch AI."""

    # Application Lifecycle Events
    APPLICATION_STARTED = "application.started"
    APPLICATION_STOPPED = "application.stopped"

    # HTTP Request Events
    REQUEST_STARTED = "request.started"
    REQUEST_COMPLETED = "request.completed"
    REQUEST_FAILED = "request.failed"

    # Agent Lifecycle Events
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"

    # Tool Execution Events
    TOOL_STARTED = "tool.started"
    TOOL_COMPLETED = "tool.completed"
    TOOL_FAILED = "tool.failed"

    # LLM Provider Events
    LLM_REQUEST = "llm.request"
    LLM_RESPONSE = "llm.response"
    LLM_ERROR = "llm.error"

    # Checkpoint Events
    CHECKPOINT_CREATED = "checkpoint.created"
    CHECKPOINT_RESOLVED = "checkpoint.resolved"
