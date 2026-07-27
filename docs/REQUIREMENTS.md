# Requirements — Desearch AI

> Product: **Desearch AI** — Deep Research. Smarter Decisions.
> Derived from: `Docs/PROJECT_VISION.md`
> Updated: TICKET-007 — Product repositioning to Desearch AI
> Updated: Consistency Pass — Terminology, operational limits, product non-goals, canonical example
> Scope: MVP only
> Status: Baseline

---

## Functional Requirements

### FR-01 — Research Query Submission

- The platform must accept a natural language research query submitted by a user.
- The platform must validate that a submitted query is non-empty and contains sufficient specificity before processing begins.
- The platform must return a confirmation to the user that the research query has been received and the pipeline has begun.

### FR-02 — Agent Orchestration

- The platform must route an incoming research query to a Planner Agent that decomposes it into a structured research execution plan.
- The Planner Agent must produce an ordered plan identifying the subtasks required and the agent assigned to each.
- The orchestrator must dispatch each subtask to the appropriate registered agent based on the agent's defined role.
- The platform must support all five MVP agents operating in sequence within a single research session: Planner, Research, Fact Checker, Writer, and Reviewer.
- Each agent must have a defined role, a bounded tool set, and an independently verifiable output.

### FR-03 — Tool Execution

- Agents must be able to invoke registered external tools during research execution.
- The platform must support a minimum of three distinct tools for the MVP: web search, web page reader, and document reader.
- Tool invocations must be structured, parameterized, and produce deterministic output formats.
- Tool execution results must be passed back to the invoking agent before the next step proceeds.

### FR-04 — Research Session Context

- The platform must maintain short-term, session-scoped research session context that all agents can read and write during an active research session.
- The Planner Agent must write the structured execution plan to research session context before any other agent is dispatched.
- Research findings written by the Research Agent must be accessible to the Fact Checker Agent, Writer Agent, and Reviewer Agent within the same research session.
- Validated findings written by the Fact Checker Agent must be accessible to the Writer Agent and Reviewer Agent within the same research session.
- Research session context must be cleared or isolated at the start of each new research session.
- Research session context from one research session must never be readable by any agent in a different research session.

### FR-05 — Human-in-the-Loop Approval

- The platform must support configurable approval checkpoints at which agent execution is paused pending user review.
- The two configurable approval checkpoint positions in the MVP are: after the Planner Agent produces the execution plan (AWAITING_PLAN_APPROVAL), and after the Fact Checker Agent produces validated findings (AWAITING_FACTCHECK_APPROVAL).
- At each approval checkpoint, the user must be able to: approve (resume execution), reject (halt the research session), or retry (re-execute the pending agent step and re-present the output).
- Execution must not continue past an approval checkpoint until the user has responded.
- If a user rejects an agent action, the system must log the rejection and halt the research session.
- Retry attempts at an approval checkpoint are bounded by the MVP maximum approval checkpoint retry limit.

### FR-06 — Research Report Generation

- The platform must return a structured research report upon pipeline completion.
- The report must reflect the combined output of all five agents involved in the research session.
- The report must indicate which agents and tools contributed to each section of the output.
- The report must include at minimum: an executive summary, a structured body with sourced findings, and a conclusion.

### FR-07 — Report Export via Output Formatter

- The platform must support export of the completed research report in Markdown format via the Output Formatter component.
- The Output Formatter must operate only after the Reviewer Agent has approved the research report and the research session has reached the COMPLETED state.
- The exported Markdown file must be self-contained: it must include all sections, citations, confidence levels, and metadata without requiring access to the platform to be readable.

### FR-08 — Execution History

- The platform must store a retrievable log of every completed research session.
- Each log entry must contain: the original research query, the research session state at completion, the agents involved, the tools called, and the final research report.
- A user must be able to retrieve the execution history for a given research session by session ID.

### FR-09 — Execution Tracing

- Every agent action, tool invocation, and model request during a research session must be recorded as a discrete trace event.
- Each trace event must capture: timestamp, agent identity, action type, inputs, and outputs.
- Execution traces must be retrievable after session completion.

### FR-10 — Failure Handling and Retry

- The platform must detect agent-level failures during research execution.
- On failure, the platform must log the error with sufficient context for diagnosis.
- The platform must either retry the failed step automatically (up to a configurable limit) or return a structured error response to the user.
- Unhandled exceptions must not propagate to the user as raw stack traces.

### FR-11 — Research Workbench Interface

- The platform must provide a web-based research workbench through which users can submit research queries, monitor research pipeline progress, review agent outputs stage by stage, inspect execution traces, and export completed research reports.
- The interface must display real-time or near-real-time status updates during research session execution, reflecting the current research session lifecycle state (PLANNING, RESEARCHING, FACT_CHECKING, WRITING, REVIEWING, COMPLETED, FAILED, HALTED).
- The interface must surface approval checkpoints (AWAITING_PLAN_APPROVAL, AWAITING_FACTCHECK_APPROVAL) requiring user action.
- The interface must clearly indicate which agent is currently active and what research pipeline step is in progress.

### FR-12 — LLM Provider Integration

- The platform must integrate with at least one external LLM provider via a network-accessible inference endpoint.
- The LLM provider must be operable within free-tier usage limits.
- The platform must support swapping the LLM provider without changes to orchestration or agent logic.

---

## Non-Functional Requirements

### NFR-01 — Performance

- A standard five-agent research pipeline (Planner → Research → Fact Checker → Writer → Reviewer) must complete within 120 seconds under normal operating conditions and within the MVP operational limits defined in `Docs/SYSTEM_ARCHITECTURE.md`.
- The research workbench interface must load within 3 seconds on a standard broadband connection.
- Research execution history and execution trace retrieval must respond within 2 seconds for any single research session record.

### NFR-02 — Reliability

- The platform must complete at least three distinct research queries end-to-end without manual intervention in a single session.
- Agent failures must be caught and handled; the system must not crash on a single agent error.
- All research sessions must produce a deterministic terminal state: either a report or a structured error — never a silent hang.

### NFR-03 — Scalability

- The platform design must not assume a single-process execution model; agent workloads must be isolatable units that can scale independently.
- The platform must function correctly when handling multiple simultaneous research sessions.

### NFR-04 — Security

- All externally accessible endpoints must require authentication (minimum: API key validation).
- No LLM provider credentials or service secrets may be exposed in client-side code, logs, or public version control.
- User-submitted research queries must be sanitized before being passed to any external service.

### NFR-05 — Maintainability

- Each agent must be independently definable with its own role, tool set, and execution logic, without modifying the Orchestrator.
- The Orchestrator must receive and execute the Planner Agent's execution plan without containing any research planning logic itself.
- The platform must include inline documentation sufficient for a new contributor to understand the flow of a research query from submission to research report export.
- All configuration values (timeouts, retry limits, MVP operational limits, provider endpoints, API keys) must be externalized and not hardcoded.

### NFR-06 — Observability

- Every agent action, tool call, and LLM request must produce a structured log entry with: timestamp, agent ID, action type, status, and duration.
- Log entries must be queryable by session ID.
- The platform must expose a health status indicator reflecting whether core components are operational.

### NFR-07 — Availability

- The deployed platform must be publicly accessible via a stable URL without requiring an evaluator to perform any local setup.
- The platform must remain operational under the resource limits imposed by free-tier cloud services.

### NFR-08 — Portability

- The platform must be deployable to any standard cloud environment without proprietary vendor lock-in.
- Deployment must be reproducible from a clean environment using documented steps in under 30 minutes.

### NFR-09 — Cost Efficiency

- The platform must operate entirely within free-tier service quotas during normal demonstration usage.
- No component may require a paid subscription as a hard dependency.

### NFR-10 — Extensibility

- Adding a new research agent must not require changes to existing agents or the orchestrator's core routing logic.
- Adding a new tool must not require changes to agent logic beyond registration.
- Replacing the LLM provider must not require changes to orchestration or agent role definitions.
- New output formats (e.g., PDF export) must be addable without modifying the Writer or Reviewer agents.

---

## User Stories

### Research Query Submission

**US-01**
As a Software Engineer,
I want to submit a research query such as "Compare Supabase vs Firebase for Enterprise SaaS" through the research workbench,
So that the platform can orchestrate specialized agents to produce a structured technical comparison research report on my behalf.

**US-02**
As a Startup Founder,
I want to receive a confirmation when my research query has been accepted for processing,
So that I know the pipeline has begun and I can return to review the report when it is ready.

### Agent Orchestration

**US-03**
As a Product Manager,
I want the Planner Agent to automatically decompose my research query into a structured plan and route each step to the appropriate agent,
So that I do not need to manually coordinate the research process.

**US-04**
As a Technical Consultant,
I want to see which agent handled each phase of my research task and what it produced,
So that I can assess the quality and sourcing of each component of the final report.

### Tool Execution

**US-05**
As an AI Engineer,
I want the Research Agent to invoke real web search and web page reader tools during research execution,
So that the findings are grounded in live, verifiable sources rather than only model memory.

### Research Session Memory

**US-06**
As a Researcher,
I want the Fact Checker Agent, Writer Agent, and Reviewer Agent to have access to the Research Agent's findings via research session context without requiring me to re-submit them,
So that context flows automatically through the research pipeline from stage to stage.

### Human-in-the-Loop Approval

**US-07**
As a Product Manager,
I want to review and approve the Planner Agent's execution plan before the Research Agent begins collecting information (AWAITING_PLAN_APPROVAL checkpoint),
So that I can redirect the scope of the research before time and tokens are spent on the wrong subtasks.

**US-08**
As a Technical Consultant,
I want to review the Fact Checker Agent's validation results at the AWAITING_FACTCHECK_APPROVAL checkpoint and reject or request a retry if a key claim is insufficiently sourced,
So that I can ensure the final research report meets the evidentiary standard required for client delivery.

### Execution History and Tracing

**US-09**
As an AI Engineer,
I want to retrieve the full execution trace of a completed research session,
So that I can audit every agent action, tool call, and model response that contributed to the research report.

**US-10**
As a Student,
I want to browse my past research sessions and their results,
So that I can reference earlier research without resubmitting the same query.

### Failure Handling

**US-11**
As a Software Engineer,
I want the platform to recover gracefully from an agent failure during a research pipeline,
So that a single failed step does not discard all prior research progress.

**US-12**
As a Researcher,
I want failed pipeline steps to produce a structured error response with sufficient context,
So that I can understand what went wrong and decide whether to retry or revise my query.

### Report Generation and Export

**US-13**
As a Startup Founder,
I want the platform to return a consolidated, structured research report with sourced findings upon pipeline completion,
So that I can use it directly to inform a product or technology decision.

**US-14**
As a Technical Consultant,
I want to export the completed research report as a Markdown document,
So that I can incorporate it into a client deliverable or internal knowledge base without formatting effort.

---

## Acceptance Criteria

### AC-01 — Research Query Submission

- A research query submitted through the web interface is accepted and acknowledged within 2 seconds.
- An empty or whitespace-only query submission is rejected with a descriptive validation message.
- A valid query submission triggers observable pipeline activity (i.e., the Planner Agent becomes active within 5 seconds).

### AC-02 — Agent Orchestration

- A submitted research query results in all five agents being invoked in the correct sequence: Planner → Research → Fact Checker → Writer → Reviewer.
- Each agent's invocation is recorded in the execution trace with its role, inputs, and outputs.
- No agent is invoked for a subtask outside its defined role.

### AC-03 — Tool Execution

- The Research Agent successfully invokes at least one registered tool (web search, web page reader, or document reader) during research execution.
- The tool's output is incorporated into the agent's response before the next pipeline step proceeds.
- Tool invocations are logged with: tool name, inputs, outputs, and duration.
- An unavailable tool causes a logged error, not an unhandled exception.

### AC-04 — Research Session Context

- The Planner Agent's execution plan written to research session context is correctly readable by the Research Agent, Fact Checker Agent, Writer Agent, and Reviewer Agent in the same research session.
- Findings written by the Research Agent are correctly readable by the Fact Checker Agent in the same research session.
- The report written by the Writer Agent is correctly readable by the Reviewer Agent in the same research session.
- Research session context from research session A is not accessible in research session B.
- Research session context is correctly cleared at the start of each new research session.

### AC-05 — Human-in-the-Loop Approval

- Execution halts at each configured approval checkpoint (AWAITING_PLAN_APPROVAL, AWAITING_FACTCHECK_APPROVAL) and does not proceed until the user responds.
- The user is presented with the pending agent output and can choose to approve, reject, or retry.
- An approval causes execution to resume from the approval checkpoint.
- A rejection causes the research session to halt and logs the rejection event with the session ID, checkpoint ID, and timestamp.
- A retry causes the agent to re-execute the pending step and re-present the new output for review.
- The number of retry attempts does not exceed the configured MVP approval checkpoint retry limit.

### AC-06 — Research Report Generation

- A completed research session returns a structured research report that conforms to the Writer Agent output schema defined in `Docs/SYSTEM_ARCHITECTURE.md`, including: title, canonical query, executive summary, sourced sections with confidence levels, conclusion, and citations.
- The research report is available through both the research workbench interface and the Research Execution API.

### AC-07 — Report Export

- A completed and Reviewer Agent-approved research report can be exported as a Markdown file via the Output Formatter from the research workbench interface.
- The exported Markdown file is self-contained: it includes all sections, confidence levels, citations, and metadata and is readable without platform access.

### AC-08 — Execution History

- A completed session's execution log is retrievable by session ID after session completion.
- Each log entry contains: timestamp, agent identity, action type, inputs, outputs, and status.
- History is not lost on system restart for a minimum of the current deployment session.

### AC-09 — Failure Handling

- When an agent raises an error, the error is caught, logged with context, and does not propagate as an unhandled exception.
- The platform retries the failed step up to the configured maximum before returning a structured error response.
- The structured error response includes: failed agent identity, step description, and error summary.

### AC-10 — Research Workbench Interface

- A user can submit a research query, monitor pipeline execution stage by stage, and view the final report entirely through the web interface without using any other tool.
- Human-in-the-loop checkpoints are surfaced in the interface with the agent's output and the approve/reject/retry controls.
- Execution status updates are visible within 5 seconds of the underlying state change.

### AC-11 — Deployment

- The platform is accessible via a public URL without any local setup by the evaluator.
- The deployment is reproducible from a clean environment in under 30 minutes following the documented steps.
- The platform operates within free-tier resource quotas during standard demonstration use.

---

## Constraints

- **CON-01** — The platform must operate entirely within free-tier cloud service quotas. No paid service may be a hard dependency.
- **CON-02** — The platform must be deployed to a cloud environment. Local-only execution does not satisfy the deployment requirement.
- **CON-03** — Local or self-hosted LLM inference is not permitted. All model inference must use a remote, network-accessible provider.
- **CON-04** — No paid external API subscription may be required for the platform to function. Free-tier access must be sufficient for normal demonstration use.
- **CON-05** — All components must be open-source friendly: relying only on software with permissive licenses compatible with public repository use.
- **CON-06** — The platform must be modular by design: agents, tools, output formats, and the LLM provider must be independently replaceable without modifying other components.
- **CON-07** — The platform must be production-oriented: no hardcoded secrets, no debug-only configurations in deployed environments, and structured error handling throughout.
- **CON-08** — The platform must be deployable without proprietary build tooling or vendor-specific CI/CD pipelines.
- **CON-09** — The platform must enforce the MVP Operational Limits defined in `Docs/SYSTEM_ARCHITECTURE.md` at runtime. No operational limit may be exceeded without an explicit configuration change.
- **CON-10** — The platform must not implement any capability defined as a Product Non-Goal in `Docs/PROJECT_VISION.md`. Any feature request that falls within a stated non-goal requires explicit written approval and a scope change before implementation.

---

## Assumptions

- **ASM-01** — Users understand what a research query is and can formulate one with sufficient specificity for the Planner Agent to produce a meaningful execution plan.
- **ASM-02** — The free-tier LLM provider offers sufficient throughput and context length for a five-agent, multi-step research pipeline under normal demonstration use.
- **ASM-03** — External research tools (web search, web page reader, document reader) are accessible via free or publicly available endpoints and do not require paid subscriptions.
- **ASM-04** — Research queries are submitted in English. Multilingual support is not a requirement for the MVP.
- **ASM-05** — The platform will not experience production-scale traffic during the MVP phase; free-tier resource limits are acceptable for demonstration and evaluation purposes.
- **ASM-06** — Deployment environment credentials and secrets will be managed by the operator outside of version control.
- **ASM-07** — The LLM provider's output format is sufficiently consistent to allow structured parsing by the Orchestrator without frequent format-correction logic.
- **ASM-08** — Research outputs are intended for professional evaluation and decision-support use; they are not a substitute for domain expert review.
- **ASM-09** — The Reviewer Agent will require at most two Writer Agent revision cycles before either approving the report or returning a structured failure response; this assumption is consistent with the Maximum Writer Agent Revision Attempts operational limit.

---

## Future Enhancements

The following capabilities are intentionally excluded from the MVP and may be considered for future iterations:

- **Long-term persistent research memory** — cross-session memory that enables agents to recall and build upon prior research sessions.
- **PDF export** — exportable research reports in PDF format with formatted citations and a table of contents.
- **Citation management** — automatic extraction, formatting, and deduplication of citations across all source documents used in a research session.
- **Multi-tenant support** — isolated research environments for multiple users or teams with role-based access control.
- **Research history search** — full-text search across all past research sessions and their outputs.
- **Streaming report generation** — incremental delivery of report sections to the user as the Writer Agent produces them.
- **Multi-LLM routing** — dynamic selection of the most appropriate LLM provider per research subtask based on capability, latency, or token cost.
- **Automated research quality evaluation** — a framework for scoring research output completeness, source coverage, and factual consistency against benchmarks.
- **Visual research workflow builder** — a drag-and-drop interface for defining custom research agent pipelines without configuration code.
- **Voice research query input** — speech-to-text input for research query submission.
- **Mobile research interface** — a native or progressive web application for research query submission and report retrieval on mobile devices.
- **Automated billing and usage metering** — per-user tracking of LLM token consumption and tool invocations.
