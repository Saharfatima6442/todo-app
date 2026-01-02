<!--
Sync Impact Report:
Version change: N/A -> 1.0.0
Modified principles: N/A
Added sections: All principles and sections as specified
Removed sections: N/A
Templates requiring updates:
- ✅ .specify/templates/plan-template.md - needs alignment
- ✅ .specify/templates/spec-template.md - needs alignment
- ✅ .specify/templates/tasks-template.md - needs alignment
- ⚠ .specify/templates/commands/*.md - needs review for outdated references
- ⚠ README.md - needs update for principles reference
Follow-up TODOs:
- TODO(RATIFICATION_DATE): Original adoption date unknown - needs to be set
- TODO: Update dependent templates to align with new principles
-->
# Todo In-Memory Console Application Constitution

## Core Principles

### Clean Code First
Every feature must follow clean code principles with clear separation of concerns between CLI, business logic, and data models; Code must be modular, readable, and maintainable with proper abstractions.

### Spec-Driven Development
All development must strictly follow approved specifications; Specifications must be saved in the specs_history folder; Claude Code must be used to generate and evolve specifications.

### Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced for all features.

### In-Memory Architecture
All data must be stored in memory during runtime; No file handling, databases, or external storage allowed; Focus on core functionality without persistence concerns.

### Console-First Interface
Every functionality must be accessible via CLI; Menu-driven interface required; Text-based input/output protocol for all interactions.

### Python 3.13+ Standards
Use Python 3.13 or higher with UV for environment management; Follow modern Python coding standards and best practices.

## Technology Stack Requirements

Python 3.13+, UV for environment management, Claude Code, Spec-Kit Plus; No third-party task management libraries; Console-only interface without GUI.

## Development Workflow

Spec-driven development using Spec-Kit Plus; Code must strictly follow approved specifications; All specifications must be saved in specs_history folder.

## Governance

Constitution supersedes all other practices; Amendments require documentation and approval; All development must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-31
