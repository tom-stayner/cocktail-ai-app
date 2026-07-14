# Cocktail AI App

A cocktail recipe application built with Python, FastAPI, and AWS DynamoDB. It currently runs locally and connects to a configured DynamoDB table.

Cocktail AI App is a Cloud & AI Engineering portfolio project focused on production-quality engineering practices while evolving toward a cloud-native, AI-powered cocktail companion.

## Current Capabilities

- FastAPI JSON API and server-rendered HTML views
- Cocktail CRUD operations backed by DynamoDB
- Service-layer separation, health monitoring, structured logging, and regression tests
- Interactive Swagger API documentation

## Getting Started

From the project root, activate a virtual environment, install dependencies, copy the environment template, and start Uvicorn:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn src.main:app --reload
```

The application is available at `http://localhost:8000`; Swagger UI is available at `http://localhost:8000/docs`.

For prerequisites, AWS credentials, environment configuration, and available endpoints, see the [local setup guide](docs/setup.md).

## Documentation

Additional project documentation can be found in the `docs/` directory.

- [Setup Guide](docs/setup.md)
- [Product Roadmap](docs/roadmap.md)
- [Architecture Overview](docs/architecture/overview.md)
- [Coding Standards](docs/development/coding-standards.md)
- [Engineering Log](docs/development/engineering-log.md)
- [AI-Assisted Development Workflow](docs/development/ai-development-workflow.md)
- [Changelog](docs/development/changelog.md)

Repository engineering governance is defined in [AGENTS.md](AGENTS.md).
