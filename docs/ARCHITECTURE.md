# Architecture

## Goal

Keep the fiscal core deterministic, testable and independent from model/provider behavior while keeping the product as simple as possible to develop and deploy.

## Architecture choice

Start as a **modular Python monolith**.

```text
browser
  │ HTML / HTMX
  ▼
FastAPI application
  ├── web routes + Jinja templates
  ├── ai orchestration
  ├── tax engine
  ├── document engine
  ├── ledger/application services
  └── persistence
          │
          ▼
      PostgreSQL
```

Do not split these modules into deployable services in v0.

## Proposed repository layout

```text
app/
  main.py
  web/
    routes/
    templates/
    static/
  domain/
  tax_engine/
  documents/
  ai/
  db/
rules/
  italy/
    <year>/
tests/
  unit/
  integration/
  e2e/
  golden/
```

## Frontend

Use server-rendered Jinja2 HTML.

Use HTMX only where partial page updates materially improve the UX, for example:

- conversational onboarding;
- inline validation;
- adding/removing invoice rows;
- recalculating estimates;
- status panels.

Prefer ordinary HTML forms and links when they are sufficient. Avoid an SPA, React state management, a separate frontend API contract and a Node build chain until the product proves it needs them.

Initial styling should use a small local CSS layer. A lightweight CSS library can be introduced later without changing the architecture.

## Python modules

### `app/ai`
Responsible for conversation, structured extraction, tool selection and explanation of engine outputs. It must not define fiscal constants or authoritative formulas.

### `app/tax_engine`
Pure/domain-oriented Python for eligibility, taxable-base calculation, contribution estimates, tax estimates, deadline applicability and review-state decisions. It must not depend on FastAPI, the database or a specific LLM.

### `app/documents`
Internal form schemas, mapping and rendering. Document generation must be deterministic from validated structured data.

### `app/domain`
Pydantic domain models, enums, result types and application invariants shared across modules.

### `app/db`
SQLAlchemy models, repositories and migrations. Database concerns must not leak into pure fiscal functions.

### `rules/italy/<year>`
Versioned configuration/constants and source metadata for legally time-dependent rules.

## Suggested request flow

```text
HTML request
 -> FastAPI route
 -> optional AI extraction of candidate facts
 -> Pydantic validation
 -> deterministic eligibility/tool call
 -> persisted domain state
 -> deterministic calculation/document mapping
 -> optional AI explanation
 -> Jinja HTML response / HTMX fragment
```

## Event/audit model

Consequential state changes should append audit events rather than only mutating opaque current state.

Examples: profile fact confirmed; classification confirmed; invoice issued; payment recorded; calculation produced; document generated; user acknowledged review warning.

## Test stack

- `pytest` for unit and integration tests;
- deterministic golden fixtures for fiscal behavior;
- Python Playwright for browser acceptance tests;
- GitHub Actions for lint, type checking and tests.

## Deployment

Keep v0 simple: one Python web application/container, managed PostgreSQL, private object storage when needed, managed LLM API and GitHub Actions.

No microservices, Kubernetes, message broker, separate frontend deployment or Node runtime until there is a demonstrated need.
