# forfettario-ai

> Open-source, AI-native tax copilot for simple Italian **regime forfettario** freelancers, starting with software developers.

**Status:** pre-alpha / requirements-first.

The project starts deliberately narrow: Italian resident natural persons working as freelance software developers, initially targeting ATECO 2025 `62.10.00` (software programming activities), with simple cases suitable for the regime forfettario.

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

AI is used for conversation, extraction, explanation, anomaly detection and tool orchestration. Tax calculations, validation, deadlines, document fields and eligibility rules live in deterministic, versioned code with sources and tests.

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

## Repository map

- `AGENTS.md` — mandatory rules for coding agents.
- `docs/PRODUCT.md` — product boundaries and target user.
- `docs/FUNCTIONAL_REQUIREMENTS.md` — canonical functional requirements.
- `docs/DOMAIN_MODEL.md` — domain entities and terminology.
- `docs/ARCHITECTURE.md` — technical boundaries.
- `docs/RESEARCH_BACKLOG.md` — unresolved fiscal/legal questions.
- `docs/manual-tests/` — executable-by-agent acceptance scenarios.
- `rules/italy/<year>/` — year-versioned fiscal rules and primary sources.
- `tests/golden/` — end-to-end fiscal fixtures.

## Development philosophy

1. Requirements before implementation.
2. Every fiscal rule has a source, applicable period and automated tests.
3. Manual acceptance tests are updated in the same PR as behavior changes.
4. Unsupported cases fail closed into review instead of guessing.
5. No production use until the relevant rules have been independently reviewed.

## Stack

Keep v0 deliberately boring and Python-first:

- Python 3.13+
- FastAPI
- Jinja2 server-rendered templates
- HTMX for small interactive updates
- minimal vanilla CSS (no frontend build system initially)
- PostgreSQL
- SQLAlchemy 2 + Alembic
- Pydantic 2
- pytest
- Playwright for Python
- GitHub Actions
- OpenAI API for orchestration/extraction/explanations

There is intentionally **no React/Next.js SPA and no Node build step** in the initial architecture. The browser receives HTML from the same Python application.

## First milestone

`onboarding → eligibility → structured tax profile → AA9/12 preparation → human review/export`

See `docs/FUNCTIONAL_REQUIREMENTS.md` and `docs/manual-tests/open-vat.md`.

## Safety / legal status

This project is experimental software, not a licensed professional. Outputs that can create legal or tax consequences must be reviewable, traceable to sources and clearly distinguish estimates from authoritative amounts.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). AI-assisted contributions are welcome, but contributors remain responsible for the correctness of their changes.

## License

MIT. See [LICENSE](LICENSE).
