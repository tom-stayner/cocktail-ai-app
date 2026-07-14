# Architecture Overview

This document gives the high-level shape of the Cocktail AI App and points to the more detailed architecture pages in this folder.

## Current Implementation

The project is currently a Python FastAPI application with:
- a small HTTP API for cocktail data
- HTML views served from the same application
- a service layer that separates business logic from route handlers
- DynamoDB as the persistence layer, configured through `AWS_REGION` and `TABLE_NAME`
- static CSS and a browser favicon served by the application

## Future Direction

The long-term direction is a cloud-native, AWS-based application with AI-assisted features. The current implementation is intentionally small and local-first so the core architecture can evolve without unnecessary complexity.

## Main Components

- FastAPI application: request handling and HTML rendering
- Service layer: cocktail CRUD operations and business logic
- DynamoDB table: persistent storage for cocktail records
- Logging: structured application logging for local operations

## Documentation Map

- [AWS architecture](aws.md): current AWS integration and planned hosting direction
- [Deployment](deployment.md): current local operating model and deployment milestone
- [Data model](data-model.md): persisted cocktail record shape
- [Product roadmap](../roadmap.md): planned evolution
- [Engineering log](../development/engineering-log.md): significant implementation history and decisions

For setup and project-wide delivery standards, see the [setup guide](../setup.md) and [coding standards](../development/coding-standards.md).
