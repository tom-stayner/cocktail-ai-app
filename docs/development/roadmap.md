# Product Roadmap

## Vision

Cocktail AI App is intended to become a cloud-native, AI-powered cocktail companion. It is also a portfolio project demonstrating professional software engineering, AWS architecture, and practical AI integration.

The product will evolve incrementally. Each stage should preserve maintainability, testing, documentation, and production-quality engineering practices.

## Current Implementation — Core Platform

The current application provides a small, local FastAPI foundation with:

- JSON cocktail CRUD endpoints and server-rendered HTML views
- DynamoDB-backed cocktail records, including ingredient lists
- a service layer separating route handlers from CRUD logic
- a health endpoint, structured logging, regression tests, and local setup documentation

This phase establishes the engineering baseline; it is not yet a hosted, user-facing cloud platform. See the [architecture overview](architecture/overview.md) for the current system shape.

## Planned Milestones

### User Experience

Improve recipe discovery and usability through a modern, responsive interface. Likely capabilities include richer browsing, filtering and search, favourites, and a better mobile experience. A React frontend is a possible implementation direction, subject to the needs of the product at that stage.

### AI-Assisted Discovery

Introduce AI where it makes cocktail exploration more useful, rather than replacing conventional navigation. Potential capabilities include natural-language search, recommendations, ingredient substitutions, food-pairing suggestions, recipe explanations, and cocktail history or trivia.

### Accounts and Personalisation

Enable an individual experience with authentication, profiles, saved recipes and collections, preferences, and recently viewed cocktails. Amazon Cognito is the current anticipated authentication service, subject to architectural review when this milestone is started.

### Cloud Platform

Evolve the local application into a production-quality AWS deployment while retaining the benefits of the current service boundaries. The likely direction is a serverless platform using services such as API Gateway, Lambda, DynamoDB, Cognito, CloudFront, S3, CloudWatch, and CI/CD automation. Service selection and deployment topology will be decided through implementation-time architecture work.

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
