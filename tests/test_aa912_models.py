import pytest
from pydantic import ValidationError

from app.documents.aa912.mapping import build_aa912_draft
from app.documents.aa912.models import AA912OpeningProfile
from tests.aa912_support import profile


def test_supported_home_owned_case_maps_deterministically() -> None:
    opening = profile()
    draft = build_aa912_draft(opening)

    assert draft.ateco_code == "62.10.00"
    assert draft.activity_description == "ATTIVITA DI PROGRAMMAZIONE INFORMATICA"
    assert draft.tax_regime_code == "2"
    assert draft.activity_address == opening.residence
    assert draft.compiled_sections == ("A", "B", "C", "I")
    assert draft.total_pages == 4


def test_rented_property_requires_registration_details() -> None:
    data = profile("aa912_home_rented_no_vies.json").model_dump(mode="json")
    data["activity_property"]["contract_registration_number"] = None

    with pytest.raises(ValidationError):
        AA912OpeningProfile.model_validate(data)


def test_vies_requires_both_expected_volumes() -> None:
    data = profile("aa912_home_owned_vies.json").model_dump(mode="json")
    data["intra_eu"]["expected_sales"] = None

    with pytest.raises(ValidationError):
        AA912OpeningProfile.model_validate(data)


def test_vies_volumes_must_fit_whole_euro_fields() -> None:
    data = profile("aa912_home_owned_vies.json").model_dump(mode="json")
    data["intra_eu"]["expected_sales"] = "2500.50"

    with pytest.raises(ValidationError):
        AA912OpeningProfile.model_validate(data)


def test_alternate_records_location_fails_closed() -> None:
    data = profile().model_dump(mode="json")
    data["records_at_activity_address"] = False

    with pytest.raises(ValidationError):
        AA912OpeningProfile.model_validate(data)


def test_invalid_fiscal_code_is_rejected() -> None:
    data = profile().model_dump(mode="json")
    data["fiscal_code"] = "RSSMRA80A01H501A"

    with pytest.raises(ValidationError):
        AA912OpeningProfile.model_validate(data)
