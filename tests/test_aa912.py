from datetime import date
from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from app.documents.aa912 import AA912OpeningData, InvalidAA912Template, render_aa912_opening
from app.main import create_app


def test_opening_data_requires_explicit_activity_address_when_different() -> None:
    with pytest.raises(ValidationError):
        _opening_data(activity_at_residence=False)


def test_renderer_overlays_confirmed_data_without_changing_page_count() -> None:
    result = render_aa912_opening(_blank_template(), _opening_data())
    reader = PdfReader(BytesIO(result))

    assert len(reader.pages) == 5
    page_two = reader.pages[1].extract_text()
    assert "SERAFINI GABRIELE" in page_two
    assert "ATTIVITA DI PROGRAMMAZIONE INFORMATICA" in page_two
    assert "VIA PIAVE 7/1" in page_two
    assert "CARUGO" in page_two


def test_renderer_rejects_wrong_template() -> None:
    with pytest.raises(InvalidAA912Template):
        render_aa912_opening(_blank_template(pages=1), _opening_data())


def test_opening_endpoint_returns_pdf(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    template = tmp_path / "aa9_12.pdf"
    template.write_bytes(_blank_template())
    monkeypatch.setenv("AA912_TEMPLATE_PATH", str(template))

    response = TestClient(create_app()).post(
        "/opening/aa912.pdf",
        data={
            "fiscal_code": "RSSMRA80A01H501U",
            "surname": "Rossi",
            "given_name": "Mario",
            "birth_date": "1980-01-01",
            "birth_municipality": "Roma",
            "birth_province": "RM",
            "residence_address": "Via Roma 10",
            "residence_postal_code": "00100",
            "residence_municipality": "Roma",
            "residence_province": "RM",
            "activity_at_residence": "on",
            "accounting_records_at_activity_address": "on",
            "start_date": "2026-09-05",
            "declaration_date": "2026-09-05",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "aa9-12-bozza.pdf" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")


def _opening_data(**overrides: object) -> AA912OpeningData:
    values: dict[str, object] = {
        "fiscal_code": "RSSMRA80A01H501U",
        "surname": "Rossi",
        "given_name": "Mario",
        "birth_date": date(1980, 1, 1),
        "birth_municipality": "Roma",
        "birth_province": "RM",
        "residence_address": "Via Piave 7/1",
        "residence_postal_code": "22060",
        "residence_municipality": "Carugo",
        "residence_province": "CO",
        "start_date": date(2026, 9, 5),
        "declaration_date": date(2026, 9, 5),
    }
    values.update(overrides)
    return AA912OpeningData.model_validate(values)


def _blank_template(pages: int = 5) -> bytes:
    buffer = BytesIO()
    pdf = Canvas(buffer, pagesize=A4)
    for _ in range(pages):
        pdf.showPage()
    pdf.save()
    return buffer.getvalue()
