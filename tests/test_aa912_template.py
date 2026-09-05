import pytest
from reportlab.lib.pagesizes import LETTER

from app.documents.aa912.template import InvalidAA912Template, TemplateProfile, validate_template
from tests.aa912_support import synthetic_template


def test_unknown_five_page_pdf_is_rejected_by_official_profile() -> None:
    content, _ = synthetic_template()

    with pytest.raises(InvalidAA912Template, match="fingerprint"):
        validate_template(content)


def test_known_template_profile_accepts_matching_pdf() -> None:
    content, profile = synthetic_template()

    validated = validate_template(content, profile)

    assert validated.pdf == content
    assert validated.profile == profile


def test_geometry_is_part_of_template_contract() -> None:
    content, matching = synthetic_template(pagesize=LETTER)
    expected_a4 = TemplateProfile(
        template_id=matching.template_id,
        sha256=matching.sha256,
        source_url=matching.source_url,
        page_count=matching.page_count,
        page_width=595.276,
        page_height=841.89,
    )

    with pytest.raises(InvalidAA912Template, match="geometry"):
        validate_template(content, expected_a4)
