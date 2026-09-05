# Architecture

## Goal

Keep the fiscal core deterministic, testable and independent from model/provider/cloud behavior while keeping the codebase and operating cost extremely small.

## Architecture choice

Start as a **modular Python monolith** hosted serverlessly on Azure Functions Flex Consumption.

```text
browser
  │ HTML / HTMX
  ▼
Azure Functions
  │ thin ASGI adapter (`function_app.py`)
  ▼
FastAPI application
  ├── web / presentation
  ├── AI orchestration
  ├── deterministic tax engine
  ├── deterministic document engine
  └── storage ports + adapters
          │
          ├── Azure Table Storage
          └── Azure Blob Storage
```

Do not split these modules into deployable services in v0.

## Patterns we deliberately use

Use patterns only where they make the code smaller, safer or easier to test.

### Functional core, imperative shell

Fiscal decisions, calculations, document mappings and validation are deterministic functions over typed inputs. HTTP, Azure, storage and LLM calls stay at the edges.

This is the primary design pattern of the application.

### Ports and adapters at real external boundaries

Use small `Protocol` ports for infrastructure that has more than one meaningful implementation, such as persistence. In-memory fakes and Azure adapters implement the same observable contract.

Do not introduce ports for ordinary internal function calls.

### Adapter exception translation

Provider-specific exceptions are caught inside adapters and translated into small application-owned errors when callers need consistent behavior. Application/domain code should never branch on Azure/OpenAI SDK exception classes.

### Append-only audit log + current snapshots

Consequential fiscal history is append-only. Mutable current-state entities exist only as read optimizations. This is intentionally **not** a full event-sourcing framework.

Generated fiscal documents are immutable/versioned artifacts. Regeneration creates a new document id instead of overwriting an existing blob.

### Versioned rule modules

Fiscal rules are grouped by applicable period and backed by stable source IDs. Do not introduce a Strategy class hierarchy while a small year-specific module/pure function is sufficient.

### Template profile for coordinate-based fiscal documents

When a document such as AA9/12 is rendered onto an official PDF, layout coordinates belong to an explicitly versioned/fingerprinted template profile. Mapping decides *what* to write; layout decides *where*; renderer only performs deterministic drawing.

## Patterns we deliberately avoid in v0

Unless a concrete requirement proves otherwise, do not add:

- dependency-injection containers;
- generic repository frameworks or ORM-like abstractions;
- Unit of Work;
- CQRS infrastructure;
- event-sourcing frameworks;
- mediator/command-bus libraries;
- service/factory classes that only forward calls;
- abstract base classes where a function or `Protocol` is enough.

## Repository layout

```text
app/
  main.py
  domain/
  tax_engine/
  documents/
  storage/
    ports.py
    memory.py
    azure.py
  ai/
  web/
    templates/
    static/          # only when needed

function_app.py      # Azure Functions hosting adapter
host.json

rules/
  italy/
    <year>/

infra/
  azure/

tests/
  architecture/
  golden/
  # unit/integration/e2e folders are added when enough tests exist to justify them
```

Do not create empty architectural layers merely to match this diagram. A directory exists when it owns real code or tests.

## Dependency direction

The dependency graph is intentionally one-way.

```text
                         ┌──────────────┐
                         │  app/domain  │
                         └──────▲───────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
         ┌───────┴──────┐ ┌─────┴──────┐ ┌────┴─────────┐
         │ tax_engine   │ │ documents  │ │ storage ports │
         └──────▲───────┘ └─────▲──────┘ └────▲──────────┘
                │               │              │
                └───────────────┼──────────────┘
                                │
                     ┌──────────┴──────────┐
                     │ AI / web / adapters │
                     └─────────────────────┘
```

The diagram shows **allowed direction**, not a requirement that every module import every lower module.

### Hard rules

`app/domain` is the lowest stable layer. It must not import:

- FastAPI;
- Azure SDKs;
- OpenAI/provider SDKs;
- `app.web`, `app.ai`, `app.storage`, `app.documents` or `app.tax_engine`.

`app/tax_engine` may depend on standard-library/domain contracts, but must not import:

- FastAPI;
- Azure SDKs;
- OpenAI/provider SDKs;
- `app.web`, `app.ai`, `app.storage` or `app.documents`.

`app/documents` owns deterministic document schemas/mapping/rendering. It must not depend on web, AI, storage, tax-engine or cloud SDKs. Any orchestration between fiscal assessment and document generation belongs at the application edge, not inside the renderer/document module.

`app/storage` owns persistence boundaries. Azure types stay inside the Azure adapter and never leak into domain/tax-engine signatures. Provider errors are translated at this boundary when their semantics are part of the port contract.

`app/ai` may orchestrate deterministic tools but must never become the source of fiscal truth.

`app/web` is presentation glue. It may call lower modules but contains no fiscal rules.

These core restrictions are enforced by `tests/architecture/test_import_boundaries.py` using Python's standard-library AST parser. The test is intentionally tiny: architecture should be protected without adding an architecture framework.

## Hosting boundary

The FastAPI application must remain runnable without Azure Functions. `function_app.py` is only an adapter from the Azure Functions runtime to the ASGI app.

This keeps local development simple and preserves portability to another ASGI/serverless host.

## Frontend

Use server-rendered Jinja2 HTML.

Use HTMX only where partial page updates materially improve UX, for example conversational onboarding, inline validation and recalculated summaries. Prefer ordinary forms and links when they are enough.

No SPA, React state management, separate frontend API contract or Node build chain in v0.

## Module responsibilities

### `app/domain`
Stable domain models, enums and invariants. No infrastructure or framework concepts.

### `app/tax_engine`
Pure deterministic fiscal assessments/calculations. Rules are versioned and source-backed. Removing Azure, FastAPI and the LLM must not affect results.

### `app/documents`
Typed fiscal-document contracts plus deterministic mapping/rendering. Renderers receive validated data and contain zero fiscal decision logic.

### `app/storage`
Small storage ports plus in-memory/Azure implementations. Do not recreate an ORM over Table Storage.

### `app/ai`
Conversation, structured extraction, tool selection and explanation. It can propose facts; deterministic code validates consequential facts/results.

### `app/web`
HTTP routes/templates/presentation. Keep route handlers thin, but do not create a service layer until orchestration complexity genuinely warrants one.

### `rules/italy/<year>`
Human-reviewable fiscal specifications, stable source IDs and legally time-dependent rules/configuration.

## Persistence

v0 uses Azure Storage only.

### Azure Table Storage
Stores structured entities and append-only audit events. Access patterns are user-scoped and designed around `PartitionKey` / `RowKey`.

### Azure Blob Storage
Stores immutable generated/binary artifacts such as PDFs and export packets.

See `docs/STORAGE_MODEL.md`.

## Request flow

```text
HTML request
 -> Azure Functions ASGI adapter
 -> FastAPI route
 -> optional AI extraction of candidate facts
 -> typed validation
 -> deterministic tax/document operation
 -> storage port when state is required
 -> optional AI explanation
 -> Jinja HTML / HTMX fragment
```

## Event/audit model

Consequential state changes append audit events rather than only mutating opaque current state. Current-state snapshots may exist for efficient reads but must not erase the audit trail.

## Test stack

- `pytest` for deterministic tests;
- golden fixtures for fiscal behavior;
- architecture boundary test for forbidden dependencies;
- Python Playwright for browser acceptance tests when UI workflows exist;
- in-memory storage fakes for normal tests;
- Azurite/isolated Azure only for adapter integration tests;
- GitHub Actions for dependency consistency, Ruff, mypy and pytest.

## Deployment

Keep v0 minimal:

- Azure Functions Flex Consumption;
- Azure Storage for runtime + Table/Blob application persistence unless later isolation is justified;
- Application Insights for basic observability;
- managed identity where practical;
- Bicep IaC;
- GitHub Actions.

No PostgreSQL, Redis, microservices, Kubernetes, VM, message broker or separate frontend deployment in v0.
