import pytest

from app.storage.memory import (
    InMemoryAuditRepository,
    InMemoryDocumentStore,
    InMemoryUserStateRepository,
)


@pytest.mark.asyncio
async def test_user_state_is_partitioned_and_prefix_queryable() -> None:
    repository = InMemoryUserStateRepository()

    await repository.upsert("user-a", "INVOICE#2026#2", {"amount": 200})
    await repository.upsert("user-a", "INVOICE#2026#1", {"amount": 100})
    await repository.upsert("user-b", "INVOICE#2026#3", {"amount": 300})

    invoices = await repository.list_prefix("user-a", "INVOICE#2026#")

    assert [invoice["amount"] for invoice in invoices] == [100, 200]


@pytest.mark.asyncio
async def test_audit_events_are_append_only() -> None:
    repository = InMemoryAuditRepository()

    await repository.append("user-a", "2026-09-04T00:00:00Z#1", {"event_type": "Example"})

    with pytest.raises(ValueError, match="already exists"):
        await repository.append(
            "user-a",
            "2026-09-04T00:00:00Z#1",
            {"event_type": "Example"},
        )


@pytest.mark.asyncio
async def test_document_store_round_trip() -> None:
    store = InMemoryDocumentStore()

    await store.put("user-a/aa912/2026/document.pdf", b"pdf", "application/pdf")

    assert await store.get("user-a/aa912/2026/document.pdf") == b"pdf"
    assert await store.get("missing.pdf") is None
