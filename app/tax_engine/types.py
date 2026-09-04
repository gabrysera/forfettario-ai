from dataclasses import dataclass
from enum import StrEnum


class ConditionStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ConditionResult:
    condition_id: str
    status: ConditionStatus
    source_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Assessment:
    conditions: tuple[ConditionResult, ...]

    @property
    def eligible(self) -> bool | None:
        statuses = {condition.status for condition in self.conditions}
        if ConditionStatus.FAIL in statuses:
            return False
        if ConditionStatus.UNKNOWN in statuses:
            return None
        return True
