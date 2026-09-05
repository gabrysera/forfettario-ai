from io import BytesIO

import pytest
from pypdf import PdfReader

from app.documents.aa912.mapping import build_aa912_draft
from app.documents.aa912.renderer import DocumentOverflowError, render_aa912
from tests.aa912_support import profile, validated_synthetic_template


def test_renderer_preserves_template_and_populates_quadro_i() -> None:
    draft = build_aa912_draft(profile("aa912_home_owned_vies.json"))

    output = render_aa912(validated_synthetic_template(), draft)
    reader = PdfReader(BytesIO(output))

    assert len(reader.pages) == 5
    assert "TEMPLATE PAGE 1" in reader.pages[0].extract_text()
    assert "RSSMRA80A01H501U" in _compact(reader.pages[1].extract_text())
    assert "MARIO.ROSSI@EXAMPLE.TEST" in reader.pages[3].extract_text()
    assert "1000" in _compact(reader.pages[3].extract_text())
    assert "2500" in _compact(reader.pages[3].extract_text())


def test_renderer_rejects_text_that_does_not_physically_fit() -> None:
    draft = build_aa912_draft(profile()).model_copy(update={"surname": "X" * 100})

    with pytest.raises(DocumentOverflowError):
        render_aa912(validated_synthetic_template(), draft)


def _compact(text: str) -> str:
    return "".join(text.split())
