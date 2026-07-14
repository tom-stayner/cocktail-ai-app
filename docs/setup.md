# Local Setup

This document is the detailed local setup guide. For a project overview and quick start, see the [README](../README.md).

## Prerequisites

- Python 3.14+
- a virtual environment
- AWS credentials available through the standard AWS credential provider chain
- access to the DynamoDB table configured by environment variables

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create a `.env` file in the project root with:
   - `AWS_REGION`
   - `TABLE_NAME`
   `LOG_LEVEL` may remain in the template for future use, but the current application logs at `INFO` and does not read it.
4. Start the app from the project root with `uvicorn src.main:app --reload`.

## Useful endpoints

- `/` for the HTML landing page
- `/health` for a basic health check
- `/docs` for the Swagger UI
- `/favicon.ico` for the browser favicon

See the [deployment notes](architecture/deployment.md) for the current operating model.
