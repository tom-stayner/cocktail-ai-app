# Deployment

The application currently runs locally for development; it is not deployed to AWS hosting infrastructure.

## Current Deployment Model

- Run the FastAPI app with Uvicorn from the project root.
- Supply application settings through environment variables or a local `.env` file.
- Provide AWS credentials through the standard AWS credential provider chain so the application can access DynamoDB.

## Operational Notes

- Logging is written to the local logs directory.
- `/health` preserves the backward-compatible basic response, `/health/live` reports process liveness, and `/health/ready` checks DynamoDB availability.
- The health endpoints are suitable for future container or load-balancer probes, but are not currently wired into deployment infrastructure.
- The application is not yet packaged for cloud deployment.

## Future Direction

The next deployment milestone is to move the service into a hosted AWS environment while preserving the existing FastAPI structure and service layer.

See [aws.md](aws.md) for the AWS architecture direction and [local setup](../setup.md) for local setup.
