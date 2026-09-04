# Start here

The repository is implementation-ready only when the current P0 fiscal questions are resolved and encoded as requirements/tests. Infrastructure and scaffolding can progress in parallel as long as they do not invent fiscal behavior.

## 1. Lock the first supported taxpayer archetype

Proposed v0.1 archetype:

- natural person;
- Italian tax resident;
- freelance software developer;
- ATECO 2025 62.10.00;
- regime forfettario candidate;
- Gestione Separata, no other mandatory pension coverage;
- no employees/collaborators;
- no participation/control situations that create exclusion issues;
- no complex foreign tax situation.

Anything else must initially escalate to review.

## 2. Complete the opening workflow research

Before implementing AA9/12 generation, resolve every P0 item in `docs/RESEARCH_BACKLOG.md`, then convert answers into:

- explicit FR requirements;
- deterministic validation rules;
- source registry entries;
- boundary tests;
- `MT-001` acceptance-test updates.

## 3. Define v0.1 data contracts

Create Pydantic v2 schemas for:

- `TaxpayerProfile`;
- `ActivityClassification`;
- `TaxRegimeAssessment`;
- `SocialSecurityAssessment`;
- `ReviewStatus`;
- `AA912Draft`;
- `SourceReference`;
- storage-facing entities/events needed by the first vertical slice.

## 4. Follow the fixed v0 architecture

The initial architecture is intentionally small:

```text
FastAPI + Jinja2 + HTMX
         │
Azure Functions Flex Consumption
         │
         ├── Azure Table Storage
         └── Azure Blob Storage
```

No SQL database in v0. No SPA. No Node build chain. No microservices.

Read `docs/ARCHITECTURE.md`, `docs/STORAGE_MODEL.md` and `docs/DEPLOYMENT.md` before adding infrastructure or persistence code.

## 5. Recommended implementation order

1. bootstrap Python project (`pyproject.toml`, lint/typecheck/test tooling);
2. create portable FastAPI app and Azure Functions ASGI adapter;
3. implement Pydantic domain schemas;
4. implement storage interfaces plus in-memory fakes;
5. implement Azure Table/Blob adapters;
6. add Bicep dev infrastructure;
7. implement deterministic eligibility engine;
8. add synthetic golden fixtures;
9. implement server-rendered onboarding UI;
10. add AI extraction behind structured schemas;
11. implement AA9/12 internal mapping;
12. run Playwright/manual acceptance tests against deployed dev environment.

## 6. Definition of done for v0.1

The first milestone is complete only when a synthetic supported user can go from empty account to a reviewable AA9/12 draft and the exact same fiscal result can be reproduced without using an LLM.

The LLM may improve the interaction, but removing the LLM must not change fiscal truth.
