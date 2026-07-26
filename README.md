# Cocktail AI App

A cocktail recipe application built with Python, FastAPI, and AWS DynamoDB. It currently runs locally and connects to a configured DynamoDB table.

Cocktail AI App is a Cloud & AI Engineering portfolio project focused on production-quality engineering practices while evolving toward a cloud-native, AI-powered cocktail companion.

**Current version:** 0.5.0 — Serverless Application Readiness

## Current Capabilities

- FastAPI JSON API and server-rendered HTML views
- Cocktail CRUD operations backed by DynamoDB
- Separate process-liveness and DynamoDB-readiness health endpoints
- Centralised, validated environment configuration
- Lambda-compatible console logging through the named `cocktail_api` logger
- Separate runtime and contributor dependency sets
- Mangum integration through `src.lambda_handler.handler`
- Deterministic, structurally audited Lambda ZIP packaging
- GitHub Actions quality checks and clean Linux packaged-handler verification
- Regression and resilience tests covering successful and failure paths
- Interactive Swagger API documentation

The application can produce a validated Lambda deployment package, but AWS Lambda,
API Gateway and supporting hosting infrastructure have not been provisioned. There
is no deployed public cloud endpoint.

## Getting Started

From the project root, activate a virtual environment, install dependencies, copy the environment template, and start Uvicorn:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn src.main:app --reload
```

`requirements-dev.txt` includes the runtime dependencies plus testing and code-quality tools. Runtime or deployment-only environments should install `requirements.txt`.

The application is available at `http://localhost:8000`; Swagger UI is available at `http://localhost:8000/docs`.

For prerequisites, AWS credentials, environment configuration, and available endpoints, see the [local setup guide](docs/setup.md).

For the current packaging boundary and future deployment direction, see the
[deployment architecture](docs/architecture/deployment.md).

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
