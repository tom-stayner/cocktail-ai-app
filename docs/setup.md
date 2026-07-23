# Local Setup

This document is the authoritative guide for running Cocktail AI App locally. For a concise quick start, see the [README](../README.md).

## Prerequisites

- Python 3.14+
- A virtual environment
- AWS credentials available through the standard AWS credential provider chain
- Access to the DynamoDB table configured for the application

## Install and Run

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy the environment template with `Copy-Item .env.example .env` on Windows or `cp .env.example .env` on Linux or macOS.
4. Review the safe defaults in `.env` and change them when needed for your environment.
5. From the project root, start the application with `uvicorn src.main:app --reload`.

## Application Settings

| Variable | Default | Purpose |
| --- | --- | --- |
| `APP_NAME` | `Tom's Cocktail API` | FastAPI service name |
| `APP_VERSION` | `0.4.0` | Current application version |
| `APP_ENV` | `development` | Runtime environment |
| `AWS_REGION` | `ap-southeast-2` | AWS region |
| `TABLE_NAME` | `Cocktails` | DynamoDB table |
| `LOG_LEVEL` | `INFO` | Application logging threshold |

Supported `APP_ENV` values are `development`, `test`, and `production`.

Supported `LOG_LEVEL` values are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

Using a `.env` file is convenient for local development. Deployed environments should supply these values through their runtime configuration.

## Local Endpoints

- `/` — HTML landing page
- `/docs` — Swagger UI
- `/favicon.ico` — browser favicon

| Endpoint | Purpose | Dependency check |
| --- | --- | --- |
| `/health` | Backward-compatible basic health response | No |
| `/health/live` | Process liveness | No |
| `/health/ready` | Application readiness | DynamoDB |

`/health/ready` returns HTTP 200 when DynamoDB is available and HTTP 503 when it is unavailable. The AWS identity used by the application requires `dynamodb:DescribeTable` for this readiness check.

## Configuration and Security

Application settings are supplied through environment variables and are not stored in the repository. Do not commit `.env`, AWS credentials, API keys, or passwords.

The application uses the standard AWS credential provider chain to access DynamoDB and does not currently configure a local DynamoDB endpoint.

See [deployment notes](architecture/deployment.md) for the current operating model and [coding standards](development/coding-standards.md) for delivery expectations.
