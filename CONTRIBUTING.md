# Contributing to Desearch AI

Thank you for your interest in contributing to **Desearch AI**!

Desearch AI is a cloud-native, modular multi-agent AI research workbench. To maintain high engineering standards, production reliability, and documentation clarity, all contributors are required to follow the guidelines outlined in this document.

---

## Code of Conduct

All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold these standards.

---

## Development Workflow

We follow a structured, ticket-driven development workflow:

1. **Find or Create an Issue/Ticket**: Ensure your work corresponds to a tracked ticket or architectural specification in `docs/`.
2. **Branch from `main`**: Always branch from an up-to-date `main` branch.
3. **Make Atomic Commits**: Write clean, modular code with clear Conventional Commit messages.
4. **Run Local Checks**: Ensure code linting, formatting, and unit tests pass before opening a Pull Request (PR).
5. **Submit a Pull Request**: Submit your PR against `main` using our PR template and checklist.

---

## Git Conventions & Branch Strategy

We use a Git-flow inspired strategy to maintain clean branch history:

### Branch Strategy & Naming Conventions

| Branch Pattern | Purpose | Example |
| -------------- | ------- | ------- |
| `main` | Production-ready baseline. All releases tag from `main`. | `main` |
| `feature/*` | New capabilities, agents, tools, or UI modules. | `feature/fact-checker-agent` |
| `bugfix/*` | Non-urgent fixes for open issues or test failures. | `bugfix/llm-timeout-retry` |
| `hotfix/*` | Urgent production fixes applied directly to `main`. | `hotfix/cors-origin-header` |
| `release/*` | Release preparation branches for version cuts. | `release/v0.1.0` |

---

## Commit Message Conventions

We strictly enforce **Conventional Commits** (v1.0.0 specification).

### Format

```text
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

### Commit Types

- **`feat:`** A new feature or agent capability (e.g., `feat(agent): implement Planner Agent execution plan generator`).
- **`fix:`** A bug fix (e.g., `fix(orchestrator): handle timeout error on agent retry`).
- **`docs:`** Documentation changes only (e.g., `docs(architecture): update report output schema`).
- **`style:`** Code formatting, indentation, white-space fixes (no production logic change).
- **`refactor:`** Code refactoring without fixing a bug or adding a feature.
- **`test:`** Adding or updating unit, integration, or end-to-end tests.
- **`build:`** Changes that affect the build system or external dependencies.
- **`ci:`** Changes to CI/CD pipeline scripts or configuration.

### Examples

```bash
git commit -m "feat(tools): add Web Page Reader tool implementation"
git commit -m "fix(memory): fix session context isolation leak under concurrency"
git commit -m "docs(readme): update project roadmap and feature matrix"
```

---

## Versioning Strategy

Desearch AI strictly adheres to **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):

- **`MAJOR`**: Incompatible architectural changes or API breaking changes.
- **`MINOR`**: Backwards-compatible new features (e.g., adding a new research agent or tool).
- **`PATCH`**: Backwards-compatible bug fixes and stability improvements.

---

## Coding Standards

### Python (Backend Services)
- Adhere to **PEP 8** guidelines.
- Use explicit type annotations for all function parameters and return types.
- Follow docstring standards for all public classes, methods, and agent interfaces.
- Format with **Black** or **Ruff**, check types with **MyPy**.

### TypeScript & React (Frontend Workbench)
- Strict mode enabled (`strict: true` in `tsconfig.json`).
- Avoid `any` types; define explicit interfaces or types for all props and API responses.
- Functional React components with hooks.
- Format with **Prettier** and lint with **ESLint**.

### Markdown Documentation
- Follow GitHub Flavored Markdown (GFM).
- Keep bullet points concise and informative.
- Enforce explicit file links using standard relative markdown links.

---

## Pull Request Checklist

Before submitting a PR, verify the following:

- [ ] My code follows the project's coding standards.
- [ ] I have added/updated unit or integration tests for my changes.
- [ ] All tests pass locally.
- [ ] My commits follow Conventional Commits formatting.
- [ ] I have updated relevant documentation in `docs/` if architecture or interfaces changed.
- [ ] No hardcoded secrets, API keys, or `.env` files are included in the commit.
- [ ] My PR title follows Conventional Commit format (e.g., `feat(orchestrator): ...`).

---

## Review & Approval Process

1. **Automated Status Checks**: CI checks (linting, tests, static analysis) must pass.
2. **Peer Review**: At least one Lead Software Engineer review and approval is required.
3. **No Self-Merge**: Code must be merged by a maintainer after review approval.
