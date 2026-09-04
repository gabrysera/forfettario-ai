# Architecture

## Goal

Keep the fiscal core deterministic, testable and independent from model/provider behavior.

## Proposed modules

```text
apps/web
packages/ui
packages/ai
packages/tax-engine
packages/documents
packages/database
rules/italy/<year>
```

## Boundaries

### `packages/ai`
Responsible for conversation, structured extraction, tool selection and explanation of engine outputs. It must not define fiscal constants or authoritative formulas.

### `packages/tax-engine`
Pure/domain-oriented code for eligibility, taxable-base calculation, contribution estimates, tax estimates, deadline applicability and review-state decisions. Must not depend on a specific LLM.

### `packages/documents`
Internal form schemas, mapping and rendering. Document generation must be deterministic from validated structured data.

### `rules/italy/<year>`
Versioned configuration/constants and source metadata for legally time-dependent rules.

## Suggested request flow

```text
UI
 -> AI extracts candidate facts
 -> schema validation
 -> deterministic eligibility/tool call
 -> persisted domain state
 -> deterministic calculation/document mapping
 -> AI explains result
```

## Event/audit model

Consequential state changes should append audit events rather than only mutating opaque current state.

Examples: profile fact confirmed; classification confirmed; invoice issued; payment recorded; calculation produced; document generated; user acknowledged review warning.

## Deployment

Keep v0 simple: one Next.js application, managed PostgreSQL, private object storage, managed LLM API and GitHub Actions. No microservices or Kubernetes until there is a demonstrated need.
