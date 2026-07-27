# Engineering Decisions — Desearch AI

> Product: **Desearch AI** — Deep Research. Smarter Decisions.
> Derived from: `Docs/PROJECT_VISION.md`, `Docs/REQUIREMENTS.md`, `Docs/SYSTEM_ARCHITECTURE.md`
> Updated: TICKET-007 — Product repositioning to Desearch AI
> Updated: Consistency Pass — Canonical example, terminology
> Scope: MVP — Engineering Decision Record (EDR)
> Status: Baseline

---

## Purpose

This document records the significant engineering decisions made for Desearch AI. Each entry explains the problem a decision addresses, the reasoning behind the chosen approach, the alternatives that were considered and rejected, the trade-offs introduced, and the implications for future development.

This is not an implementation guide. It does not prescribe code structure, library selection, or deployment steps. It records *why* the system is designed the way it is, so that future contributors and evaluators can understand the reasoning behind the architecture without having to reverse-engineer it from the code.

---

## EDR-01 — Multi-Agent Architecture

### Decision

The platform is built around a multi-agent architecture in which distinct, specialized agents collaborate to complete a task, rather than a single general-purpose agent handling all steps.

### Rationale

Research tasks are inherently heterogeneous. A query such as "Compare Supabase vs Firebase for Enterprise SaaS" requires fundamentally different cognitive operations: planning the scope of research, gathering source material from the web, validating factual claims, synthesizing findings into a structured report, and reviewing the report for quality. Assigning all of these operations to a single agent creates a prompt that is overloaded with conflicting responsibilities. The result is lower output quality, harder debugging, and an architecture that does not reflect how production AI systems are built.

A multi-agent approach allows each agent to be optimized for a narrow research role. The Planner Agent can be given a prompt and execution logic tuned for research scoping. The Research Agent can be optimized for source retrieval and tool invocation. The Fact Checker Agent, Writer Agent, and Reviewer Agent can each be given prompts, context access patterns, and evaluation logic tuned for their specific responsibilities. Each agent is independently improvable without affecting the others.

This decision also makes the architecture demonstrably modern. Multi-agent systems are the direction the field has moved toward; a platform that demonstrates multi-agent orchestration with clearly bounded research roles is a more credible engineering artifact than one that wraps a single LLM call.

### Alternatives Considered

1. **Single general-purpose agent** — One agent with access to all tools, a broad system prompt, and the responsibility to handle all subtasks within a single inference context.
2. **Sequential prompt chaining** — A pipeline of sequential LLM calls without agent identity or role boundaries, where the output of one call is the input to the next.

### Why Alternatives Were Rejected

A single general-purpose agent cannot be optimized for multiple domains simultaneously. A broad system prompt dilutes role focus, increases the risk of context confusion, and makes the agent harder to test and improve. It also does not scale: as tasks grow in complexity, a single agent's context window fills quickly, and there is no mechanism for parallel execution.

Sequential prompt chaining lacks structure. There is no concept of an agent with a defined role, a tool set, or a memory read/write interface. Failures are harder to isolate, retries are harder to implement, and the system produces no meaningful observability because there are no named, bounded execution units.

### Trade-offs

Multi-agent systems are more complex to build and coordinate than single-agent systems. The Orchestrator must correctly decompose tasks and route subtasks — a failure in routing produces incorrect or incomplete results that may not be immediately obvious. Agent boundaries introduce latency: each agent hand-off requires serialization, context reads, and a new inference request.

### Future Impact

The multi-agent design establishes the foundation for all future extensibility. Adding a new capability to the platform means adding a new specialized agent, not modifying existing ones. The architecture can accommodate arbitrarily many agents as the platform grows, without requiring changes to the Orchestrator's routing logic or the other agents' execution logic.

---

## EDR-02 — Central Orchestrator Pattern

### Decision

A single, dedicated Orchestrator component is responsible for task decomposition, agent routing, execution sequencing, result aggregation, and error coordination. No agent has knowledge of or responsibility for orchestration.

### Rationale

Distributing orchestration logic across agents — allowing agents to decide what to do next, which other agent to invoke, or how to handle failures — creates an emergent, implicit coordination model. Emergent coordination is difficult to observe, difficult to test, and difficult to reason about. When something goes wrong, it is unclear which agent made the routing decision that led to the failure.

Centralizing orchestration in a single component makes the system's behavior deterministic and inspectable. The Orchestrator owns the execution plan and is the authoritative record of what happened. Every routing decision, every retry, every checkpoint evaluation is made in one place and is attributable to one component.

This pattern also makes the system easier to extend. New agents can be registered with the Orchestrator without modifying any existing component. New orchestration policies (e.g., parallel dispatch, conditional routing) can be added to the Orchestrator without touching agents.

### Alternatives Considered

1. **Peer-to-peer agent coordination** — Agents communicate directly with each other, each deciding which agent to invoke next based on the current state.
2. **LLM-driven orchestration** — A meta-agent powered by an LLM makes all routing and sequencing decisions dynamically based on the task and the intermediate results.

### Why Alternatives Were Rejected

Peer-to-peer coordination produces a system that is difficult to observe and test. There is no single component that knows the complete execution state. Debugging a failure requires tracing communication across multiple agents. Adding a new agent requires modifying the agents that might need to invoke it. Circular invocation is a latent risk with no natural safeguard.

LLM-driven orchestration is non-deterministic. An LLM deciding which agent to invoke next may produce different routing decisions for identical inputs. This makes the system unpredictable, difficult to test, and unreliable in production. It also couples the correctness of orchestration to the quality of a prompt, which is fragile.

### Trade-offs

The central Orchestrator is a single point of failure. If the Orchestrator encounters an unrecoverable error, the entire task fails. This is mitigated by the Orchestrator's stateless design — it can be restarted or scaled horizontally without loss of task state, since all durable state is held by the Persistence Layer. However, it remains a coordination bottleneck that limits parallelism to what the Orchestrator explicitly plans for.

### Future Impact

The central Orchestrator is the natural place to implement more sophisticated execution strategies in future iterations: conditional branching, parallel agent dispatch, dynamic agent selection, and priority-based routing. All of these enhancements can be made within the Orchestrator without modifying any other component.

---

## EDR-03 — Specialized Agents Instead of a General Agent

### Decision

Each agent in the platform has a narrow, explicitly defined role, a bounded tool set, and an execution pattern optimized for that role. No agent is designed to handle arbitrary task types.

### Rationale

A general-purpose agent with broad instructions and access to all tools produces a system that is hard to test, hard to optimize, and hard to reason about. The prompt for a general agent must anticipate every possible task type and provide instructions for each, resulting in a large, unwieldy system prompt that frequently produces inconsistent behavior.

Specialized agents are easier to evaluate: their expected behavior is bounded by their role definition. A Research Agent should produce retrieved, relevant information — and that output can be evaluated against a clear standard. A Synthesis Agent should produce a coherent, structured analysis — and that can also be evaluated independently. When a specialized agent produces poor output, the cause is localized: it is a problem with that agent's prompt, tool set, or execution pattern, not a systemic problem with the entire pipeline.

Specialization also enables independent improvement. The Research Agent can be tuned and evaluated in isolation. Its performance improvements do not require changes to the Synthesis Agent.

### Alternatives Considered

1. **Single general-purpose agent** — One agent with a comprehensive system prompt handling all task types.
2. **Dynamically generated agents** — Agents whose roles and prompts are generated at runtime by a meta-agent or template engine based on the task.

### Why Alternatives Were Rejected

The single general-purpose agent argument is addressed in EDR-01 and EDR-02. The fundamental problem is that breadth of responsibility degrades the quality of any single responsibility.

Dynamically generated agents introduce non-determinism in agent design. An agent whose role definition changes per task is not a bounded execution unit — it is a general agent with extra indirection. It also makes observability harder: execution traces reference agent roles, and if those roles are dynamic, the traces are harder to interpret. Testing becomes nearly impossible because the agent's behavior depends on the quality of the generation step.

### Trade-offs

Specialization creates rigidity. If a task does not map cleanly onto the defined agent roles, the Orchestrator either fails to route it or routes it incorrectly. New task types that fall outside existing agent roles require the definition of a new agent — they cannot be handled by extending an existing one's prompt.

This is acceptable for the MVP, where the task domain is intentionally bounded. It becomes a maintenance concern as the platform expands to cover more diverse task types.

### Future Impact

The specialization decision establishes a clear pattern for adding capability: define a new role, implement a new agent with that role, and register it with the Orchestrator. The platform can grow its capability surface incrementally without requiring modifications to existing agents or the orchestration logic.

---

## EDR-04 — Shared Session Memory

### Decision

All agents within a single task execution share a common, session-scoped memory context. Agents write their results to this shared context and read prior results from it. No agent is required to receive its full context as a direct input from the Orchestrator.

### Rationale

In a multi-agent pipeline, context produced by one agent is almost always needed by subsequent agents. If the Orchestrator is responsible for passing this context explicitly — serializing Agent A's output and attaching it as input to Agent B's invocation — the Orchestrator becomes a context management component in addition to a coordination component. This makes the Orchestrator harder to reason about and creates a coupling between the Orchestrator's routing logic and the data formats expected by each agent.

Shared session memory decouples agents from each other and from the Orchestrator at the data level. Agent B simply reads the memory slot written by Agent A. The Orchestrator does not need to know which specific data Agent B will need; it only needs to know that Agent B should execute after Agent A.

This design also makes context evolution transparent. The memory layer's append-oriented write model preserves the full history of context changes within a session, which is directly useful for execution tracing and debugging.

### Alternatives Considered

1. **Orchestrator-mediated context passing** — The Orchestrator explicitly passes Agent A's output as a direct input to Agent B's invocation.
2. **Agent-to-agent direct communication** — Agents communicate directly with each other to share context without going through a shared store.

### Why Alternatives Were Rejected

Orchestrator-mediated passing creates a tight coupling between the Orchestrator's routing logic and the data contracts of every agent pair. Every new agent pairing requires the Orchestrator to be updated to know what data to extract from Agent A and what format Agent B expects. This is not extensible and makes the Orchestrator increasingly complex as the agent count grows.

Agent-to-agent direct communication is addressed and rejected in EDR-02. It produces undirected communication graphs that are difficult to observe and test, and it undermines the Orchestrator's role as the authoritative coordinator.

### Trade-offs

Shared memory introduces a form of implicit coupling: Agent B's behavior depends on what Agent A wrote, but this dependency is not expressed in the Orchestrator's routing graph — it is expressed in Agent B's execution logic. If Agent A writes incorrect or incomplete context, Agent B may fail in ways that are not immediately attributable to Agent A.

Session-scoped memory is also ephemeral by design for the MVP. Context does not persist beyond the task session, which means the platform has no memory of prior sessions. This is a deliberate MVP constraint, not a permanent architectural limitation.

### Future Impact

The session memory model is designed to be extended toward long-term persistent memory in future iterations. The interface — read and write by session-keyed entries — is compatible with persistent storage backends. Cross-session memory retrieval can be layered onto the same interface without modifying agents.

---

## EDR-05 — Human-in-the-Loop Approval

### Decision

The platform supports configurable checkpoints at which agent execution is paused pending explicit user authorization. Execution does not continue past a checkpoint until the user approves, rejects, or requests a retry.

### Rationale

Autonomous agent systems that execute without human oversight are appropriate for low-stakes, well-bounded tasks. For tasks involving consequential actions — making a retrieval decision, generating content that will be published, calling an external service with side effects — unbounded autonomy is an engineering risk.

The HITL approval layer is a first-class architectural component, not an afterthought. Including it in the MVP makes the platform suitable for a wider class of tasks and demonstrates a level of design maturity that distinguishes production AI systems from demo-quality prototypes. It also aligns with the emerging industry consensus that human oversight is a requirement, not an option, for production agent systems.

From an engineering perspective, the HITL layer provides a natural mechanism for task validation during development: engineers can pause execution at any step, inspect the agent's proposed action, and verify correctness before allowing execution to continue.

### Alternatives Considered

1. **Fully autonomous execution** — No checkpoints; agents execute all steps without human review.
2. **Post-execution review** — Task executes fully; user reviews the complete output after execution and can request a re-run.

### Why Alternatives Were Rejected

Fully autonomous execution is appropriate only when the agent's behavior is well-characterized and the consequences of an incorrect action are reversible. For an MVP platform that is being evaluated for the first time on arbitrary task inputs, this assumption is not justified. Fully autonomous execution also eliminates a key differentiator of the platform: the ability to demonstrate human oversight as a production-grade feature.

Post-execution review provides no mechanism for intervention. If an agent takes an incorrect intermediate action that corrupts the context for subsequent agents, the final output will be wrong, and the user's only recourse is to restart the task. This wastes execution time, LLM token budget, and tool invocations.

### Trade-offs

HITL checkpoints introduce latency. A task that requires human approval cannot complete without the user being present and responsive. If the user does not respond to a checkpoint within the configured timeout, the task must be halted or escalated. This is an acceptable trade-off for tasks where oversight is required, but makes the platform unsuitable for fully automated pipelines where human availability cannot be guaranteed.

The HITL layer also adds complexity to the state management model. The Human Approval Layer must maintain the state of open checkpoints durably, so that a checkpoint is not lost if the backend restarts between the pause and the user's response.

### Future Impact

The HITL mechanism is the foundation for more sophisticated oversight models in future iterations: role-based approval (different users approve different action types), approval escalation (automatic escalation to a secondary approver on timeout), and audit-grade compliance records for regulated use cases.

---

## EDR-06 — Tool Registry Pattern

### Decision

All tools available to agents are registered in a central tool registry. Agents interact with tools through the registry's uniform interface. No agent has a hardcoded dependency on any specific tool's implementation.

### Rationale

Without a registry, tool availability is determined by the agent's internal configuration. Adding a new tool requires modifying each agent that needs access to it. Removing a tool requires modifying each agent that invokes it. There is no authoritative source of what tools exist and what they do. Observability is partial: tool invocations are only logged if the agent remembers to log them.

A central registry solves all of these problems. The registry is the single authoritative source of tool identity and capability. New tools are added by registering them; existing agents gain access to new tools without modification. Tool invocations are logged at the registry boundary, so observability is complete regardless of which agent invoked the tool. Tool input validation is performed at the registry boundary, so agents are protected from malformed external responses.

The registry pattern also makes the platform's tool set self-describing: the Orchestrator can inspect the registry to understand what capabilities are available and use this information to improve routing decisions.

### Alternatives Considered

1. **Agent-owned tools** — Each agent maintains its own internal list of tools and directly invokes them without going through a registry.
2. **Hardcoded tool configuration** — Tools are defined as static configuration within each agent and cannot be changed without modifying the agent.

### Why Alternatives Were Rejected

Agent-owned tools create duplication: if two agents need access to the same tool, the tool's invocation logic must be duplicated in both agents. Changes to the tool's behavior or interface require modifications in multiple places. This violates the principle that each concern should be owned by exactly one component.

Hardcoded tool configuration is the worst-case version of agent-owned tools. It is the antithesis of extensibility and produces a system that cannot be adapted without modifying source code.

### Trade-offs

The registry introduces a layer of indirection between agents and tools. Every tool invocation passes through the registry boundary, which adds a small amount of latency and processing overhead compared to direct invocation. This is a negligible trade-off for the capabilities gained.

The registry also creates a dependency: if the registry is unavailable, no agent can invoke any tool. This is mitigated by the registry's role as an in-process component rather than a remote service for the MVP, but it becomes a reliability consideration if the registry is extracted into a separate service in future iterations.

### Future Impact

The registry pattern is the foundation for a plugin and agent marketplace in future iterations. Third-party tools can be registered without modifying the platform. Tool discovery, capability matching, and dynamic tool selection can be layered onto the registry interface. Tool versioning and deprecation can be managed centrally.

---

## EDR-07 — Structured Logging and Observability

### Decision

Every component in the platform emits structured log events — machine-parseable records with defined fields — rather than free-form text logs. Observability is treated as a first-class architectural requirement, not a debugging aid.

### Rationale

Free-form text logs are useful for human reading during active debugging, but they are not useful for systematic analysis, alerting, or audit. A production AI system generates large volumes of events across multiple components. Without structure, it is impossible to answer basic operational questions: How long did the Research Agent take on average? What is the tool failure rate for the search tool? Which sessions triggered HITL checkpoints?

Structured logging makes the system queryable. Every field is a filter dimension. Session ID, component identity, event type, and status are all queryable without parsing free-form text. This is what makes the platform's observability feature set genuinely useful rather than decorative.

For an AI system specifically, structured logging serves an additional purpose: it provides the raw material for behavioral analysis. Token usage per session, tool invocation patterns, and agent execution durations are all engineering signals that help identify performance regressions, cost growth, and reliability issues before they become user-facing problems.

### Alternatives Considered

1. **Free-form text logging** — Components emit human-readable log lines without a defined schema.
2. **No logging beyond error capture** — The platform only records errors; normal operations are not logged.

### Why Alternatives Were Rejected

Free-form text logging is not queryable at scale. Parsing log lines with regular expressions is fragile and expensive. Free-form logs cannot be reliably aggregated across components. They are not suitable for audit purposes.

No logging beyond error capture eliminates the ability to understand normal system behavior. Without a baseline of normal operation, anomalies cannot be detected. Without execution traces, the cause of incorrect output cannot be diagnosed. Without HITL audit records, the platform cannot demonstrate accountability for human approval decisions.

### Trade-offs

Structured logging requires every component to adhere to the logging schema. A component that emits a log event with missing or incorrect fields undermines the queryability of the log store. Maintaining schema consistency across all components requires discipline and enforcement — typically through a shared logging utility that components use rather than direct log emission.

Structured log volume is higher than selective error logging. More storage is consumed per event. For a free-tier deployment, this is a real constraint that must be managed through log retention policies and selective emission of high-cardinality fields.

### Future Impact

The structured logging foundation supports future additions of real-time monitoring dashboards, anomaly detection, and cost attribution per user or session. The audit trail produced by the logging system is directly applicable to compliance and governance use cases. The execution trace data is the raw input for future automated evaluation systems.

---

## EDR-08 — Cloud-Native Deployment

### Decision

The platform is designed and deployed as a cloud-native system from the outset. It assumes a cloud execution environment, uses managed services where available, and is designed to be publicly accessible via a stable URL without local installation.

### Rationale

A platform that runs only on a local machine is not evaluable by external stakeholders without significant setup effort. A cloud-deployed platform is accessible to anyone with a browser. For a project with resume and portfolio goals, public accessibility is a hard requirement: a recruiter or hiring manager must be able to interact with the platform without installing anything.

Beyond accessibility, cloud-native design produces better engineering outcomes. It forces discipline around externalized configuration, secrets management, and stateless service design — all of which are production engineering practices that would be obscured by a local-only deployment. Cloud deployment also makes the platform's reliability characteristics real: if a component fails in cloud deployment, it must recover or be replaced, not simply restarted manually.

The cloud-native constraint also aligns with the project's free-tier requirement. Managed cloud services — static hosting, compute services, managed storage — are available at no cost on free tiers. Local infrastructure (physical servers, dedicated hardware) is not a free-tier option.

### Alternatives Considered

1. **Local-only deployment** — The platform runs on the developer's local machine and is shared via a tunneling service.
2. **Containerized local deployment with documentation** — The platform is packaged for local execution and documented for self-hosting.

### Why Alternatives Were Rejected

Local-only deployment with a tunneling service is fragile. The platform is only accessible when the developer's machine is running and the tunnel is active. It cannot be used as a persistent, always-available demonstration artifact.

Containerized local deployment addresses portability but not accessibility. An evaluator must still install a container runtime, clone the repository, configure secrets, and run the build — a friction barrier that will prevent most non-technical evaluators from ever seeing the platform in action. It also does not validate that the platform works in a cloud environment, which is the environment where production AI systems actually run.

### Trade-offs

Cloud deployment within free-tier limits introduces resource constraints. Free-tier compute services have limited CPU, memory, and request throughput. Cold-start latency is a real issue on free-tier services that spin down inactive instances. The platform must be designed to be tolerant of these constraints rather than assuming dedicated, always-on infrastructure.

Free-tier services also impose usage limits that may be exceeded under sustained evaluation traffic. The platform must be documented with these limits clearly stated so that evaluators understand the operational boundary.

### Future Impact

Cloud-native design is directly compatible with future scaling. Horizontal scaling, managed queue services, and distributed storage are all cloud-native patterns that can be applied to the platform without architectural changes. The stateless service design established for the MVP is the prerequisite for horizontal scaling in production.

---

## EDR-09 — Provider-Agnostic LLM Design

### Decision

The platform interacts with the LLM provider through an abstraction layer that hides provider-specific request formats, response schemas, and credential management from all other components. Agents, the Orchestrator, and the Tool Layer have no knowledge of which LLM provider is configured.

### Rationale

LLM providers are a rapidly evolving market. New providers emerge regularly, existing providers change their APIs, and the relative cost-performance profile of providers shifts over time. A platform that hardcodes a dependency on a specific provider's API format is brittle: any breaking change in the provider's API requires modifications across every component that calls it.

The abstraction layer ensures that changing the LLM provider is a configuration change, not a code change. This is particularly important for the free-tier constraint: if the currently configured free-tier provider reduces its free quota or becomes paid-only, the platform must be able to switch providers without requiring a refactoring effort.

Provider-agnosticism is also a resume-relevant engineering signal. It demonstrates awareness of the principle of dependency inversion: high-level components should not depend on low-level implementation details. The agents are the high-level components; the specific LLM provider is an implementation detail.

### Alternatives Considered

1. **Direct provider coupling** — Each agent constructs and sends provider-specific inference requests directly.
2. **Multi-provider routing** — The platform routes each inference request to the most appropriate provider dynamically based on cost, latency, or capability.

### Why Alternatives Were Rejected

Direct provider coupling is the obvious failure mode. Every agent becomes tied to a single provider's API format. Testing agents in isolation requires mocking the provider's API. Switching providers requires touching every agent. This is not an acceptable design for a production-oriented platform.

Multi-provider routing is an advanced feature that is valuable but out of scope for the MVP. It introduces significant complexity: the routing logic must evaluate provider capabilities per request type, handle fallback when a provider is unavailable, and manage multiple sets of credentials. This complexity is not justified by the MVP's requirements and would slow delivery of the core capabilities. It is listed in Future Enhancements for exactly this reason.

### Trade-offs

The abstraction layer adds a translation step between the platform's internal inference request format and each provider's native API format. This translation logic must be maintained for each supported provider. For the MVP with a single configured provider, this is minimal overhead. As the number of supported providers grows, maintaining accurate translations becomes a non-trivial maintenance burden.

### Future Impact

The provider-agnostic design makes multi-LLM routing possible in future iterations without requiring changes to any agent or orchestration logic. The abstraction layer is also the natural place to implement token budget management, request caching, and response validation as the platform matures.

---

## EDR-10 — Stateless Backend Services

### Decision

The API Layer, Orchestrator, and Agent Layer are designed to hold no durable state between requests. All task state, session context, and execution records are externalized to the Memory Layer and Persistence Layer.

### Rationale

Stateful services are difficult to scale horizontally. If a service instance holds task state in memory, routing subsequent requests for the same task to a different instance produces incorrect behavior — the new instance has no knowledge of the prior state. Horizontal scaling of a stateful service requires either sticky routing (which limits scaling benefits) or state replication (which introduces consistency complexity).

Stateless services eliminate this problem entirely. Any instance of the API Layer or Orchestrator can handle any request at any time, because all state is held by external components that are accessible to all instances. This is the foundational property that makes the platform scalable.

Stateless design also improves fault tolerance. If an API Layer instance fails, in-flight requests can be retried against a different instance without task state loss, because the task state is in the Persistence Layer, not in the failed instance.

### Alternatives Considered

1. **Stateful service instances** — Each service instance maintains task state in memory for the duration of a task.
2. **Sticky session routing** — The load balancer routes all requests for a given session to the same service instance.

### Why Alternatives Were Rejected

Stateful service instances cannot scale horizontally without state replication. State replication across instances introduces distributed consistency problems that are significantly more complex than the problem being solved. A stateful service that fails loses all in-flight task state, requiring the user to restart tasks from scratch.

Sticky session routing is a workaround, not a solution. It preserves the ability to use stateful instances while routing all requests for a session to the same instance. But it undermines horizontal scaling: if the instance handling a session is overloaded, requests for that session cannot be offloaded to less-loaded instances. It also degrades fault tolerance: if the sticky instance fails, the session is lost.

### Trade-offs

Stateless design requires every operation that needs state to make a read from the Memory Layer or Persistence Layer. This adds latency to every stateful operation compared to in-memory access. For high-frequency operations, this latency is significant and must be managed through caching strategies.

The Memory Layer and Persistence Layer become critical dependencies. If either is unavailable, stateful operations cannot proceed. This shifts the reliability concern from the compute services (which are stateless and replaceable) to the storage services (which must be highly available).

### Future Impact

Stateless backend services are the prerequisite for horizontal scaling. Adding compute capacity is a matter of deploying additional service instances behind a load balancer — no architectural changes required. The stateless design also simplifies zero-downtime deployment: new versions of a service can be deployed alongside existing versions and traffic shifted gradually without session loss.

---

## EDR-11 — Modular Component Architecture

### Decision

Each system component — Frontend, API Layer, Orchestrator, Agent Layer, Tool Layer, Memory Layer, Human Approval Layer, Persistence Layer, LLM Provider Integration — is defined with a bounded responsibility and interacts with other components only through well-defined interfaces. No component has knowledge of another component's internal implementation.

### Rationale

A monolithic system — in which all concerns are implemented in a single, undifferentiated codebase — is easier to build initially but becomes increasingly difficult to maintain, test, and extend as complexity grows. In a monolith, a change in one area of the code can produce unintended side effects in unrelated areas. Testing requires the entire system to be running. Adding a new capability requires understanding the entire codebase.

Modular architecture solves these problems by establishing clear boundaries. Each module can be tested in isolation by mocking its interfaces. Changes within a module do not affect other modules as long as the interface contract is preserved. New capabilities are added by extending or adding modules, not by modifying existing ones.

For an AI platform specifically, modularity is also an extensibility requirement. The platform must be able to accommodate new agents, new tools, and new LLM providers without requiring architectural changes. This is only achievable if the components that define agents, tools, and providers are modular and independently replaceable.

### Alternatives Considered

1. **Monolithic architecture** — All components implemented in a single service with no defined internal boundaries.
2. **Microservices from day one** — Each component deployed as an independent service with network communication between them.

### Why Alternatives Were Rejected

A monolithic architecture is not extensible in the way this platform requires. Adding a new agent in a monolith means modifying the shared codebase and potentially affecting the Orchestrator, existing agents, and the API Layer simultaneously. Observability is harder because there are no component boundaries to emit events at. Testing is harder because the entire system must be running to test any individual concern.

A full microservices deployment from day one introduces operational complexity that is not justified at the MVP stage. Each service requires its own deployment pipeline, health monitoring, and inter-service communication infrastructure. On free-tier cloud resources, running a dozen separate services is not viable. The architecture is designed so that components are logically modular — with defined boundaries and interfaces — but can be deployed within a smaller number of physical services for the MVP. The physical deployment can be decomposed as the platform scales, without requiring changes to the logical architecture.

### Trade-offs

Enforcing module boundaries requires discipline. It is always tempting, under time pressure, to reach directly into another component's internals rather than going through its defined interface. Without consistent enforcement, module boundaries erode over time, and the system becomes a modular-in-name-only monolith.

Modular design also requires upfront investment in interface design. The interface between the Orchestrator and the Agent Layer, for example, must be defined carefully: it must be generic enough to accommodate any agent role, but specific enough to be useful for routing and error handling.

### Future Impact

The modular design is the primary enabler of the platform's long-term extensibility. Each module can be evolved, replaced, or scaled independently. The logical module boundaries defined in the MVP provide the natural seams along which the system can be decomposed into independent services when the scale and operational requirements justify it.

---

## EDR-12 — Free-Tier-First Design Philosophy

### Decision

Every infrastructure and service dependency in the platform is evaluated first for free-tier availability. No component may have a paid dependency as a hard requirement. The platform must function fully within free-tier service quotas under normal demonstration conditions.

### Rationale

The free-tier constraint is not a cost-cutting measure — it is an accessibility and reproducibility requirement. A platform that requires paid API subscriptions cannot be deployed and demonstrated by a developer who does not have a billing account or is unwilling to incur costs. It cannot be reproduced by a hiring manager or open-source contributor who wants to evaluate or contribute to the project. Paid dependencies create a friction barrier that reduces the project's value as a public engineering artifact.

The constraint also forces better engineering discipline. When a component must work within tight resource limits, the design must be efficient. Over-fetching, redundant calls, and wasteful token usage are not acceptable. These are exactly the engineering qualities that distinguish a production-oriented system from a demo prototype.

Finally, free-tier availability does not imply low quality. Major cloud and AI providers offer free tiers with sufficient capability for the platform's MVP requirements. The free-tier constraint is compatible with production-grade design.

### Alternatives Considered

1. **Best-in-class tooling regardless of cost** — Choose the most capable and convenient services without cost constraints, and document the expected monthly cost.
2. **Self-hosted alternatives for all dependencies** — Replace paid cloud services with self-hosted open-source equivalents running on free compute.

### Why Alternatives Were Rejected

Best-in-class tooling regardless of cost eliminates reproducibility. A platform that costs money to run can only be demonstrated by its author. This significantly reduces its value as a public engineering artifact and undermines the resume and portfolio objectives.

Self-hosted alternatives introduce operational complexity that is not justified at the MVP stage. Running self-hosted services on free compute requires managing infrastructure, updates, and failures that are not related to the platform's AI engineering concerns. They also typically have worse reliability and availability than managed services, which conflicts with the production-oriented quality standard.

### Trade-offs

Free-tier services have resource limits: compute CPU and memory, storage quotas, request rate limits, and monthly usage caps. The platform must be designed with these limits in mind. Cold-start latency is a real issue on free-tier compute services. Token usage must be managed to avoid exceeding LLM provider free-tier quotas. These constraints produce a platform that is sufficient for demonstration but not capable of production-scale traffic.

### Future Impact

The free-tier-first design makes the platform easily reproducible and forkable. Any engineer can clone the repository, configure the documented environment variables, and deploy a running instance at zero cost. This makes the platform genuinely open-source friendly and maximizes its value as a community reference implementation. Paid alternatives can be substituted at any integration point without architectural changes, since all service dependencies are abstracted behind interfaces.

---

## EDR-13 — Error Recovery Strategy

### Decision

The platform implements a layered error recovery strategy: retry at the step level, retry at the tool level, and structured halt at the task level. Every error is caught at a component boundary, logged as a structured event, and results in a deterministic terminal state. No error produces a silent hang or an unhandled exception visible to the user.

### Rationale

A production AI system that crashes on the first agent failure is not production-grade. LLM provider APIs are not perfectly reliable: they experience transient errors, rate limits, and occasional timeouts. External tool APIs fail. Agent outputs occasionally violate expected formats. A system that cannot recover from these routine failure modes is brittle by design.

The layered recovery strategy is calibrated to the severity of the failure:

- A **tool-level retry** handles the most common failure mode: a transient external service error that resolves on a second attempt.
- A **step-level retry** handles agent failures that may be caused by a malformed LLM response or a temporary context issue that resolves on a fresh attempt.
- A **structured halt** handles persistent failures where retries have been exhausted and the system cannot make progress. A structured halt is better than an infinite retry loop and better than a silent failure.

Every failure, regardless of level, produces a log event and an updated execution record. The user always knows what happened and why.

### Alternatives Considered

1. **No retry — fail immediately on any error** — Any component failure immediately halts the task with an error response.
2. **Unlimited retry** — The system retries indefinitely until success, with no halt condition.

### Why Alternatives Were Rejected

No retry is brittle. Transient errors — the most common category of errors in networked systems — cannot be distinguished from permanent failures, and the user pays the full cost of a task restart for every transient error. This produces a poor user experience and wastes LLM token budget on tasks that could have completed with a simple retry.

Unlimited retry is the opposite problem. A permanent failure (e.g., a tool that will never succeed because the external service is down) produces an infinite loop that consumes resources without making progress. It also introduces unbounded latency: the user has no way to predict when the task will complete or halt.

### Trade-offs

Retry introduces latency. A step that fails and is retried three times before succeeding takes four times the latency of a step that succeeds on the first attempt. The maximum latency of any step is bounded by (max retries × step timeout), which must be accounted for in the overall task execution timeout.

Retry also consumes LLM tokens and tool invocations. A failed LLM inference request that is retried still costs the tokens of the failed attempt. On a free-tier LLM provider with strict monthly token limits, retry policies must be conservative.

### Future Impact

The retry strategy can be made more sophisticated in future iterations: exponential backoff, jitter, circuit breakers for persistently failing tools, and per-agent retry configuration. The structured error envelope format established in the MVP provides the data needed to support these enhancements.

---

## EDR-14 — Session Isolation Strategy

### Decision

Each task execution is assigned a unique session ID. All state associated with that execution — session memory, execution trace events, approval checkpoints — is keyed by session ID. No operation may read or write state belonging to a different session.

### Rationale

Without session isolation, concurrent task executions can corrupt each other's state. Agent A writing to session memory in Task 1 must not be visible to Agent B reading from session memory in Task 2. An approval checkpoint created for Task 1 must not be surfaced to the user of Task 2.

Session isolation is both a correctness requirement and a security requirement. It is a correctness requirement because cross-session state leakage produces incorrect agent behavior. It is a security requirement because in a multi-user environment, cross-session state leakage is an information disclosure vulnerability.

Enforcing isolation at the interface level — requiring a valid session ID on every state operation — is more robust than relying on application-level discipline to avoid cross-session access. The interface makes incorrect behavior impossible by design rather than by convention.

### Alternatives Considered

1. **Global shared state** — All task executions share a single memory and log namespace, with in-application logic responsible for preventing cross-task interference.
2. **Per-task service instances** — Each task is handled by a dedicated service instance that holds all task state in memory and is terminated when the task completes.

### Why Alternatives Were Rejected

Global shared state with in-application isolation is fragile. A single bug — writing to the wrong key, reading without filtering by session — produces cross-task interference. In a concurrent system, this bug may be intermittent and difficult to reproduce. The isolation guarantee is only as strong as the application code's discipline.

Per-task service instances provide strong isolation but are not compatible with free-tier resource constraints. Spawning a new service instance for every task requires container orchestration infrastructure that is not available on free-tier compute. It also introduces significant latency: task startup latency includes the time to provision and start a new instance.

### Trade-offs

Session-keyed state requires that every component carry the session ID through every operation. This is a pervasive requirement that touches the API Layer, Orchestrator, Agent Layer, Memory Layer, and Persistence Layer. Any component that drops the session ID from an operation cannot be correctly isolated.

Session ID management also requires a session lifecycle: sessions must be created, maintained through the task execution, and cleaned up after completion or expiry. This lifecycle management adds complexity that would not be present in a simpler, non-isolated design.

### Future Impact

Session isolation is the prerequisite for multi-tenant support. In a multi-user environment, session IDs can be scoped to user identities, and access control policies can be enforced at the session level. The isolation infrastructure built for the MVP is directly usable in a multi-tenant architecture without fundamental changes.

---

## EDR-15 — Extensibility Strategy

### Decision

The platform is designed so that new agents, tools, and LLM providers can be added without modifying existing components. Extensibility is achieved through three mechanisms: a tool registry, an agent manifest, and an LLM provider abstraction. Each mechanism allows new entries to be added by registration, not by code modification.

### Rationale

The platform's value as a reference implementation is directly proportional to how easily it can be extended. A platform that requires forking and modifying core components to add a new agent or tool is not a useful reference — it is a fixed artifact that can only be used as-is.

The registry and manifest patterns enforce what is sometimes called the Open-Closed Principle at the system level: the platform is open to extension (new agents and tools can be added) but closed to modification (existing agents and tools do not need to change when new ones are added). This is the correct design posture for a platform that is intended to grow over time.

Extensibility is also a resume-relevant engineering quality. A platform designed with explicit extension points demonstrates that the designer was thinking beyond the immediate MVP requirements and building for long-term maintainability.

### Alternatives Considered

1. **Hardcoded component configuration** — Agents, tools, and providers are listed directly in the Orchestrator's and agents' source code. Adding a new one requires a code change.
2. **Plugin loading via convention** — New agents and tools are loaded automatically by scanning a directory or namespace for components that conform to a naming convention.

### Why Alternatives Were Rejected

Hardcoded configuration is the antithesis of extensibility. Every new agent or tool requires a code change, which requires a review, test, and deployment cycle. This friction discourages incremental extension and makes the platform rigid.

Plugin loading via convention is more dynamic but harder to reason about. The system's capabilities are determined at runtime by the contents of a directory, which makes static analysis and testing more difficult. It also creates a surface for unintended side effects if a poorly implemented plugin is loaded. Convention-based loading is a valid approach for mature, well-defined plugin systems, but introduces more complexity than is warranted for the MVP.

### Trade-offs

The registry and manifest approach requires that new agents and tools conform to the defined interface contracts. A new agent must implement the standard agent interface: it must accept a subtask and a session ID, read from and write to the Memory Layer, invoke tools through the registry, and return a structured output. If the interface contract is not well-defined, extension requires reverse-engineering the expected behavior from the existing implementations.

The manifest approach also requires a registration step: new agents and tools must be explicitly added to the manifest or registry before they are available. This is a minor operational overhead but prevents accidentally-loaded components from affecting the system.

### Future Impact

The extensibility mechanisms defined in the MVP are the direct foundation for a future plugin marketplace or agent registry. Third-party agents and tools can be published as packages that conform to the standard interface, and registered with the platform without any modification to the platform's core components. The manifest pattern can be extended to support versioned agent definitions, capability declarations, and compatibility constraints.
