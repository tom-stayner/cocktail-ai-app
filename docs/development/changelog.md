# Changelog

All notable changes to this project will be documented in this file.

The format is based on the principles of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project follows
[Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Planned

- Configuration validation and configurable logging
- Expanded API and service-layer regression coverage
- Improved exception handling
- Docker support
- AWS deployment
- Amazon S3 image management
- Insights and analytics dashboard
- AI-powered cocktail recommendations

### Added

- Browser favicon served at `/favicon.ico`.

### Changed

- Reorganised documentation and repaired internal navigation after file moves.
- Routed all HTML cocktail views through the service layer, removing direct DynamoDB access from route handlers.

---

## [0.3.0] - 2026-07-14

### Added

- Modular project structure with dedicated modules for database, models and logging.
- Structured application logging with both console and file output.
- Professional project documentation, including setup, architecture and roadmap guides.
- MIT License.
- Public GitHub repository.
- `.env.example` configuration template.

### Changed

- Refactored the application from a single-file implementation towards a modular architecture.
- Introduced a service layer to progressively separate business logic from FastAPI route handlers.
- Reorganised documentation into a dedicated `docs/` hierarchy.
- Improved README to serve as a concise project landing page.

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
