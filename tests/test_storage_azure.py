from typing import cast

import pytest
from azure.core.exceptions import ResourceExistsError
from azure.data.tables.aio import TableClient
from azure.storage.blob.aio import ContainerClient

from app.storage.azure import AzureBlobDocumentStore, AzureTableAuditRepository
from app.storage.ports import AuditEventAlreadyExists, DocumentAlreadyExists


class _ExistingAuditClient:
    async def create_entity(self, entity: object) -> None:
        del entity
        raise ResourceExistsError("already exists")


class _ExistingBlobClient:
    async def upload_blob(self, **kwargs: object) -> None:
        del kwargs
        raise ResourceExistsError("already exists")


@pytest.mark.asyncio
async def test_azure_audit_conflict_is_provider_independent() -> None:
    repository = AzureTableAuditRepository(cast(TableClient, _ExistingAuditClient()))

    with pytest.raises(AuditEventAlreadyExists):
        await repository.append("user", "event", {"event_type": "Example"})


@pytest.mark.asyncio
async def test_azure_document_conflict_is_provider_independent() -> None:
    store = AzureBlobDocumentStore(cast(ContainerClient, _ExistingBlobClient()))

    with pytest.raises(DocumentAlreadyExists):
        await store.put("user/aa912/document.pdf", b"pdf", "application/pdf")
