# Changelog

All notable changes to this project will be documented in this file.

The format is based on the principles of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project follows
[Semantic Versioning](https://semver.org/).

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
