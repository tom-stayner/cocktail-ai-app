# Deployment

The application currently runs locally for development; it is not deployed to AWS hosting infrastructure.

## Current Deployment Model

- Run the FastAPI app with Uvicorn from the project root.
- Configure `AWS_REGION` and `TABLE_NAME` before launching the service.
- Provide AWS credentials through the standard AWS credential provider chain so the application can access DynamoDB.

## Operational Notes

- Logging is written to the local logs directory.
- Health checks are available through the /health endpoint.
- The application is not yet packaged for cloud deployment.

## Future Direction

The next deployment milestone is to move the service into a hosted AWS environment while preserving the existing FastAPI structure and service layer.

See [aws.md](aws.md) for the AWS architecture direction and [local setup](../setup.md) for local setup.
