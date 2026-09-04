# forfettario-ai

> Open-source, AI-native tax copilot for simple Italian **regime forfettario** freelancers, starting with software developers.

**Status:** pre-alpha / requirements-first.

The project starts deliberately narrow: Italian resident natural persons working as freelance software developers, initially targeting ATECO 2025 `62.10.00`, with simple cases suitable for the regime forfettario.

## Product idea

The user should be able to:

1. describe their situation in plain language;
2. receive a structured eligibility assessment;
3. generate the data/document package needed to open a VAT position;
4. create and track invoices and collections;
5. always see estimated tax/social-security reserves and upcoming obligations;
6. receive clear explanations and escalation when the case is outside the supported scope.

## Core principle

**LLMs never decide fiscal arithmetic or authoritative rules.**

AI is used for conversation, extraction, explanation, anomaly detection and tool orchestration. Tax calculations, validation, deadlines, document fields and eligibility rules live in deterministic, versioned Python code with sources and tests.

```text
user
  │
  ▼
AI orchestration layer
  │ structured tool calls
  ├───────────────┬────────────────┐
  ▼               ▼                ▼
Tax engine     Document engine    Ledger
(deterministic) (deterministic)   (deterministic)
```

## Initial scope

Supported first:

- Italy;
- natural person / freelancer;
- regime forfettario;
- software development / ATECO 62.10.00;
- simple Gestione Separata cases;
- opening workflow;
- invoices and collections;
- tax and contribution estimates;
- explicit `NEEDS_REVIEW` for unsupported/ambiguous cases.

Not initially supported:

- companies;
- ordinary VAT regime;
- artisans / merchants;
- professional pension funds;
- multiple complex activities;
- crypto, property or complex foreign income;
- generic tax advice for arbitrary cases;
- autonomous filing on behalf of the taxpayer.

## v0 architecture

The initial deployment is intentionally tiny and serverless:

```text
Browser
   │ HTML / HTMX
   ▼
Azure Functions — Flex Consumption
   │
   ├── FastAPI + Jinja2
   ├── deterministic tax/document code
   ├── AI orchestration
   │
   ├── Azure Table Storage  ← structured application data
   └── Azure Blob Storage   ← PDFs / generated documents

OpenAI API                 ← only where AI is useful
Application Insights       ← basic observability
GitHub Actions + Bicep     ← CI/CD + IaC
```

The Function app is only a hosting adapter. Core domain and fiscal code must remain ordinary Python and runnable locally without Azure.

## Data philosophy

v0 intentionally does **not** use PostgreSQL or another database server.

Azure Table Storage is the primary structured datastore. Data is designed around access patterns instead of SQL joins, with user-scoped partitions and append-only audit events where fiscal traceability matters.

Blob Storage stores binary/generated artifacts such as AA9/12 drafts and invoice PDFs.

See `docs/STORAGE_MODEL.md` before adding persistence code.

## Repository map

- `AGENTS.md` — mandatory rules for coding agents.
- `START_HERE.md` — implementation order.
- `docs/PRODUCT.md` — product boundaries and target user.
- `docs/FUNCTIONAL_REQUIREMENTS.md` — canonical functional requirements.
- `docs/DOMAIN_MODEL.md` — domain entities and terminology.
- `docs/ARCHITECTURE.md` — application/deployment boundaries.
- `docs/STORAGE_MODEL.md` — Azure Table/Blob data model and access patterns.
- `docs/DEPLOYMENT.md` — Azure Functions + IaC deployment model.
- `docs/RESEARCH_BACKLOG.md` — unresolved fiscal/legal questions.
- `docs/decisions/` — architectural decision records.
- `docs/manual-tests/` — executable-by-agent acceptance scenarios.
- `rules/italy/<year>/` — year-versioned fiscal rules and primary sources.
- `tests/golden/` — end-to-end fiscal fixtures.
- `infra/azure/` — Bicep infrastructure definitions.

## Stack

Keep v0 deliberately boring and Python-first:

- Python 3.13+
- FastAPI
- Azure Functions v4 / Flex Consumption
- Jinja2 server-rendered templates
- HTMX for targeted interactivity
- minimal vanilla CSS
- Pydantic 2
- Azure Data Tables SDK
- Azure Blob Storage SDK
- pytest
- Playwright for Python
- GitHub Actions
- Bicep
- OpenAI API for orchestration/extraction/explanations

There is intentionally:

- no React/Next.js SPA;
- no Node build pipeline;
- no PostgreSQL in v0;
- no Redis;
- no Kubernetes;
- no VM;
- no microservices.

## Development philosophy

1. Requirements before implementation.
2. Every fiscal rule has a source, applicable period and automated tests.
3. Manual acceptance tests are updated in the same PR as behavior changes.
4. Unsupported cases fail closed into review instead of guessing.
5. Storage design follows documented access patterns; do not recreate SQL-style joins in application code.
6. Consequential fiscal state must be auditable.
7. Azure-specific code stays at infrastructure/adaptor boundaries.
8. No production use until the relevant rules have been independently reviewed.

## First milestone

`onboarding → eligibility → structured tax profile → AA9/12 preparation → human review/export`

See `docs/FUNCTIONAL_REQUIREMENTS.md` and `docs/manual-tests/open-vat.md`.

## Safety / legal status

This project is experimental software, not a licensed professional. Outputs that can create legal or tax consequences must be reviewable, traceable to sources and clearly distinguish estimates from authoritative amounts.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). AI-assisted contributions are welcome, but contributors remain responsible for the correctness of their changes.

## License

MIT. See [LICENSE](LICENSE).
