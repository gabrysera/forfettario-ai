from .models import (
    SUPPORTED_ACTIVITY_DESCRIPTION,
    SUPPORTED_ATECO_CODE,
    AA912Draft,
    AA912OpeningProfile,
)

_FORFETTARIO_REGIME_CODE = "2"
_COMPILED_SECTIONS = ("A", "B", "C", "I")
_TOTAL_DECLARATION_PAGES = 4


def build_aa912_draft(profile: AA912OpeningProfile) -> AA912Draft:
    return AA912Draft(
        fiscal_code=profile.fiscal_code,
        surname=profile.surname,
        given_name=profile.given_name,
        birth_date=profile.birth_date,
        birth_municipality=profile.birth_municipality,
        birth_province=profile.birth_province,
        residence=profile.residence,
        activity_address=profile.effective_activity_address,
        records_at_activity_address=profile.records_at_activity_address,
        start_date=profile.start_date,
        declaration_date=profile.declaration_date,
        ateco_code=SUPPORTED_ATECO_CODE,
        activity_description=SUPPORTED_ACTIVITY_DESCRIPTION,
        tax_regime_code=_FORFETTARIO_REGIME_CODE,
        email=profile.email,
        phone_prefix=profile.phone_prefix,
        phone_number=profile.phone_number,
        fax_prefix=profile.fax_prefix,
        fax_number=profile.fax_number,
        website=profile.website,
        activity_property=profile.activity_property,
        intra_eu=profile.intra_eu,
        compiled_sections=_COMPILED_SECTIONS,
        total_pages=_TOTAL_DECLARATION_PAGES,
    )
