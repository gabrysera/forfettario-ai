# ADR-003 — Storage-first serverless Azure v0

## Status
Accepted.

## Context

The first version is expected to have very low and sporadic traffic. The product should be inexpensive to run, easy for coding agents to reason about and simple to recreate from infrastructure as code.

A managed relational database would add a continuously provisioned component and more operational surface than the current access patterns require.

## Decision

For v0:

- host the Python web application on Azure Functions Flex Consumption;
- keep FastAPI as the portable ASGI application;
- use Azure Table Storage as the structured datastore;
- use Azure Blob Storage for generated/binary documents;
- use Bicep for Azure infrastructure;
- use GitHub Actions for CI/CD;
- do not provision PostgreSQL or another SQL database.

The storage model is explicitly designed around known user-scoped access patterns and append-only audit events.

## Consequences

### Positive

- very low idle compute cost;
- no database server lifecycle;
- tiny Azure resource footprint;
- simple backup/durability model delegated to managed storage;
- architecture stays understandable for AI coding agents;
- same Storage Account can serve Functions runtime and v0 application persistence where acceptable;
- easy future introduction of queues if asynchronous work becomes necessary.

### Negative

- no joins or arbitrary SQL queries;
- secondary lookup patterns require explicit denormalization/index entities;
- cross-partition/cross-table atomic transactions are unavailable;
- schema evolution must be handled at application level;
- complex reporting may later justify a different read model or database.

## Guardrails

- no whole-table scans in normal product workflows;
- no PII in partition/row keys when an opaque ID is sufficient;
- domain modules do not import Azure SDKs;
- storage access occurs through interfaces;
- consequential fiscal history remains auditable;
- replacing Table Storage requires a new ADR and migration plan.

## Revisit when

Re-evaluate this decision if any of the following becomes true:

- cross-user reporting becomes a core feature;
- relational consistency across multiple aggregates becomes necessary;
- access patterns cannot be served efficiently without excessive denormalization;
- storage transaction limitations create correctness risk;
- product scale/cost data demonstrates another datastore is materially better.
