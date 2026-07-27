# Local Setup

This document is the authoritative guide for running Cocktail AI App locally. For a concise quick start, see the [README](../README.md).

## Prerequisites

- Python 3.14+
- A virtual environment
- Terraform 1.15.8 only for contributors performing infrastructure formatting and validation; ordinary local application use does not require Terraform
- AWS credentials available through the standard AWS credential provider chain when running DynamoDB-backed application routes
- Access to the configured DynamoDB table when exercising persistence or readiness locally

## Install and Run

1. Create and activate a virtual environment.
2. Install runtime and development dependencies with `python -m pip install -r requirements-dev.txt`.
3. Copy the environment template with `Copy-Item .env.example .env` on Windows or `cp .env.example .env` on Linux or macOS.
4. Review the safe defaults in `.env` and change them when needed for your environment.
5. From the project root, start the application with `uvicorn src.main:app --reload`.

`requirements.txt` contains only application runtime dependencies for production or deployment packaging. `requirements-dev.txt` includes those runtime dependencies through `-r requirements.txt`, plus the test, linting, and formatting tools used by contributors.

For a runtime-only installation, use `python -m pip install -r requirements.txt`.

## Local Quality Checks

The local quality workflow uses the contributor dependencies:

```text
python -m pytest
python -m ruff check .
python -m black --check .
```

GitHub Actions repeats these checks on pull requests and `main`. Tests and Lambda
package build/audit operations do not require AWS credentials; tests isolate AWS
interactions and packaging downloads dependencies without invoking AWS APIs.

## Terraform Validation

Terraform Step 1 is a repository foundation only. It defines no application
hosting resources and must be validated without AWS credentials, plans or applies:

```text
terraform fmt -check -recursive infra/terraform
terraform -chdir=infra/terraform/bootstrap init -backend=false
terraform -chdir=infra/terraform/bootstrap validate
terraform -chdir=infra/terraform/environments/dev init -backend=false
terraform -chdir=infra/terraform/environments/dev validate
```

Initialization downloads the declared provider from the Terraform Registry and
generates a tracked `.terraform.lock.hcl` in each root. The generated
`.terraform/` working directories remain ignored.

The bootstrap root is intentionally configured with local state until a separately
approved AWS execution and state-migration step. The development root uses a
partial S3 backend with native lockfiles. Supply its future bucket, key and region
through an ignored `*.tfbackend` file; do not commit backend configuration, state,
plans, credentials or environment-specific `.tfvars`.

Do not run `terraform plan` or `terraform apply` as part of Step 1. The existing
`Cocktails` DynamoDB table remains outside Terraform ownership.

## Lambda Package Build

Build the generated Lambda deployment archive from the project root:

```text
python scripts/lambda_package.py build --output dist/cocktail-ai-lambda.zip
python scripts/lambda_package.py audit --archive dist/cocktail-ai-lambda.zip
```

The builder installs runtime dependencies from `requirements.txt` only and targets
AWS Lambda's CPython 3.14 runtime on Linux x86-64. It requests compatible
manylinux2014 wheels and fails rather than falling back to host-specific packages.
The generated and ignored archive is written to
`dist/cocktail-ai-lambda.zip`; temporary staging content is removed automatically.

A package built on Windows intentionally contains Linux dependencies, so importing
it with the host Windows interpreter is not a meaningful compatibility test.
GitHub Actions builds and audits the package on Linux, extracts it into a clean
location, and invokes the packaged handler from a separate empty virtual
environment.

## Application Settings

| Variable | Default | Purpose |
| --- | --- | --- |
| `APP_NAME` | `Tom's Cocktail API` | FastAPI service name |
| `APP_VERSION` | `0.5.0` | Current application version |
| `APP_ENV` | `development` | Runtime environment |
| `AWS_REGION` | `ap-southeast-2` | AWS region |
| `TABLE_NAME` | `Cocktails` | DynamoDB table |
| `LOG_LEVEL` | `INFO` | Application logging threshold |
| `ALLOW_MUTATIONS` | `false` | Enable cocktail create, update and delete routes |

Supported `APP_ENV` values are `development`, `test`, and `production`.

Supported `LOG_LEVEL` values are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

`ALLOW_MUTATIONS` is fail-closed: it defaults to `false`, and only the explicit value
`true` enables POST, PUT and DELETE operations. Invalid values prevent application
startup. Set it to `true` only for trusted local development or test environments
that need to modify cocktail data. This switch is a safety control, not
authentication or authorisation, and deployed environments should leave it set to
`false`.

Using a `.env` file is convenient for local development. Deployed environments should supply these values through their runtime configuration.

## Logging

Application logs are written to the console and remain visible in the local Uvicorn terminal. The application does not create a log directory or manage log files.

When the application is hosted on AWS Lambda in a future deployment, Lambda will capture standard output and standard error for collection by CloudWatch. CloudWatch log groups and retention will be managed later through deployment infrastructure; this application change creates no AWS resources.

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

Server-rendered cocktail pages escape stored content before inserting it into HTML.
JSON endpoints continue to return the original stored values.

See [deployment notes](architecture/deployment.md) for the current operating model and [coding standards](development/coding-standards.md) for delivery expectations.
