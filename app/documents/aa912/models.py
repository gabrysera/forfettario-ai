from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.fiscal_code import is_valid_fiscal_code

SUPPORTED_ATECO_CODE = "62.10.00"
SUPPORTED_ACTIVITY_DESCRIPTION = "ATTIVITA DI PROGRAMMAZIONE INFORMATICA"


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class PropertyTenure(StrEnum):
    POSSESSION = "P"
    DETENTION = "D"


class CadastreType(StrEnum):
    BUILDING = "F"
    LAND = "T"


class Address(Model):
    address: str = Field(min_length=1, max_length=120)
    postal_code: str = Field(pattern=r"^\d{5}$")
    municipality: str = Field(min_length=1, max_length=60)
    province: str = Field(pattern=r"^[A-Z]{2}$")

    @field_validator("province", mode="before")
    @classmethod
    def uppercase_province(cls, value: object) -> object:
        return value.upper() if isinstance(value, str) else value


class PropertyDetails(Model):
    tenure: PropertyTenure
    cadastre_type: CadastreType
    section: str | None = Field(default=None, max_length=8)
    sheet: str = Field(min_length=1, max_length=8)
    parcel: str = Field(min_length=1, max_length=16)
    subunit: str | None = Field(default=None, max_length=8)
    contract_registration_date: date | None = None
    contract_registration_office: str | None = Field(default=None, max_length=12)
    contract_registration_number: str | None = Field(default=None, max_length=16)
    contract_registration_subnumber: str | None = Field(default=None, max_length=8)
    contract_registration_series: str | None = Field(default=None, max_length=8)

    @model_validator(mode="after")
    def require_contract_registration_for_detention(self) -> Self:
        required = (
            self.contract_registration_date,
            self.contract_registration_office,
            self.contract_registration_number,
        )
        if self.tenure is PropertyTenure.DETENTION and any(value in (None, "") for value in required):
            raise ValueError("registration details are required for a rented/loaned property")
        return self


class IntraEUPlan(Model):
    wants_vies: bool
    expected_purchases: Decimal | None = Field(default=None, ge=0)
    expected_sales: Decimal | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_expected_volumes(self) -> Self:
        volumes = (self.expected_purchases, self.expected_sales)
        if self.wants_vies and any(value is None for value in volumes):
            raise ValueError("expected EU purchase and sales volumes are required for VIES")
        if not self.wants_vies and any(value is not None for value in volumes):
            raise ValueError("EU volumes must be omitted when VIES is not requested")
        return self


class AA912OpeningProfile(Model):
    fiscal_code: str
    surname: str = Field(min_length=1, max_length=60)
    given_name: str = Field(min_length=1, max_length=60)
    birth_date: date
    birth_municipality: str = Field(min_length=1, max_length=60)
    birth_province: str = Field(pattern=r"^[A-Z]{2}$")
    residence: Address
    activity_at_residence: bool
    activity_address: Address | None = None
    records_at_activity_address: bool
    start_date: date
    declaration_date: date | None = None
    email: str = Field(min_length=3, max_length=120)
    phone: str = Field(min_length=3, max_length=30)
    fax: str | None = Field(default=None, max_length=30)
    website: str | None = Field(default=None, max_length=160)
    property: PropertyDetails
    intra_eu: IntraEUPlan

    @field_validator("fiscal_code", "birth_province", mode="before")
    @classmethod
    def uppercase_codes(cls, value: object) -> object:
        return value.upper() if isinstance(value, str) else value

    @field_validator("fiscal_code")
    @classmethod
    def validate_fiscal_code(cls, value: str) -> str:
        if not is_valid_fiscal_code(value):
            raise ValueError("invalid Italian fiscal code checksum")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if value.count("@") != 1 or value.startswith("@") or value.endswith("@"):
            raise ValueError("invalid email address")
        return value

    @model_validator(mode="after")
    def validate_supported_path(self) -> Self:
        if not self.activity_at_residence and self.activity_address is None:
            raise ValueError("activity address is required when it differs from residence")
        if self.activity_at_residence and self.activity_address is not None:
            raise ValueError("activity address must be omitted when activity is at residence")
        if self.declaration_date is not None and self.start_date > self.declaration_date:
            raise ValueError("start date cannot be after declaration date")
        return self

    @property
    def effective_activity_address(self) -> Address:
        return self.residence if self.activity_at_residence else self._explicit_activity_address()

    def _explicit_activity_address(self) -> Address:
        if self.activity_address is None:
            raise RuntimeError("validated profile is missing activity address")
        return self.activity_address


class AA912Draft(Model):
    fiscal_code: str
    surname: str
    given_name: str
    birth_date: date
    birth_municipality: str
    birth_province: str
    residence: Address
    activity_address: Address
    records_at_activity_address: bool
    start_date: date
    declaration_date: date | None
    ateco_code: str
    activity_description: str
    tax_regime_code: str
    email: str
    phone: str
    fax: str | None
    website: str | None
    property: PropertyDetails
    intra_eu: IntraEUPlan
    compiled_sections: tuple[str, ...]
    total_pages: int
