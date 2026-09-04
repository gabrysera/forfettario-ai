from collections.abc import Mapping
from typing import Any

from .ports import Entity


class InMemoryUserStateRepository:
    def __init__(self) -> None:
        self._entities: dict[tuple[str, str], Entity] = {}

    async def get(self, user_id: str, row_key: str) -> Entity | None:
        entity = self._entities.get((user_id, row_key))
        return dict(entity) if entity else None

    async def upsert(self, user_id: str, row_key: str, values: Mapping[str, Any]) -> None:
        self._entities[(user_id, row_key)] = {
            "PartitionKey": user_id,
            "RowKey": row_key,
            **values,
        }

    async def list_prefix(self, user_id: str, row_key_prefix: str) -> list[Entity]:
        return [
            dict(entity)
            for (partition, row_key), entity in sorted(self._entities.items())
            if partition == user_id and row_key.startswith(row_key_prefix)
        ]


class InMemoryAuditRepository:
    def __init__(self) -> None:
        self._entities: dict[tuple[str, str], Entity] = {}

    async def append(self, user_id: str, row_key: str, values: Mapping[str, Any]) -> None:
        key = (user_id, row_key)
        if key in self._entities:
            raise ValueError(f"Audit event already exists: {row_key}")
        self._entities[key] = {"PartitionKey": user_id, "RowKey": row_key, **values}

    async def list(self, user_id: str) -> list[Entity]:
        return [
            dict(entity)
            for (partition, _), entity in sorted(self._entities.items())
            if partition == user_id
        ]


class InMemoryDocumentStore:
    def __init__(self) -> None:
        self._documents: dict[str, bytes] = {}

    async def put(self, path: str, data: bytes, content_type: str) -> None:
        del content_type
        self._documents[path] = data

    async def get(self, path: str) -> bytes | None:
        return self._documents.get(path)
