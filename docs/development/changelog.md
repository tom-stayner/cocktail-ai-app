# Changelog

All notable changes to this project will be documented in this file.

The format is based on the principles of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project follows
[Semantic Versioning](https://semver.org/).

## [0.5.0] - 2026-07-27

**v0.5.0 — Serverless Application Readiness**

### Added

- Added Mangum as the runtime ASGI-to-Lambda adapter with the dedicated `src.lambda_handler.handler` entry point.
- Added API Gateway HTTP API payload-v2 adapter coverage for health, static stylesheet and favicon responses.
- Added Uvicorn and Lambda-path coverage for fail-closed cocktail mutation safeguards.
- Added GitHub Actions quality checks for the complete test suite, Ruff and Black.
- Added stable Lambda ZIP construction using runtime-only Linux x86-64 dependencies.
- Added structural and security auditing for Lambda package contents and paths.
- Added clean packaged-handler smoke tests covering health, stylesheet and favicon responses.
- Added release documentation aligned with the v0.5.0 application metadata.

### Changed

- Replaced local file-based application logging with console logging compatible with AWS Lambda and CloudWatch.
- Separated application runtime dependencies from development and test tooling.
- Runtime installations now use `requirements.txt`, while contributor environments use `requirements-dev.txt`.
- Preserved local Uvicorn execution through `src.main:app` alongside the Lambda adapter.
- Escaped stored cocktail content at server-rendered HTML boundaries while preserving original JSON values.
- Cocktail create, update and delete routes now return HTTP 403 by default through the fail-closed `ALLOW_MUTATIONS` setting.
- Trusted local and test environments can explicitly set `ALLOW_MUTATIONS=true` to preserve existing mutation behaviour.
- Application configuration and console logging now support both local Uvicorn and Lambda execution environments.

### Deployment

- The application is ready to package and validate for AWS Lambda, but this release does not provision or deploy Lambda, API Gateway, IAM, CloudWatch or other hosting infrastructure.

---

## [0.4.0] - 2026-07-23

### Added

- Separate liveness and DynamoDB readiness health endpoints.
- Centralised typed application configuration with validated environment settings.
- Expanded failure-path coverage for validation errors, missing resources, DynamoDB interactions and health-check degradation.

### Changed

- Preserved `/health` as a backward-compatible liveness endpoint.
- Readiness checks now return HTTP 503 when DynamoDB is unavailable.
- Successful health checks no longer generate application INFO logs.
- Reduced duplicate application logging between API routes and services.
- Classified routine reads and HTML rendering as debug-level events.
- Standardised application logs on the named `cocktail_api` logger.
- Avoided logging user-supplied cocktail content.
- Corrected DynamoDB startup logging to describe configuration rather than connectivity.
- FastAPI metadata, DynamoDB settings and application log level now use shared configuration.
- Local environment examples now provide safe project defaults.

---

## [0.3.0] - 2026-07-14

### Added
- Modular project structure with dedicated modules for database, models and logging.
- Structured application logging with both console and file output.
- Professional project documentation, including setup, architecture and roadmap guides.
- MIT License.
- Public GitHub repository.
- `.env.example` configuration template.
- Browser favicon served at `/favicon.ico`.

### Changed
- Refactored the application from a single-file implementation towards a modular architecture.
- Completed the service layer architecture, with all HTML and JSON routes now delegating business logic to `cocktail_service`.
- Database access is now encapsulated within the service layer and database module.
- Reorganised project documentation into a structured `docs/` hierarchy.
- Repaired internal documentation navigation following the documentation restructure.
- Improved README to serve as a concise project landing page.
- Clarified current and future architecture diagrams to avoid presenting planned AWS services or data structures as implemented.
- Added status and release metadata to Mermaid diagrams.
- Refined the AI-assisted development workflow and documented the current status of formatting and linting tools.

### Infrastructure
- AWS DynamoDB configuration isolated into a dedicated database module.
- Logging configuration extracted into a reusable module.
- Project prepared for future environment-based configuration.

### Documentation
- Added engineering log.
- Added coding standards.
- Added architecture documentation.
- Added project roadmap.
- Improved setup instructions.
- Added `docs/development/ai-development-workflow.md` documenting the project's AI-assisted software engineering workflow and team responsibilities.

---

## [0.2.0]

### Added

- FastAPI REST API.
- HTML interface for browsing cocktails.
- CRUD operations for cocktail management.
- AWS DynamoDB integration.

---

## [0.1.0]

### Added

- Initial project structure.
- FastAPI application.
- Basic cocktail data model.
