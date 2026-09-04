# Azure infrastructure

This directory contains Bicep IaC for the v0 serverless deployment.

Target architecture:

- Azure Functions v4 — Flex Consumption;
- Azure Storage account;
- Azure Table Storage;
- private Azure Blob containers;
- Application Insights / required monitoring resources;
- managed identity / RBAC where supported.

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
```

Do not add PostgreSQL, SQL Database, Redis, VM, Kubernetes, Container Apps or other always-on services without an ADR that replaces or extends ADR-003.

See:

- `docs/DEPLOYMENT.md`
- `docs/STORAGE_MODEL.md`
- `docs/decisions/ADR-003-storage-first-serverless-azure.md`
