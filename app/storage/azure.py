from collections.abc import Mapping

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.data.tables import UpdateMode
from azure.data.tables.aio import TableClient
from azure.storage.blob import ContentSettings
from azure.storage.blob.aio import ContainerClient

from .ports import AuditEventAlreadyExists, DocumentAlreadyExists, Entity


def _prefix_end(prefix: str) -> str:
    if not prefix:
        raise ValueError("row_key_prefix must not be empty")

    codepoints = [ord(char) for char in prefix]
    for index in range(len(codepoints) - 1, -1, -1):
        if codepoints[index] < 0x10FFFF:
            codepoints[index] += 1
            return "".join(chr(value) for value in codepoints[: index + 1])
    raise ValueError("row_key_prefix has no lexical upper bound")


class AzureTableUserStateRepository:
    def __init__(self, client: TableClient) -> None:
        self._client = client

    async def get(self, user_id: str, row_key: str) -> Entity | None:
        try:
            entity = await self._client.get_entity(partition_key=user_id, row_key=row_key)
        except ResourceNotFoundError:
            return None
        return dict(entity)

    async def upsert(self, user_id: str, row_key: str, values: Mapping[str, object]) -> None:
        await self._client.upsert_entity(
            {"PartitionKey": user_id, "RowKey": row_key, **values},
            mode=UpdateMode.REPLACE,
        )

    async def list_prefix(self, user_id: str, row_key_prefix: str) -> list[Entity]:
        entities = self._client.query_entities(
            "PartitionKey eq @partition and RowKey ge @start and RowKey lt @end",
            parameters={
                "partition": user_id,
                "start": row_key_prefix,
                "end": _prefix_end(row_key_prefix),
            },
        )
        return [dict(entity) async for entity in entities]


class AzureTableAuditRepository:
    def __init__(self, client: TableClient) -> None:
        self._client = client

    async def append(self, user_id: str, row_key: str, values: Mapping[str, object]) -> None:
        try:
            await self._client.create_entity({"PartitionKey": user_id, "RowKey": row_key, **values})
        except ResourceExistsError as exc:
            raise AuditEventAlreadyExists(row_key) from exc

    async def list(self, user_id: str) -> list[Entity]:
        entities = self._client.query_entities(
            "PartitionKey eq @partition",
            parameters={"partition": user_id},
        )
        return [dict(entity) async for entity in entities]


class AzureBlobDocumentStore:
    def __init__(self, client: ContainerClient) -> None:
        self._client = client

    async def put(self, path: str, data: bytes, content_type: str) -> None:
        try:
            await self._client.upload_blob(
                name=path,
                data=data,
                overwrite=False,
                content_settings=ContentSettings(content_type=content_type),
            )
        except ResourceExistsError as exc:
            raise DocumentAlreadyExists(path) from exc

    async def get(self, path: str) -> bytes | None:
        try:
            stream = await self._client.download_blob(path)
        except ResourceNotFoundError:
            return None
        return await stream.readall()
