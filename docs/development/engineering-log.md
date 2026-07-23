# Engineering Log

## 2026-07-23 — v0.4.0 Operational Readiness

### Context

The application needed clearer operational health signals, quieter and safer logging, centralised configuration, and stronger failure-path coverage before deployment work begins.

### Decisions

- Separated process liveness from dependency readiness while preserving the existing `/health` response for compatibility.
- Used DynamoDB `DescribeTable` for a lightweight, read-only readiness check.
- Assigned cocktail-operation logging primarily to the service layer and standardised application records on the named `cocktail_api` logger.
- Introduced immutable central settings with fail-fast validation for application, AWS, and logging configuration.
- Expanded network-free tests around invalid input, missing resources, DynamoDB interactions, dependency degradation, and unexpected failures.
- Kept unexpected DynamoDB exceptions visible rather than hiding them behind broad exception handling.

### Trade-offs

- `DescribeTable` requires the runtime AWS identity to have `dynamodb:DescribeTable`.
- Settings are loaded once; configuration changes require a process restart.
- General DynamoDB exceptions still propagate pending a future API error policy.
- Update requests still accept both path and body IDs, with the path ID authoritative.

### Outcome

The application now has stronger operational contracts while remaining simple, local-first, and deployment-neutral.

---

## 2026-07-14

### Documented AI-Assisted Development Workflow

#### Decision

Introduced `docs/development/ai-development-workflow.md` to formally document the project's AI-assisted software engineering process.

#### Reason

As the project evolved, AI tools became integrated into the engineering workflow rather than being used solely for code generation. Different tools naturally assumed specialised roles:

- Product Owner and Engineering Lead
- Software Architect
- Software Engineer
- Engineering Tooling

Documenting these responsibilities provides transparency into how architectural decisions are made, how implementations are reviewed, and how quality is maintained.

#### Outcome

The repository now documents not only the application's architecture, but also the engineering workflow used to develop it, providing future contributors with a clear understanding of the project's development methodology.

## 2026-07-14 — Repository Engineering Constitution (Version 1.0)

### Summary

Established `AGENTS.md` as the repository's Engineering Constitution: the durable source of engineering principles and governance for AI-assisted development.

### Why

The project will be developed collaboratively using AI coding agents (Codex) alongside human architectural oversight.

Rather than relying on detailed prompts for every task, the repository now defines stable principles for implementation, documentation, testing and verification. This gives human and AI contributors a shared basis for making consistent engineering decisions as the project evolves.

### Decisions

- Established `AGENTS.md` as the single source of truth for repository engineering principles.
- Defined a lightweight engineering workflow based on:
  - Review
  - Plan
  - Approval for architectural or structural changes
  - Implement
  - Verify
  - Summarise
- Introduced a Definition of Done for engineering tasks.
- Set documentation governance: distinguish current implementation from future direction and avoid presenting planned work as delivered.
- Established controlled evolution of the Constitution: agents recommend reusable improvements, and changes require explicit approval.
- Kept the Constitution focused on enduring engineering behaviour rather than feature-specific implementation detail.

### Outcomes

AI-assisted development should now consistently:

- Consider the wider impact of changes.
- Review documentation alongside implementation.
- Produce implementation plans before significant work.
- Seek approval before making architectural or structural changes.
- Verify changes before completion.
- Clearly separate implemented behaviour from planned direction in documentation.
- Summarise implementation outcomes and important decisions.
- Recommend improvements to engineering guidance rather than changing it automatically.

### Future Direction

`AGENTS.md` is intended to remain stable.

Changes should be infrequent and only made when repeated engineering experience identifies a genuinely reusable principle that benefits future development across the repository.

---

## 2026-07-14 - Health endpoint and Regression Tests (Version 1.0)

- Added a health endpoint for basic service monitoring.
- Moved cocktail CRUD logic behind a service layer to improve separation of concerns.
- Added regression tests for the health endpoint and cocktail collection route.
- Refined the architecture documentation to match the current implementation more closely.

## Notes

The project remains intentionally simple at this stage while the architecture is being established for future cloud and AI expansion.

---

## 2026-07-14 - Service-Layer Completion

- Removed direct DynamoDB access from HTML route handlers.
- Reused the existing collection and single-cocktail service operations to preserve CRUD behaviour and avoid duplicate data-access logic.
- Added regression tests covering the HTML routes' use of the service layer.
