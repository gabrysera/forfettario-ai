# Deployment model

## Goal

Run the v0 application with near-zero idle compute cost, minimal operational overhead and reproducible infrastructure.

## Target architecture

```text
GitHub
  │
  ├── CI: lint / typecheck / pytest / browser checks
  │
  └── deploy
        ▼
Azure Functions — Flex Consumption
        │
        ├── Azure Storage account
        │     ├── Table Storage
        │     └── Blob Storage
        │
        ├── Application Insights
        └── managed identity / app settings
```

The FastAPI application remains ordinary ASGI Python. Azure Functions is a hosting adapter.

## Azure Functions

Use Azure Functions v4 with the Python programming model and Flex Consumption for new environments.

Requirements:

- HTTP-triggered entrypoint;
- ASGI adapter to the FastAPI app;
- scale-to-zero configuration by default;
- no Always Ready instances in v0 unless measured latency justifies the cost;
- health endpoint that does not expose sensitive details;
- timeouts/limits documented before adding long-running workflows.

Long-running work should not be hidden inside synchronous HTTP handlers. If future document/AI tasks exceed practical HTTP execution limits, add a queue-backed worker pattern only when needed and document it in an ADR.

## Azure Storage

Initially prefer one general-purpose Storage Account for the tiny v0 environment, unless security or operational constraints require separation.

Uses:

- Azure Functions runtime storage;
- Azure Table Storage for structured application data;
- Blob containers for private generated documents/exports.

Production isolation may later split runtime and application storage through an ADR.

## Infrastructure as Code

Use Bicep.

Expected layout:

```text
infra/azure/
  main.bicep
  modules/
    storage.bicep
    function-app.bicep
    monitoring.bicep
  environments/
    dev.bicepparam
    prod.bicepparam   # only once production exists
```

No production resource should depend on undocumented portal clicks.

IaC must not contain secrets.

## Authentication to Azure

Prefer GitHub Actions OIDC/workload identity federation over stored Azure client secrets.

Prefer managed identity from the Function app to Azure Storage and other Azure services where supported.

## Secrets

v0 secrets may live in protected Function application settings when appropriate.

Introduce Key Vault when:

- secret count/lifecycle warrants it;
- rotation requirements increase;
- multiple services need controlled access;
- production security review requires it.

Never commit API keys or connection strings.

## CI

On pull request:

1. install pinned Python dependencies;
2. lint;
3. typecheck;
4. run unit tests;
5. run golden fiscal tests;
6. run integration tests that do not require shared production resources;
7. optionally run Playwright against a local app.

## CD

On approved merge to the deployment branch:

1. CI must already pass;
2. deploy/update infrastructure through Bicep when required;
3. package and deploy the Function app;
4. run smoke test against `/health`;
5. run a minimal synthetic acceptance scenario where practical.

Production deployment policy can become stricter before real users are onboarded.

## Environments

Start with only:

- `local`;
- `dev`.

Add `prod` only when the end-to-end vertical slice is safe enough for real data.

Do not create staging, QA or other environments until there is a concrete need.

## Local development

Local application code must not require Azure.

Use:

- FastAPI locally;
- in-memory storage fakes for ordinary development/tests;
- Azurite only when testing Azure Storage adapters;
- environment-based configuration through Pydantic settings or equivalent.

## Observability

Use structured logging and Application Insights/basic Azure monitoring.

Never log:

- fiscal codes;
- invoice full contents;
- addresses;
- raw uploaded documents;
- complete LLM prompts containing sensitive tax data;
- storage credentials.

Recommended correlation fields:

- request/correlation id;
- synthetic/opaque user id when truly needed;
- workflow name;
- ruleset/calculation version;
- review status;
- latency/error classification.

## Cost discipline

v0 is explicitly optimized for low idle cost:

- serverless compute;
- no SQL server;
- no always-on worker;
- no Redis;
- one tiny Azure environment;
- storage-first persistence;
- pay-per-use external AI calls.

Add infrastructure only after a measurable product requirement justifies it.
