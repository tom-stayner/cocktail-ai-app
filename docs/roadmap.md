# Product Roadmap

## Vision

Cocktail AI App is intended to become a cloud-native, AI-powered cocktail companion. It is also a portfolio project demonstrating professional software engineering, AWS architecture, and practical AI integration.

The product will evolve incrementally. Each stage should preserve maintainability, testing, documentation, and production-quality engineering practices.

## Current Implementation — v0.5.0 Serverless Application Readiness

The current application provides a tested FastAPI foundation that runs locally and
is ready to package for AWS Lambda:

- JSON cocktail CRUD endpoints and server-rendered HTML views
- DynamoDB-backed cocktail records, including ingredient lists
- a service layer separating route handlers from CRUD logic
- separate liveness and readiness endpoints with DynamoDB dependency checks
- centralised validated configuration and console-based structured logging
- separated runtime and contributor dependency sets
- a Mangum handler for API Gateway HTTP API payload-v2 events
- deterministic Linux x86-64 Lambda ZIP construction and structural auditing
- GitHub Actions quality checks and isolated Linux packaged-handler smoke tests
- regression and resilience tests covering validation and dependency failures
- aligned local setup, architecture, and operational documentation

The v0.5.0 release completes application-level serverless readiness. It does not
provision Lambda, API Gateway or other hosting infrastructure and does not expose a
deployed public endpoint. See the [architecture overview](architecture/overview.md)
for the current system shape.

## Planned Milestones

### v0.6.0 — AWS Deployment

Deploy the validated application package through an approved AWS architecture.
Expected concerns include Lambda, API Gateway, least-privilege IAM execution roles,
CloudWatch operational configuration and Terraform-managed infrastructure.

The first delivery step establishes separate Terraform bootstrap and development
application roots, protected S3 state design with native lockfiles, and
validation-only CI. The second step defines, but does not deploy, a private Lambda
runtime with least-privilege table access, explicit log retention, immutable
versions, a `live` alias and baseline error and throttle alarms. The existing
`Cocktails` table remains outside Terraform ownership.

Later steps will add and review API Gateway integration, invocation permission and
deployment automation. No AWS hosting resources or public endpoint are currently
provisioned.

### User Experience

Improve recipe discovery and usability through a modern, responsive interface. Likely capabilities include richer browsing, filtering and search, favourites, and a better mobile experience. A React frontend is a possible implementation direction, subject to the needs of the product at that stage.

### AI-Assisted Discovery

Introduce AI where it makes cocktail exploration more useful, rather than replacing conventional navigation. Potential capabilities include natural-language search, recommendations, ingredient substitutions, food-pairing suggestions, recipe explanations, and cocktail history or trivia.

### Accounts and Personalisation

Enable an individual experience with authentication, profiles, saved recipes and collections, preferences, and recently viewed cocktails. Amazon Cognito is the current anticipated authentication service, subject to architectural review when this milestone is started.

### Insights

Develop analytics that can create value for users, rather than a conventional administrative panel. This may include cocktail popularity, ingredient trends, search analytics, AI-assisted insights, visualisation, and reporting.

## Longer-Term Exploration

The following ideas are intentionally exploratory rather than committed milestones:

- advanced AI experiences, such as a personal AI bartender, generated recipes, voice interaction, image generation, event or menu planning, seasonal recommendations, and ingredient inventory assistance
- mobile and progressive web applications
- barcode scanning and OCR for cocktail books
- RAG-powered cocktail knowledge and agentic AI workflows
- smart shopping lists, social sharing, community recipes, and a public API

These ideas should be assessed against user value, engineering complexity, data requirements, cost, privacy, and operational readiness before becoming planned work.

## Engineering Direction

Across all milestones, the project aims to demonstrate clean, maintainable architecture; AWS best practices; thoughtful AI integration; automated testing; clear documentation; and continuous improvement. Detailed implementation tasks belong in issue tracking or milestone plans, not in this roadmap.

See [AWS architecture](architecture/aws.md), [deployment](architecture/deployment.md), and [AGENTS.md](../AGENTS.md) for related guidance.
