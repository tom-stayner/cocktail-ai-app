# AWS Architecture

The current implementation does not yet use a full AWS deployment. The application is designed to be compatible with an AWS-hosted future state.

## Current Implementation

- The backend uses DynamoDB as its persistence layer.
- Configuration is provided through the `AWS_REGION` and `TABLE_NAME` environment variables.
- The application runs locally and uses the standard AWS credential provider chain to access DynamoDB. It does not currently configure a local DynamoDB endpoint.

## Future Direction

A future version is expected to use:
- AWS Lambda or container-based hosting for the API
- Amazon DynamoDB as the primary data store
- Amazon Cognito for authentication
- Amazon S3 for image storage if media features are introduced

## Architectural Note

The repository keeps the AWS design intentionally lightweight at this stage so the implementation remains easy to evolve.

See [deployment.md](deployment.md) for the current operating model and [roadmap.md](roadmap.md) for planned milestones.
