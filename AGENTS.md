# AGENTS.md

This file is authoritative for AI coding agents working in this repository.

## Product invariants

1. **Never implement fiscal rules inside UI components or prompts.**
2. **Never use an LLM to perform authoritative tax arithmetic.**
3. **Never silently infer missing fiscal facts.** Missing material information must produce an explicit question or `NEEDS_REVIEW`.
4. **Fail closed.** Unsupported or ambiguous situations must not be forced through the happy path.
5. **Every fiscal rule must be versioned by jurisdiction and applicable period.**
6. **Every fiscal rule must cite a primary or authoritative source.**
7. **Every fiscal rule change must add/update automated tests.**
8. **Every user-visible workflow change must update the corresponding manual test.**
9. **Never mix issued invoices with collected income.** The domain must separately represent documents, payments and tax-relevant cash events.
10. **No user-facing number may be presented as final/authoritative unless the engine can explain how it was derived.**

## v0 architecture invariants

1. Python-first modular monolith.
2. FastAPI application must remain runnable outside Azure Functions.
3. Azure Functions code is a thin hosting adapter only.
4. Azure Table Storage is the v0 structured datastore.
5. Azure Blob Storage is the v0 binary/document store.
6. No PostgreSQL, SQLAlchemy, Alembic, Redis, Kubernetes, VM, microservices or Node frontend build pipeline in v0 unless an ADR explicitly replaces this architecture.
7. Domain and tax-engine modules must not import Azure SDK types.
8. Persistence must be accessed through storage interfaces/ports.
9. Storage keys and denormalized records must be designed from documented access patterns in `docs/STORAGE_MODEL.md`.
10. Do not emulate relational joins by scanning entire Azure tables.
11. Consequential fiscal operations require append-only audit events.
12. Current-state snapshots may be updated for efficient reads but never replace the audit trail.
13. Prefer one user-scoped partition for transactional user data unless a documented access/scale reason requires another partition strategy.
14. Do not place sensitive personal data in logs, PartitionKeys, RowKeys, blob paths or telemetry dimensions when an opaque identifier can be used instead.
15. The application must work against in-memory storage fakes in unit/domain tests.

## Required change discipline

Before implementing a feature:

- read `docs/PRODUCT.md`;
- read `docs/FUNCTIONAL_REQUIREMENTS.md`;
- read `docs/ARCHITECTURE.md`;
- read `docs/STORAGE_MODEL.md` if persistence is involved;
- read relevant files in `rules/`;
- read relevant manual tests;
- identify whether the change affects a fiscal invariant.

A PR that changes behavior must update, where applicable:

- `docs/FUNCTIONAL_REQUIREMENTS.md`;
- `docs/DOMAIN_MODEL.md`;
- `docs/STORAGE_MODEL.md`;
- one or more `docs/manual-tests/*.md`;
- deterministic tests;
- `rules/.../sources.md` if fiscal logic changed;
- an ADR if an architectural boundary changed.

## AI boundary

Allowed LLM responsibilities:

- conversational onboarding;
- extracting structured facts from user text/documents;
- explaining deterministic engine outputs;
- classifying whether a workflow/tool should be invoked;
- identifying missing information;
- summarizing authoritative sources already provided to the system.

Disallowed LLM responsibilities:

- deciding tax rates from memory;
- computing taxes instead of calling the engine;
- inventing deadlines, codes, thresholds or form values;
- deciding an ambiguous legal/fiscal classification without deterministic validation;
- claiming a filing/payment was completed when it was not.

## Review states

Use this conceptual contract consistently:

```python
class ReviewStatus(str, Enum):
    AUTO_VALIDATED = "AUTO_VALIDATED"
    USER_CONFIRMATION_REQUIRED = "USER_CONFIRMATION_REQUIRED"
    PROFESSIONAL_REVIEW_REQUIRED = "PROFESSIONAL_REVIEW_REQUIRED"
    UNSUPPORTED = "UNSUPPORTED"
```

## Testing

Prefer pure functions for fiscal calculations.

Minimum for a rule change:

- unit test for the rule;
- boundary tests around thresholds/dates;
- at least one golden fixture if end-user output changes;
- manual test update if the UI/workflow changes.

Persistence tests should normally use in-memory fakes. Azure adapter integration tests may use Azurite or an isolated Azure test environment, but domain tests must never require Azure.

Never weaken or delete a failing fiscal test merely to make CI green unless the requirement/source changed and the PR documents why.

## Security and privacy

Assume all tax profiles, invoices, fiscal codes, addresses and financial information are sensitive.

- no secrets in source control;
- no production personal data in fixtures;
- fixtures must use synthetic identities;
- redact logs by default;
- minimize data sent to LLM providers;
- do not send unnecessary identity fields to the model;
- prefer managed identity for Azure access;
- do not expose storage account keys to browser code;
- generated document blobs must not be public by default.
