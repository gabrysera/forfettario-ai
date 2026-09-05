import pytest

from app.storage.memory import (
    InMemoryAuditRepository,
    InMemoryDocumentStore,
    InMemoryUserStateRepository,
)
from app.storage.ports import AuditEventAlreadyExists, DocumentAlreadyExists


@pytest.mark.asyncio
async def test_user_state_is_partitioned_and_prefix_queryable() -> None:
    repository = InMemoryUserStateRepository()

    await repository.upsert("user-a", "INVOICE#2026#2", {"amount": 200})
    await repository.upsert("user-a", "INVOICE#2026#1", {"amount": 100})
    await repository.upsert("user-b", "INVOICE#2026#3", {"amount": 300})

    invoices = await repository.list_prefix("user-a", "INVOICE#2026#")

    assert [invoice["amount"] for invoice in invoices] == [100, 200]


@pytest.mark.asyncio
async def test_repository_keys_cannot_be_overridden_by_payload() -> None:
    repository = InMemoryUserStateRepository()

    await repository.upsert(
        "user-a",
        "PROFILE",
        {"PartitionKey": "attacker", "RowKey": "OTHER", "schema_version": 1},
    )

    entity = await repository.get("user-a", "PROFILE")
    assert entity is not None
    assert entity["PartitionKey"] == "user-a"
    assert entity["RowKey"] == "PROFILE"


@pytest.mark.asyncio
async def test_empty_prefix_is_rejected_consistently() -> None:
    repository = InMemoryUserStateRepository()

    with pytest.raises(ValueError, match="must not be empty"):
        await repository.list_prefix("user-a", "")


@pytest.mark.asyncio
async def test_audit_events_are_append_only() -> None:
    repository = InMemoryAuditRepository()

    await repository.append("user-a", "2026-09-04T00:00:00Z#1", {"event_type": "Example"})

    with pytest.raises(AuditEventAlreadyExists):
        await repository.append(
            "user-a",
            "2026-09-04T00:00:00Z#1",
            {"event_type": "Example"},
        )


@pytest.mark.asyncio
async def test_documents_are_immutable() -> None:
    store = InMemoryDocumentStore()
    path = "user-a/aa912/2026/document.pdf"

    await store.put(path, b"first", "application/pdf")

    with pytest.raises(DocumentAlreadyExists):
        await store.put(path, b"replacement", "application/pdf")

    assert await store.get(path) == b"first"
    assert await store.get("missing.pdf") is None
