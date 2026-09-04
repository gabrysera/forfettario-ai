# Architecture

## Goal

Keep the fiscal core deterministic, testable and independent from model/provider behavior while keeping deployment and operating cost extremely small.

## Architecture choice

Start as a **modular Python monolith** hosted serverlessly on Azure Functions Flex Consumption.

```text
browser
  │ HTML / HTMX
  ▼
Azure Functions
  │ ASGI adapter
  ▼
FastAPI application
  ├── web routes + Jinja templates
  ├── ai orchestration
  ├── tax engine
  ├── document engine
  ├── ledger/application services
  └── storage ports
          │
          ├── Azure Table Storage
          └── Azure Blob Storage
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
  storage/
    ports.py
    azure_tables.py
    azure_blobs.py
azure_functions/
  function_app.py
rules/
  italy/
    <year>/
infra/
  azure/
tests/
  unit/
  integration/
  e2e/
  golden/
```

## Hosting boundary

`app/` must not depend on Azure Functions runtime objects. The Azure entrypoint adapts HTTP requests into the FastAPI ASGI application.

This keeps the application runnable locally and portable to another ASGI host if needed.

## Frontend

Use server-rendered Jinja2 HTML.

Use HTMX only where partial page updates materially improve the UX, for example:

- conversational onboarding;
- inline validation;
- adding/removing invoice rows;
- recalculating estimates;
- status panels.

Prefer ordinary HTML forms and links when sufficient. Avoid an SPA, React state management, a separate frontend API contract and a Node build chain until the product proves it needs them.

Initial styling should use a small local CSS layer.

## Python modules

### `app/ai`
Responsible for conversation, structured extraction, tool selection and explanation of engine outputs. It must not define fiscal constants or authoritative formulas.

### `app/tax_engine`
Pure/domain-oriented Python for eligibility, taxable-base calculation, contribution estimates, tax estimates, deadline applicability and review-state decisions. It must not depend on FastAPI, Azure SDKs or a specific LLM.

### `app/documents`
Internal form schemas, mapping and rendering. Document generation must be deterministic from validated structured data.

### `app/domain`
Pydantic domain models, enums, result types and application invariants shared across modules.

### `app/storage`
Storage interfaces and Azure adapters. Domain code must depend on interfaces, not Azure SDK types.

### `rules/italy/<year>`
Versioned configuration/constants and source metadata for legally time-dependent rules.

## Persistence

v0 uses Azure Storage only.

### Azure Table Storage
Stores structured entities and append-only audit events. Access patterns are user-scoped and designed around `PartitionKey` / `RowKey`.

### Azure Blob Storage
Stores generated/binary artifacts such as PDFs, exported packets and source documents when needed.

See `docs/STORAGE_MODEL.md` for concrete entity/access-pattern rules.

## Suggested request flow

```text
HTML request
 -> Azure Functions ASGI adapter
 -> FastAPI route
 -> optional AI extraction of candidate facts
 -> Pydantic validation
 -> deterministic eligibility/tool call
 -> storage port
 -> deterministic calculation/document mapping
 -> optional AI explanation
 -> Jinja HTML response / HTMX fragment
```

## Event/audit model

Consequential state changes should append audit events instead of only mutating opaque current state.

Examples: profile fact confirmed; classification confirmed; invoice issued; payment recorded; calculation produced; document generated; user acknowledged review warning.

Current-state snapshots may exist for efficient reads, but they must not erase the audit trail.

## Test stack

- `pytest` for unit and integration tests;
- deterministic golden fixtures for fiscal behavior;
- Python Playwright for browser acceptance tests;
- local/in-memory storage fakes for most tests;
- Azurite or an isolated Azure test account only for adapter integration tests;
- GitHub Actions for lint, type checking and tests.

## Deployment

Keep v0 minimal:

- Azure Functions Flex Consumption;
- one Azure Storage account for Functions runtime plus application Table/Blob storage unless isolation is later required;
- Application Insights for basic observability;
- Key Vault only when secrets/operational needs justify it, otherwise platform application settings with managed identity where possible;
- Bicep IaC;
- GitHub Actions.

No PostgreSQL, Redis, microservices, Kubernetes, VM, message broker or separate frontend deployment in v0.
