from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ReviewStatus(StrEnum):
    AUTO_VALIDATED = "AUTO_VALIDATED"
    USER_CONFIRMATION_REQUIRED = "USER_CONFIRMATION_REQUIRED"
    PROFESSIONAL_REVIEW_REQUIRED = "PROFESSIONAL_REVIEW_REQUIRED"
    UNSUPPORTED = "UNSUPPORTED"


class SourceReference(Model):
    source_id: str
    title: str
    url: str
    effective_from: date | None = None
    effective_to: date | None = None


class TaxpayerProfile(Model):
    taxpayer_id: UUID


class ActivityClassification(Model):
    ateco_version: str
    code: str
    description: str
    confirmed: bool = False


class TaxRegimeAssessment(Model):
    tax_year: int
    review_status: ReviewStatus
    condition_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()


class SocialSecurityAssessment(Model):
    tax_year: int
    review_status: ReviewStatus
    scheme: str | None = None
    source_ids: tuple[str, ...] = ()
