from collections.abc import Mapping
from typing import Protocol

type Entity = dict[str, object]


class StorageConflictError(RuntimeError):
    """Base error for a write that conflicts with existing persisted state."""


class AuditEventAlreadyExists(StorageConflictError):
    """Raised when an append-only audit event key is reused."""


class UserStateRepository(Protocol):
    async def get(self, user_id: str, row_key: str) -> Entity | None: ...

    async def upsert(self, user_id: str, row_key: str, values: Mapping[str, object]) -> None: ...

    async def list_prefix(self, user_id: str, row_key_prefix: str) -> list[Entity]: ...


class AuditRepository(Protocol):
    async def append(self, user_id: str, row_key: str, values: Mapping[str, object]) -> None: ...

    async def list(self, user_id: str) -> list[Entity]: ...


class DocumentStore(Protocol):
    async def put(self, path: str, data: bytes, content_type: str) -> None: ...

    async def get(self, path: str) -> bytes | None: ...
