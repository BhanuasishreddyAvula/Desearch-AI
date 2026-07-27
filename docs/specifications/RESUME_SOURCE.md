# Resume Source — Desearch AI

> Product: **Desearch AI** — Deep Research. Smarter Decisions.
> Derived from: All `Docs/` project documentation
> Updated: TICKET-007 — Product repositioning to Desearch AI
> Updated: Consistency Pass — Canonical example, terminology, agent names
> Purpose: Career documentation — resume, LinkedIn, GitHub, interviews
> Status: Pre-implementation (metrics are placeholders; update after deployment)

---

## Project Summary

Designed and built **Desearch AI**, a production-grade, cloud-native AI research workbench that orchestrates a five-agent pipeline to transform a natural language research query into a structured, sourced, and verified research report. The system implements a Planner Agent for research scoping, a Research Agent for source gathering, a Fact Checker Agent for claim validation, a Writer Agent for structured report generation, and a Reviewer Agent for quality assurance — all coordinated through a central orchestrator. A shared research session context layer propagates research findings across agent hand-offs without direct inter-agent coupling. A tool registry provides web search, web page reading, and document reading capabilities. An Output Formatter renders the completed research report to Markdown for export. Human-in-the-loop approval checkpoints enable user oversight at critical research pipeline stages (AWAITING_PLAN_APPROVAL and AWAITING_FACTCHECK_APPROVAL). The system is deployed to a cloud environment, observable through structured execution traces, and fully reproducible from a clean environment.

---

## One-Line Resume Description

Architected and built Desearch AI — a cloud-native, five-agent AI research workbench that transforms research queries into structured, verified reports through a multi-agent orchestration pipeline with human-in-the-loop oversight and full execution observability.

---

## Resume Bullet Points

- **Architected and built Desearch AI**, a cloud-native multi-agent AI research platform orchestrating a five-agent pipeline (Planner, Research, Fact Checker, Writer, Reviewer) to produce structured, source-verified research reports from natural language queries — deployed on free-tier infrastructure and publicly accessible.

- **Engineered a provider-agnostic LLM integration layer** that decouples all agent and orchestration logic from any specific AI provider, enabling the underlying model to be swapped by configuration change — with structured token usage logging and configurable timeout enforcement across all five research agents.

- **Implemented a human-in-the-loop approval system** with configurable checkpoints at critical research pipeline stages (research plan approval, fact-check validation), supporting approve/reject/retry resolution flows, durable checkpoint persistence, and an immutable audit trail for every user decision.

- **Delivered full research pipeline observability** through schema-enforced structured logging across all components, per-session execution traces capturing every agent invocation, tool call, and LLM request, and a public-facing research trace viewer — all deployed with documented reproducibility in under 30 minutes.

---

## LinkedIn Project Description

**Desearch AI** | AI Research Workbench — Deep Research. Smarter Decisions.

Built Desearch AI, a production-grade AI research platform that goes far beyond single-prompt chatbots. Submit a research query — "Compare Supabase vs Firebase for enterprise SaaS" — and a coordinated pipeline of five specialized AI agents produces a structured, sourced, and reviewed research report.

**The five-agent research pipeline:**
- **Planner Agent** — scopes the research and creates an execution plan.
- **Research Agent** — gathers information using web search, page reading, and document retrieval tools.
- **Fact Checker Agent** — validates key claims and sources before they reach the report.
- **Writer Agent** — synthesizes validated findings into a structured report with executive summary and body sections.
- **Reviewer Agent** — evaluates the report for completeness and quality before delivery.

**Engineering capabilities implemented:**

**Multi-Agent Orchestration** — A central orchestrator routes research subtasks to agents through a defined pipeline, with no direct agent-to-agent coupling.

**Tool Integration** — A modular tool registry enables agents to invoke real external capabilities (web search, page reader, document reader) with validated inputs and structured responses.

**Human-in-the-Loop Approval** — Configurable checkpoints pause the research pipeline for user review of the research plan and validated findings before the report is written.

**Observability** — Every agent invocation, tool call, and LLM request produces a structured, schema-enforced log event. Full execution traces are retrievable per research session.

**Cloud Deployment** — Publicly accessible via a stable URL, operating entirely within free-tier cloud service quotas.

---

## GitHub Repository Description

### Short Description
*(max 160 characters)*

Desearch AI: cloud-native multi-agent AI research workbench. Five-agent pipeline produces structured research reports with HITL oversight and full observability.

### Long Description

Desearch AI is a production-grade, cloud-native AI research workbench that transforms a natural language research query into a structured, source-verified research report through a coordinated five-agent pipeline: Planner, Research, Fact Checker, Writer, and Reviewer.

Built with a focus on production engineering: a central orchestrator with no direct agent-to-agent coupling, a shared research session context layer for cross-agent context propagation, a provider-agnostic LLM integration layer, a modular tool registry (web search, page reader, document reader), configurable human-in-the-loop approval checkpoints with durable state persistence, schema-enforced structured logging, and full per-session execution tracing.

Fully documented with architecture specs, 15 engineering decision records, requirements, and an implementation plan. Publicly deployed on free-tier cloud infrastructure. A reference implementation for AI Engineers building production multi-agent research systems.

---

## ATS Keywords

```
Research AI
Deep Research
AI Research
Research Automation
AI Workbench
Knowledge Synthesis
Technical Research
Competitive Analysis
Multi-Agent Systems
AI Agent Orchestration
Autonomous Agents
Tool Calling
Tool Use
Human-in-the-Loop
HITL
Approval Checkpoint
Retrieval Augmented Generation
RAG
Agent Architecture
Task Decomposition
Prompt Engineering
Context Management
Research Session Context
Structured Logging
Observability
Execution Tracing
Audit Trail
Cloud-Native
Cloud Deployment
Free-Tier Deployment
REST API
Backend Engineering
Modular Architecture
Fault Tolerance
Error Handling
Provider-Agnostic
LLM Abstraction
Applied AI
AI Engineering
Production AI
AI Infrastructure
Agent Framework
Research Pipeline
AI Report Generation
Report Confidence Model
Output Formatter
```

---

## Skills Demonstrated

### AI Engineering
- Multi-agent system design and orchestration (five-agent research pipeline)
- Research pipeline decomposition and agent routing
- LLM integration with provider-agnostic abstraction
- Tool calling and structured tool integration (web search, page reader, document reader)
- Research session context design and cross-agent context propagation
- Human-in-the-loop approval checkpoint design (AWAITING_PLAN_APPROVAL, AWAITING_FACTCHECK_APPROVAL)
- Agent lifecycle management in a sequential research pipeline
- Prompt engineering for specialized research agent roles (planner, researcher, fact-checker, writer, reviewer)
- Report output schema design (Writer Agent structured output)
- Output Formatter for structured Markdown generation
- Report Confidence Model (claim, section, and report-level confidence scoring)
- LLM error handling, timeout management, and token budget awareness
- Execution tracing and AI research system observability

### Backend Engineering
- RESTful API design with authentication and input validation
- Stateless backend service design
- Layered error handling and structured error responses
- Configurable retry logic with bounded backoff
- Session lifecycle management and isolation enforcement
- Audit trail and immutable record design for HITL decisions
- Durable checkpoint state management across system restarts
- Health monitoring endpoint design

### System Design
- Central orchestrator pattern for research pipeline coordination
- Tool registry and plugin patterns
- Provider abstraction and dependency inversion
- Component interface-driven design
- Session isolation strategy in concurrent research sessions
- Modular, independently replaceable component architecture
- Open-closed system design (new agents, tools, output formats by registration)
- Scalability through stateless services and external state

### Cloud & DevOps
- Cloud-native deployment on free-tier infrastructure
- Secrets management via environment-level configuration
- Static frontend hosting and backend compute service deployment
- Managed persistence and in-memory store configuration
- Deployment documentation for clean-environment reproducibility in under 30 minutes
- Health status monitoring for deployed research services

### Software Engineering
- Engineering decision record (EDR) authoring (15 EDRs)
- Requirements specification (functional, non-functional, user stories, acceptance criteria)
- Architecture specification at system design level
- Incremental, milestone-driven development planning
- Test strategy design (unit, integration, end-to-end, acceptance)
- Risk identification and mitigation planning
- Interface contract design before implementation

---

## Interview Talking Points

---

**Q1. Walk me through what Desearch AI does and why you built it.**

*Why asked:* Interviewers want to assess whether you can articulate the purpose of your own work clearly and concisely to both technical and non-technical audiences.

*Key points expected:*
- The problem: complex research tasks require planning, source gathering, validation, synthesis, and review — operations that a single chatbot prompt cannot reliably perform.
- The solution: a five-agent research pipeline where each agent has a narrow, optimized role in producing a structured, sourced research report.
- The "why": to demonstrate production AI engineering — multi-agent coordination, tool grounding, observability — applied to a real user problem.

---

**Q2. Why five specialized research agents instead of one powerful agent?**

*Why asked:* This tests your understanding of the trade-offs between single-agent simplicity and multi-agent quality. It is a common question because many engineers default to a single-agent design.

*Key points expected:*
- A research query involves fundamentally different cognitive operations: scoping, gathering, validating, writing, reviewing. Assigning all to one agent produces an overloaded prompt and lower quality output.
- Specialization: each agent gets a prompt, context access pattern, and tool set optimized for its specific role.
- Independent improvability: the Fact Checker Agent can be improved without touching the Research or Writer agents.
- Acknowledge the trade-off: increased coordination complexity, more state management, longer pipelines.

---

**Q3. How does the orchestrator coordinate five agents without direct agent-to-agent communication?**

*Why asked:* This probes the depth of your orchestration design. A surface-level answer ("the orchestrator routes tasks") is not sufficient.

*Key points expected:*
- The orchestrator uses each agent's declared role description to make routing decisions — not hardcoded logic.
- A shared research session context layer is the context exchange mechanism: the Research Agent writes findings, and the Fact Checker reads them from research session context without the orchestrator carrying data between them.
- The orchestrator maintains pipeline ordering (sequential dispatch with dependency enforcement) but does not become a data-routing component.
- Adding a new agent requires only updating the manifest, not modifying the orchestrator.

---

**Q4. How do research findings flow from the Research Agent to the Fact Checker, then Writer, then Reviewer?**

*Why asked:* Inter-agent context propagation in a five-step sequential pipeline is a key engineering challenge. This question reveals whether you solved it architecturally or ad hoc.

*Key points expected:*
- A shared research session context layer is the context exchange mechanism: all agents in a research session read from and write to a common context store keyed by session ID.
- The Research Agent writes sourced findings to research session context. The Fact Checker Agent reads them, validates them, and writes validated findings. The Writer Agent reads validated findings and writes the draft report. The Reviewer Agent reads the draft report.
- The Orchestrator does not pass context explicitly; it only dispatches the subtask and receives the structured output.
- Session isolation ensures concurrent research sessions cannot read each other's research session context.

---

**Q5. Where and why did you implement HITL checkpoints in the research pipeline?**

*Why asked:* HITL placement decisions reveal product thinking applied to AI system design — not every step needs a checkpoint.

*Key points expected:*
- Two checkpoint placement decisions were made: after the Planner Agent (AWAITING_PLAN_APPROVAL) and after the Fact Checker Agent (AWAITING_FACTCHECK_APPROVAL).
- The plan approval checkpoint allows scope correction before the expensive Research Agent gathering phase begins.
- The fact-check approval checkpoint allows evidentiary quality control before the Writer Agent synthesizes the final report.
- Each approval checkpoint supports approve (resume), reject (halt), and retry (re-execute and re-present).
- Approval checkpoint state is persisted durably — a system restart does not lose an open approval checkpoint.

---

**Q6. How is the LLM provider abstracted? Why does this matter for a research system?**

*Why asked:* Provider abstraction is a signal of good software engineering. This question evaluates whether you anticipated change.

*Key points expected:*
- A dedicated integration layer translates the platform's standard inference request format into the provider's native API format. All five agents interact with the abstraction, not the provider directly.
- Switching providers is a configuration change, not a code change.
- For a research system specifically: research tasks can have long prompts (research plans, multi-source findings). Different providers have different context window limits and pricing. Provider agnosticism allows adapting to the best available free-tier option.

---

**Q7. How do you handle failures mid-pipeline — what happens if the Research Agent fails?**

*Why asked:* Error handling in a five-step sequential pipeline is complex. This question distinguishes production-oriented engineers.

*Key points expected:*
- Layered recovery: tool-level retry, agent-level retry (up to configurable maximum), task-level structured halt.
- Every error is caught at its component boundary — no unhandled exceptions propagate to the user.
- A Research Agent failure does not lose the Planner's work; the orchestrator can retry only the failed step.
- All failures produce structured log events with session ID, agent identity, step description, and error summary.
- If retries are exhausted, the pipeline halts with a structured error response identifying the failed step.

---

**Q8. How does your observability system work for a multi-step research pipeline?**

*Why asked:* Observability in a five-agent pipeline is more valuable — and more complex — than in a single-agent system. This question reveals production engineering maturity.

*Key points expected:*
- Schema-enforced structured log events emitted by every component at every action: agent invocations, tool calls, LLM requests, approval decisions, errors.
- All events keyed by session ID, enabling retrieval of the complete execution trace for any research session.
- A user can inspect which agent acted, what it read from research session context, which tools it invoked, what the LLM received and returned, and what it wrote back.
- Health status endpoint for operational monitoring.
- Audit trail for all HITL decisions — separate from operational logs.

---

**Q9. Why are the backend services stateless when a research pipeline is inherently stateful?**

*Why asked:* This question reveals whether you understand the difference between stateful workflows and stateless services.

*Key points expected:*
- The research pipeline produces stateful data (findings, validated claims, draft reports), but that state is stored externally in the research session context and persistence layers — not inside the service process.
- Stateless services can be scaled horizontally and replaced without state loss.
- A service restart does not lose research progress because all state is in the external layers.
- This distinction — stateful workload, stateless service — is the key insight.

---

**Q10. How is research session isolation enforced when multiple users submit queries simultaneously?**

*Why asked:* Session isolation is a correctness requirement and a security property in a multi-session research system.

*Key points expected:*
- Every state operation (read/write) in the research session context layer requires a session ID at the interface level.
- Cross-session reads are structurally rejected — not prevented by application discipline alone.
- Research session A's findings cannot be read by session B's agents, even if they run concurrently.
- Validated by a specific integration test running two concurrent research sessions and verifying no context leakage.

---

**Q11. How do you test a five-agent AI research pipeline?**

*Why asked:* Testing multi-agent AI systems is non-trivial. This question reveals whether you have thought beyond manual testing.

*Key points expected:*
- Unit tests with mocked LLM and tool responses — each agent tested in isolation without real external calls.
- Integration tests verifying real component interactions: Research Agent writing to research session context and Fact Checker reading correctly.
- End-to-end tests against the deployed environment with real LLM and tool calls on known research queries.
- Acceptance tests mapped directly to the acceptance criteria in the specification (AC-01 through AC-11).
- Specific tests for session isolation, graceful pipeline failure handling, and HITL checkpoint resolution flows.

---

**Q12. How did you design extensibility — adding a sixth agent or a new research tool?**

*Why asked:* Extensibility design reveals whether you built for your current requirements or for future requirements.

*Key points expected:*
- New agents are added by registering them in the agent manifest with their role description — no changes to existing agents or the orchestrator.
- New tools are added by registering them in the tool registry — no changes to agents.
- The orchestrator uses role descriptions to route subtasks, so new agents are discoverable by registration.
- A PDF export tool, for example, could be added to the registry without modifying the Writer or Reviewer agents.
- This is the Open-Closed principle applied at the system level.

---

**Q13. What was the hardest engineering problem in building Desearch AI?**

*Why asked:* This open-ended question reveals how you think about difficulty and problem-solving.

*Key points expected:*
- Point to a specific concrete problem: coordinating five sequential agents through a shared research session context layer without coupling them directly, managing LLM context size as research findings accumulate across five agents, or designing approval checkpoints (AWAITING_PLAN_APPROVAL, AWAITING_FACTCHECK_APPROVAL) that pause a multi-step pipeline durably.
- Describe the problem clearly, explain why it was hard, explain the solution chosen, and acknowledge its trade-offs.

---

**Q14. What engineering decisions did you make and why?**

*Why asked:* This evaluates decision-making maturity. Interviewers want to hear that you considered alternatives and chose deliberately.

*Key points expected:*
- Reference specific decisions from the 15 engineering decision records: multi-agent architecture, central orchestrator pattern, shared research session context, provider-agnostic LLM abstraction, tool registry pattern.
- For each, name the problem, the alternatives considered, why the chosen option was selected, and the trade-offs.
- Demonstrate that you can articulate the "why" behind a decision, not just the "what."

---

**Q15. How did you handle the free-tier constraint without compromising research quality?**

*Why asked:* Constraint-driven engineering is a valuable skill.

*Key points expected:*
- Provider-agnostic design allows switching to a different free-tier provider by configuration change if quota is exhausted.
- Token usage logging per agent provides early warning of quota consumption.
- Research agents are designed to be selective about context: each agent reads only the relevant subset of research session context for its step, not the entire accumulated context.
- Stateless services prevent always-on compute costs.

---

**Q16. How is Desearch AI deployed? How would someone reproduce the deployment from scratch?**

*Why asked:* Cloud deployment and reproducibility are operational engineering skills.

*Key points expected:*
- Frontend deployed to cloud static hosting; backend deployed to cloud compute service.
- All secrets managed as environment-level secrets, never in source code.
- Deployment documentation enables a clean-environment deployment in under 30 minutes.
- Health endpoint used to verify post-deployment operational status of all core components.

---

**Q17. How is Desearch AI different from just asking ChatGPT to research a topic?**

*Why asked:* This is a direct challenge to the project's substance.

*Key points expected:*
- ChatGPT uses its training data; Desearch AI invokes real external tools (web search, page reader, document reader) to ground findings in live sources.
- ChatGPT produces a single response; Desearch AI produces a verifiable pipeline: the Research Agent's findings pass through a Fact Checker before the Writer produces the report.
- ChatGPT has no execution trace; Desearch AI logs every agent action, tool call, and LLM request — the research process is fully auditable.
- ChatGPT has no human checkpoint; Desearch AI allows the user to review and approve the research plan and validated findings before the report is written.

---

**Q18. How would you scale Desearch AI to support hundreds of concurrent research sessions?**

*Why asked:* Scalability thinking is expected at the senior engineer level.

*Key points expected:*
- Stateless backend services already support horizontal scaling — adding instances requires no architectural changes.
- A task queue decouples research query submission from pipeline execution and handles burst traffic.
- Each of the five agents is an isolated execution unit that can be scaled independently (e.g., more Research Agent instances during high tool-usage periods).
- The research session context and persistence layers use managed cloud services that handle scaling transparently.

---

**Q19. What would you build next for Desearch AI after the MVP?**

*Why asked:* Forward-thinking is a signal of senior engineering maturity.

*Key points expected:*
- Long-term persistent memory: agents recall findings from prior research sessions on related topics.
- PDF export: production-quality research reports with formatted citations and a table of contents.
- Citation management: automatic extraction, deduplication, and formatting of all cited sources.
- Streaming report generation: the Writer's report is delivered section-by-section as it is generated.
- Multi-LLM routing: different agents use different providers based on the nature of their task (e.g., a stronger model for the Fact Checker, a faster model for the Planner).

---

**Q20. What did you learn from building Desearch AI?**

*Why asked:* Reflective learning signals engineering growth mindset.

*Key points expected:*
- Be specific: name a concrete thing learned about multi-agent context propagation, LLM token budgeting across a five-step pipeline, or the complexity of durable HITL checkpoint state.
- Connect the learning to a decision you made or changed during the project.
- Acknowledge something that was harder than expected and what you would do differently — for example, the accumulated context size problem in the Writer Agent, or the complexity of designing the Fact Checker's validation prompt.

---

## STAR Stories

---

### STAR Story 1 — System Design Under Constraint for a Real Product

**Situation:**
I needed to build Desearch AI — a five-agent AI research platform — in a way that was deployable, publicly accessible, and demonstrable by evaluators, without any paid infrastructure. Free-tier cloud services impose strict limits on compute, storage, and API usage that are incompatible with naive multi-agent architectures that assume always-on, dedicated resources.

**Task:**
Design a system architecture that delivered production-grade research capabilities — five-agent orchestration, tool grounding, human oversight, and structured observability — while operating entirely within free-tier service quotas and remaining fully reproducible from a clean environment.

**Action:**
I made several deliberate architectural decisions to resolve this constraint. All backend services were designed as stateless: all research session state is externalized to managed storage, so services can start cold without data loss. The LLM integration layer was designed provider-agnostically, so if any free-tier provider exhausted its quota, Desearch AI could switch providers by configuration change alone. Each research agent was designed to read only its relevant subset of research session context rather than the entire accumulated context, keeping LLM inference requests within token limits and reducing per-session cost. The deployment was structured for maximum reproducibility: all configuration externalized, all secrets in environment variables, deployment documented to a 30-minute target.

**Result:**
Desearch AI operates fully within free-tier constraints, is publicly accessible at a stable URL, and can be reproduced by any engineer following the documented steps. The architecture decisions made to satisfy the constraint also produced production engineering best practices: stateless services for scalability, provider agnosticism for resilience, and context budget discipline for reliability in long research pipelines.

---

### STAR Story 2 — Designing Cross-Agent Context Propagation for a Five-Step Research Pipeline

**Situation:**
In a five-agent research pipeline, each subsequent agent needs access to the work of all prior agents: the Fact Checker Agent needs the Research Agent's findings, the Writer Agent needs the validated findings, the Reviewer Agent needs the draft report. The naive approach — having the Orchestrator explicitly pass each agent's output as direct input to the next — couples the Orchestrator's routing logic to the data contracts of every agent pair. This creates a system where adding a sixth agent requires modifying the Orchestrator, and where the Orchestrator becomes a complex data-routing component rather than an execution coordinator.

**Task:**
Design an inter-agent context propagation mechanism for the five-step research pipeline that is decoupled, transparent, and extensible — without the Orchestrator becoming responsible for carrying data between agents.

**Action:**
I designed a shared research session context layer as the context exchange mechanism. All five agents read from and write to a common context store keyed by session ID. The Orchestrator initializes the research session and dispatches agents but does not carry data between them — agents read what prior agents have written to research session context. I enforced session isolation at the interface level: cross-session reads are structurally impossible. I designed writes to be append-oriented, preserving the full context evolution history for execution trace reconstruction. Each agent reads only the subset of research session context it needs for its specific role, keeping inference context focused.

**Result:**
The Orchestrator's routing logic is completely decoupled from agent data contracts. Adding a new research agent requires only registering it and defining what it reads from and writes to research session context — no changes to the Orchestrator or existing agents. The append-oriented context model also became the primary source material for the execution trace, producing full research pipeline observability as a byproduct of the design rather than as a separate instrumentation effort.

---

### STAR Story 3 — Designing Human Oversight for a Research Pipeline That Matters

**Situation:**
Research outputs used for real decisions — technology selections, competitive analyses, investment assessments — carry consequence. A research pipeline that produces an unreviewed report based on poor source selection or unvalidated claims is not a trustworthy product. I needed to design a human oversight mechanism that was structurally integrated into the research pipeline, not an afterthought, and that supported practical workflow decisions: redirecting research scope before it is too late, or validating source quality before the report is written.

**Task:**
Design and implement a human-in-the-loop approval system with checkpoints positioned at the highest-leverage decision points in the research pipeline — after the Planner produces the research plan, and after the Fact Checker validates findings — with full support for approve, reject, and retry flows.

**Action:**
I implemented configurable HITL checkpoints as a first-class architectural component, not a wrapper around existing logic. Checkpoint placement was chosen based on research workflow logic: the plan checkpoint allows scope correction before expensive source gathering begins; the fact-check checkpoint allows evidentiary quality control before the Writer synthesizes the final report. Each checkpoint pauses the entire pipeline, persists its state durably (so a system restart does not lose an open checkpoint), surfaces the pending agent output to the user, and waits for an explicit decision. Every resolution — approve, reject, retry, or timeout — produces an immutable audit record. I implemented configurable timeout handling so that unresolved checkpoints escalate to a structured halt rather than hanging indefinitely.

**Result:**
Desearch AI's HITL system gives users genuine control over the research process at the points where it matters most. The durable checkpoint design means the system is correct across restarts. The audit trail means every user decision is traceable. The retry flow means a poor research plan can be corrected without restarting the entire session. This design was documented in a formal engineering decision record, making the design intent clear for future contributors.

---

## Metrics to Update After Implementation

Complete the following checklist after deployment. Do not invent values — fill in from actual measurement.

### Research Pipeline Performance
- [ ] Mean end-to-end research session time (five-agent, three-tool query): `__ seconds`
- [ ] P95 end-to-end research session time: `__ seconds`
- [ ] Mean LLM inference latency per agent request: `__ seconds`
- [ ] Mean tool invocation latency (web search): `__ ms`
- [ ] Mean tool invocation latency (web page reader): `__ ms`
- [ ] Mean tool invocation latency (document reader): `__ ms`
- [ ] API research query submission endpoint response time (acceptance): `__ ms`
- [ ] Execution trace retrieval response time: `__ ms`
- [ ] Cold-start latency (cloud compute, first request after inactivity): `__ seconds`

### Reliability
- [ ] End-to-end research session completion rate (sessions completed without error / sessions submitted): `__%`
- [ ] Tool invocation success rate: `__%`
- [ ] LLM inference success rate (first attempt, all agents): `__%`
- [ ] Agent retry rate (retries triggered / total agent invocations): `__%`
- [ ] Mean retries before success (when retry is triggered): `__`
- [ ] Graceful failure rate (structured error returned / total errors): `__%`
- [ ] Unhandled exception count in production: `__`

### Observability
- [ ] Structured log events emitted per average five-agent research session: `__`
- [ ] Execution trace completeness rate (traces with no missing events): `__%`
- [ ] Log schema compliance rate (events passing schema validation): `__%`
- [ ] Audit record completeness (HITL decisions with full audit record): `__%`

### Scale and Scope
- [ ] Number of registered agents: `__ / 5` (Planner, Research, Fact Checker, Writer, Reviewer)
- [ ] Number of registered tools: `__ / 3` (Web Search, Page Reader, Document Reader)
- [ ] Number of API endpoints: `__`
- [ ] Number of LLM providers supported: `__`
- [ ] Number of distinct research task types validated end-to-end: `__ / 3`
- [ ] Total engineering tickets completed: `__ / 52+`

### Testing
- [ ] Unit test count: `__`
- [ ] Integration test count: `__`
- [ ] End-to-end test count: `__`
- [ ] Test coverage (backend): `__%`
- [ ] Acceptance criteria passed (out of 11): `__ / 11`
- [ ] MVP success criteria satisfied (out of 6): `__ / 6`

### Deployment
- [ ] Time to deploy from clean environment (following documented steps): `__ minutes`
- [ ] Cloud deployment uptime since initial deployment: `__%`
- [ ] Free-tier quota utilization (LLM provider tokens, monthly): `__ / __ tokens`
- [ ] Cloud compute free-tier hours consumed (monthly average): `__ / __ hours`
- [ ] Number of public URL evaluations confirmed functional: `__`

### Human-in-the-Loop (Research Checkpoints)
- [ ] Mean time from checkpoint creation to user resolution: `__ seconds`
- [ ] Research plan checkpoint approval rate: `__%`
- [ ] Research plan checkpoint rejection rate: `__%`
- [ ] Research plan checkpoint retry rate: `__%`
- [ ] Fact-check checkpoint approval rate: `__%`
- [ ] Fact-check checkpoint rejection rate: `__%`
- [ ] Checkpoint timeout rate: `__%`
