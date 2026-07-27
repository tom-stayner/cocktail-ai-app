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
- A deterministic, audited Lambda ZIP can be built locally and in CI; no hosting infrastructure is provisioned.

## Lambda Adapter Boundary

Mangum provides the ASGI-to-Lambda adapter around the existing FastAPI application. The Lambda handler reference is `src.lambda_handler.handler`, and API Gateway HTTP API payload format `2.0` is the supported and tested event shape.

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

## Terraform Validation Boundary

Terraform is the approved infrastructure-as-code tool for v0.6.0. The repository
contains two independently initialized roots:

- `infra/terraform/bootstrap` defines only the protected S3 bucket intended for
  Terraform state. Its own state initially remains local and must not be applied
  until AWS execution and state migration are separately approved.
- `infra/terraform/environments/dev` defines a partial S3 backend and the
  configuration contract for a future development deployment. The backend uses
  native S3 lockfiles; bucket, key and region values are supplied through ignored
  local backend configuration.

The application root defines the private Lambda runtime, its least-privilege
execution role, explicit log group, immutable-version alias and baseline alarms.
These definitions have only been statically validated. They have not been planned
against AWS, applied or deployed. The existing `Cocktails` table is resolved as an
external data source and remains outside Terraform ownership.

GitHub Actions pins Terraform, checks formatting, initializes both roots with
`-backend=false` and validates them. CI supplies no AWS credentials and runs
neither `terraform plan` nor `terraform apply`.

## Defined Runtime Boundary

The defined function uses the audited ZIP as `src.lambda_handler.handler` on the
Python 3.14 Amazon Linux 2023 runtime with x86-64 architecture. It defaults to
256 MB memory, a 15-second timeout, immutable version publication and a `live`
alias. Terraform hashes the actual ZIP, so package changes change the function's
source-code hash.

The execution role trusts only Lambda. Its DynamoDB policy targets the resolved
existing table ARN and grants `DescribeTable`, `Scan` and `GetItem`; `PutItem` and
`DeleteItem` are conditional on `ALLOW_MUTATIONS=true`. Its separate log policy
grants only `CreateLogStream` and `PutLogEvents` for the managed function log
group. It does not grant log-group creation because Terraform defines the group
before the function.

Terraform configures all application settings except `AWS_REGION`, which is
reserved and supplied automatically by Lambda. `ALLOW_MUTATIONS` remains `false`
by default and is not an authentication or authorisation mechanism.

The managed log group retains records for 14 days. Error and throttle alarms use a
five-minute `Sum`, alarm at one or more events and treat missing data as
non-breaching. They have no notification actions.

The `live` alias points to the published function version rather than `$LATEST`.
Emergency rollback can repoint it to an earlier immutable version, followed by
approved Terraform configuration and state reconciliation. No rollback script is
provided.

`ALLOW_MUTATIONS=true` is intended only for trusted local development or test
environments. The setting is a safety control rather than an authentication or
authorisation boundary. The Lambda adapter, API Gateway event handling and AWS IAM
do not add application-user authentication, and this release adds no authentication
or deployment infrastructure.

## Future Direction

The v0.6.0 deployment milestone is to move the service into a hosted AWS
environment while preserving the existing FastAPI structure and service layer. It
will require an approved API Gateway/Lambda topology, least-privilege IAM,
CloudWatch operational configuration and later Terraform implementation steps.

No public endpoint or deployed AWS hosting infrastructure exists after this step.
API Gateway, Lambda invocation permission, planning, applying, deployment
automation and GitHub OIDC remain subject to separate approval.

The existing package builder installs from `requirements.txt` so the ZIP contains
runtime dependencies only. Contributor and quality environments install
`requirements-dev.txt`; development tools are excluded from Lambda artefacts.

See [aws.md](aws.md) for the AWS architecture direction and [local setup](../setup.md) for local setup.
