from datetime import date
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AA912OpeningData(BaseModel):
    """Confirmed facts required by the first supported AA9/12 opening path."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    fiscal_code: str = Field(pattern=r"^[A-Z0-9]{16}$")
    surname: str = Field(min_length=1, max_length=60)
    given_name: str = Field(min_length=1, max_length=60)
    birth_date: date
    birth_municipality: str = Field(min_length=1, max_length=60)
    birth_province: str = Field(pattern=r"^[A-Z]{2}$")

    residence_address: str = Field(min_length=1, max_length=120)
    residence_postal_code: str = Field(pattern=r"^\d{5}$")
    residence_municipality: str = Field(min_length=1, max_length=60)
    residence_province: str = Field(pattern=r"^[A-Z]{2}$")

    activity_at_residence: bool = True
    activity_address: str | None = Field(default=None, max_length=120)
    activity_postal_code: str | None = Field(default=None, pattern=r"^\d{5}$")
    activity_municipality: str | None = Field(default=None, max_length=60)
    activity_province: str | None = Field(default=None, pattern=r"^[A-Z]{2}$")
    accounting_records_at_activity_address: bool = True

    start_date: date
    ateco_code: str = "62.10.00"
    activity_description: str = "ATTIVITA DI PROGRAMMAZIONE INFORMATICA"
    declaration_date: date | None = None

    @field_validator(
        "fiscal_code",
        "birth_province",
        "residence_province",
        "activity_province",
        mode="before",
    )
    @classmethod
    def uppercase_codes(cls, value: object) -> object:
        return value.upper() if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_supported_path(self) -> Self:
        if self.ateco_code != "62.10.00":
            raise ValueError("v0 supports only ATECO 62.10.00")
        if not self.accounting_records_at_activity_address:
            raise ValueError("v0 supports records kept at the activity address only")
        if not self.activity_at_residence:
            fields = (
                self.activity_address,
                self.activity_postal_code,
                self.activity_municipality,
                self.activity_province,
            )
            if any(value is None or value == "" for value in fields):
                raise ValueError("activity address is required when it differs from residence")
        if self.declaration_date is not None and self.start_date > self.declaration_date:
            raise ValueError("start date cannot be after declaration date")
        return self

    @property
    def effective_activity_address(self) -> tuple[str, str, str, str]:
        if self.activity_at_residence:
            return (
                self.residence_address,
                self.residence_postal_code,
                self.residence_municipality,
                self.residence_province,
            )
        assert self.activity_address is not None
        assert self.activity_postal_code is not None
        assert self.activity_municipality is not None
        assert self.activity_province is not None
        return (
            self.activity_address,
            self.activity_postal_code,
            self.activity_municipality,
            self.activity_province,
        )
