# Security Policy

At **Desearch AI**, we take security seriously. As a cloud-native AI research platform handling research data, external tool integrations, and LLM inference, protecting user context, API keys, and infrastructure is a top priority.

---

## Supported Versions

Only the latest release version receives security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

---

## Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in Desearch AI, please follow our responsible disclosure process:

1. **Email Details**: Send a detailed report to **security@example.com**.
2. **Include Details**:
   - Type of issue (e.g., secret exposure, injection risk, unauthorized access, SSRF, dependency vulnerability).
   - Step-by-step instructions or proof-of-concept (PoC) to reproduce the issue.
   - Affected components (e.g., API Layer, Tool Layer, Frontend, Orchestrator).
   - Any potential impact or exploit scenarios.
3. **Response Timeline**:
   - **Acknowledgment**: Within 24 hours of receiving the report.
   - **Assessment & Triage**: Within 3 business days.
   - **Patch Release**: High severity issues patched within 7 business days.

We kindly ask that you keep vulnerabilities confidential until we have released an official patch or resolution.

---

## Security Best Practices in Desearch AI

### 1. No Secrets in Source Control
- All API keys, credentials, database connection strings, and tokens MUST be passed via environment variables or managed cloud secrets.
- Never commit `.env` or configuration files containing real credentials to Git. Use `.env.example` as a template.

### 2. Input Sanitization & Prompt Injection Protection
- All natural language research queries submitted by users undergo input validation and sanitization at the API Layer boundary before reaching LLM inference or tool execution.
- Tool input parameters are strictly validated against JSON schema definitions before execution.

### 3. API Key & Credential Isolation
- LLM provider API credentials and third-party tool API keys are accessible only by backend microservices.
- Credentials are never exposed to client-side code, frontend bundles, execution traces, or public log streams.

### 4. Session & Data Isolation
- Research session context is strictly isolated by session ID (`session_id`). Cross-session context reading or writing is prohibited and enforced at the Memory Layer interface level.

### 5. Transport Security
- All internal microservice-to-microservice traffic and external LLM/Tool provider API traffic MUST use TLS (HTTPS). Plaintext HTTP communications are prohibited in production environments.

### 6. Dependency Auditing
- Automated security scanners and dependency vulnerability audits are executed on every build to prevent supply-chain vulnerabilities.
