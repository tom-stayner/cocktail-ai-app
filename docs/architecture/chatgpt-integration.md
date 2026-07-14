# AI-Assisted Engineering

## Purpose

This document describes how AI coding assistance supports engineering work in this repository. It complements, but does not replace, human ownership of product and architectural decisions.

## Governance

[AGENTS.md](../../AGENTS.md) is the repository's Engineering Constitution and the source of truth for engineering principles, delivery workflow, documentation rules, and approval requirements.

The developer retains responsibility for product direction, AWS infrastructure, and final approval of architectural and repository changes.

## Working Model

For significant work, AI assistance should:

1. Review the relevant implementation and documentation.
2. Identify affected code, tests, configuration, and documentation.
3. Propose a plan and obtain approval for architectural or structural changes.
4. Implement the approved work and verify it.
5. Summarise the result, including material decisions and verification.

Significant engineering decisions belong in the [engineering log](engineering-log.md). Current architecture and future direction belong in the relevant architecture documents.

## Repository and GitHub

The repository is the source of truth for source code, documentation, roadmap, and recorded engineering decisions. Pull requests and GitHub automation may be adopted as the delivery workflow evolves; their use should be documented once implemented and verified.

## Future Direction

Potential future improvements include a repeatable pull-request workflow, automated checks, and lessons learned from AI-assisted development. These should be added only after they are demonstrated in this repository.
