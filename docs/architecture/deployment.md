# Deployment

The application currently runs locally for development; it is not deployed to AWS hosting infrastructure.

## Current Deployment Model

- Run the FastAPI app with Uvicorn from the project root.
- Supply application settings through environment variables or a local `.env` file.
- Provide AWS credentials through the standard AWS credential provider chain so the application can access DynamoDB.

## Operational Notes

- Application logging is written to the console. A future Lambda deployment can forward standard output and standard error to CloudWatch without application-managed log files.
- `/health` preserves the backward-compatible basic response, `/health/live` reports process liveness, and `/health/ready` checks DynamoDB availability.
- The health endpoints are suitable for future container or load-balancer probes, but are not currently wired into deployment infrastructure.
- Read and HTML routes remain callable, while cocktail POST, PUT and DELETE routes return HTTP 403 by default because `ALLOW_MUTATIONS` is fail-closed.
- The application is not yet packaged for cloud deployment.

## Lambda Adapter Boundary

Mangum provides the ASGI-to-Lambda adapter around the existing FastAPI application. The future Lambda handler reference is `src.lambda_handler.handler`, and API Gateway HTTP API payload format `2.0` is the supported and tested event shape.

Local development continues to use `src.main:app` through Uvicorn. This adapter does not create or deploy a Lambda function, API Gateway, IAM role, or any other AWS infrastructure.

## Lambda Package and CI Boundary

The Lambda ZIP is generated with `scripts/lambda_package.py` for CPython 3.14 on
Linux x86-64. Its archive root contains the complete `src/` package, `static/`
assets and runtime dependencies such as Mangum and FastAPI. There is no enclosing
project directory, so the handler remains addressable as
`src.lambda_handler.handler`.

The package excludes development dependencies, tests, documentation, repository
metadata, local environment files and Python caches. Its structural audit checks
the handler and application modules, runtime dependencies, CSS and favicon assets,
archive paths, duplicate entries, symbolic links and prohibited development or
local content.

GitHub Actions runs the full test, Ruff and Black checks before building the
runtime-only package. A second job audits and extracts the archive, then imports and
invokes the packaged handler in an empty Linux virtual environment. The smoke test
covers health, stylesheet and favicon responses without calling DynamoDB.

CI requires no AWS credentials and performs validation only. It does not upload or
deploy the package, create infrastructure or publish a release. Hosting,
permissions and deployment remain separate future work.

`ALLOW_MUTATIONS=true` is intended only for trusted local development or test
environments. The setting is a safety control rather than an authentication or
authorisation boundary. The Lambda adapter, API Gateway event handling and AWS IAM
do not add application-user authentication, and this release adds no authentication
or deployment infrastructure.

## Future Direction

The next deployment milestone is to move the service into a hosted AWS environment while preserving the existing FastAPI structure and service layer.

Future Lambda deployment packages should install from `requirements.txt` so they contain only application runtime dependencies. Contributor and CI environments should install `requirements-dev.txt`; development tools should not be included in Lambda artefacts.

See [aws.md](aws.md) for the AWS architecture direction and [local setup](../setup.md) for local setup.
