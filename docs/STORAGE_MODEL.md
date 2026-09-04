# Storage model

## Purpose

Define the v0 persistence model for Azure Table Storage and Blob Storage.

The design must optimize for the application's actual access patterns, not for relational normalization.

## Principles

1. Use opaque internal `user_id` values as partition identifiers.
2. Never put fiscal codes, email addresses, names or other PII into `PartitionKey`, `RowKey` or blob names when avoidable.
3. Keep user-scoped operational records in the same partition where practical.
4. Use append-only audit events for consequential fiscal actions.
5. Maintain current-state snapshots only as read optimizations.
6. Never rely on whole-table scans for normal application workflows.
7. Do not model cross-user joins.
8. Every stored entity must have an explicit schema version.

## Core access patterns

The v0 app needs to efficiently answer:

- load one user's current profile;
- load one user's current activity/tax-regime assessment;
- list invoices for one user/year;
- load one invoice;
- list payments for one user/year;
- load tax calculations for one user/year;
- load the latest calculation;
- load AA9/12 drafts and generated document metadata;
- append/read the audit history for one user;
- recover current state without querying other users.

If a new feature requires a materially different query, update this document before implementing persistence.

## Tables

Prefer a small number of Azure Tables rather than one table per domain type.

### `UserState`

Current-state/read-optimized entities.

`PartitionKey = <opaque user_id>`

Recommended RowKey prefixes:

```text
PROFILE
ACTIVITY#<activity_id>
ASSESSMENT#FORFETTARIO#<tax_year>
ASSESSMENT#SOCIAL_SECURITY#<tax_year>
INVOICE#<year>#<invoice_id>
PAYMENT#<year>#<payment_id>
TAX_SUMMARY#<year>
AA912#<draft_id>
DOCUMENT#<document_id>
```

Example:

```text
PartitionKey = 01J...
RowKey       = INVOICE#2026#01J...
```

### `AuditEvents`

Append-only domain/audit events.

`PartitionKey = <opaque user_id>`

`RowKey = <reverse-sortable or sortable timestamp>#<event_id>`

Example event types:

```text
TaxpayerFactConfirmed
ActivityClassificationConfirmed
EligibilityCalculated
InvoiceIssued
PaymentRecorded
TaxCalculationGenerated
AA912DraftGenerated
DocumentGenerated
ReviewWarningAcknowledged
```

Each event should contain at minimum:

- `event_type`;
- `schema_version`;
- UTC timestamp;
- opaque actor identifier/type;
- relevant aggregate/entity id;
- deterministic ruleset/version when applicable;
- sanitized event payload;
- correlation id when part of a workflow.

Events should be immutable after successful creation except where Azure technical metadata requires otherwise.

## Entity shape

All structured entities should include:

```text
schema_version
entity_type
created_at
updated_at (for mutable snapshots)
```

Fiscal outputs should additionally include where relevant:

```text
ruleset_version
tax_year
calculation_version
source_reference_ids
review_status
```

## Query design

Allowed normal query patterns:

- exact `PartitionKey` + exact `RowKey`;
- exact `PartitionKey` + RowKey prefix/range;
- exact `PartitionKey` + narrow property filtering when the volume remains bounded.

Avoid:

- full table scans;
- queries by PII;
- filters that require all users to be inspected;
- application-level joins across large result sets.

If a secondary lookup becomes necessary, create an explicit denormalized/index entity whose consistency behavior is documented and tested.

## Transaction boundaries

When multiple writes must succeed atomically, keep them in the same table and same partition whenever feasible so they can use an Azure Table transactional batch.

Do not assume cross-partition or cross-table transactions.

For workflows spanning Table and Blob Storage:

1. write/generate blob with an opaque temporary/final path;
2. persist deterministic metadata/state;
3. append audit event;
4. make retries idempotent;
5. define cleanup behavior for orphaned blobs.

## Blob Storage

Container names (provisional):

```text
documents
exports
```

Blob path convention:

```text
<opaque_user_id>/<document_type>/<year>/<opaque_document_id>.<ext>
```

Examples:

```text
01J.../aa912/2026/01J....pdf
01J.../invoice/2026/01J....pdf
```

Blob names must not contain taxpayer names, fiscal codes, client names or invoice descriptions.

Private access only by default. Generate short-lived access only through authenticated server-side flows when required.

## Concurrency and idempotency

Use Azure entity ETags for optimistic concurrency on mutable snapshots.

Every externally retried command that can create consequential data should use an idempotency/correlation identifier.

Examples:

- recording a payment;
- generating an invoice;
- generating an AA9/12 draft;
- recalculating tax results after a user confirmation.

## Local development

Domain/application code talks to storage ports.

Implementations:

```text
InMemoryUserStateRepository
InMemoryAuditRepository
InMemoryDocumentStore
AzureTableUserStateRepository
AzureTableAuditRepository
AzureBlobDocumentStore
```

Most tests use in-memory implementations.

Azure adapter tests may use Azurite or a dedicated Azure test environment.

## Migration/versioning strategy

Table Storage is schemaless, but the application is not.

- every entity carries `schema_version`;
- readers must explicitly support known versions;
- migrations are deterministic scripts/jobs checked into the repository;
- do not silently reinterpret old fiscal data under new rules;
- tax calculations retain the ruleset/calculation version that produced them.

## Security

- use managed identity in Azure where possible;
- never expose storage credentials to the browser;
- no public blob containers;
- redact storage identifiers from logs when they could help correlate sensitive data;
- encrypt in transit and rely on Azure Storage encryption at rest;
- define retention/deletion behavior before onboarding real production users.
