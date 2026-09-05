from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from pypdf import PdfReader

from app.main import create_app
from tests.aa912_support import validated_synthetic_template


def test_opening_page_is_available() -> None:
    response = TestClient(create_app()).get("/opening")

    assert response.status_code == 200
    assert "Apri la tua Partita IVA" in response.text


def test_valid_form_generates_pdf_without_accepting_rogue_fiscal_fields(
    monkeypatch: object,
    tmp_path: Path,
) -> None:
    import app.web.opening as opening

    source = tmp_path / "template.pdf"
    source.write_bytes(b"synthetic")
    monkeypatch.setattr(opening, "_template_path", lambda: source)  # type: ignore[attr-defined]
    monkeypatch.setattr(  # type: ignore[attr-defined]
        opening,
        "validate_template",
        lambda _: validated_synthetic_template(),
    )

    data = _form_data()
    data["ateco_code"] = "99.99.99"
    response = TestClient(create_app()).post("/opening/aa912.pdf", data=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    text = PdfReader(BytesIO(response.content)).pages[1].extract_text().replace(" ", "")
    assert "621000" in text
    assert "999999" not in text


def test_unsupported_records_location_fails_closed(
    monkeypatch: object,
    tmp_path: Path,
) -> None:
    import app.web.opening as opening

    source = tmp_path / "template.pdf"
    source.write_bytes(b"synthetic")
    monkeypatch.setattr(opening, "_template_path", lambda: source)  # type: ignore[attr-defined]
    monkeypatch.setattr(  # type: ignore[attr-defined]
        opening,
        "validate_template",
        lambda _: validated_synthetic_template(),
    )

    data = _form_data()
    data["records_at_activity_address"] = "no"
    response = TestClient(create_app()).post("/opening/aa912.pdf", data=data)

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("text/html")


def test_missing_official_template_is_reported_as_service_unavailable(
    monkeypatch: object,
    tmp_path: Path,
) -> None:
    import app.web.opening as opening

    monkeypatch.setattr(  # type: ignore[attr-defined]
        opening,
        "_template_path",
        lambda: tmp_path / "missing.pdf",
    )

    response = TestClient(create_app()).post("/opening/aa912.pdf", data=_form_data())

    assert response.status_code == 503
    assert "modello AA9/12 ufficiale" in response.text


def _form_data() -> dict[str, str]:
    return {
        "fiscal_code": "RSSMRA80A01H501U",
        "surname": "Rossi",
        "given_name": "Mario",
        "birth_date": "1980-01-01",
        "birth_municipality": "Roma",
        "birth_province": "RM",
        "residence_address": "Via Esempio 10",
        "residence_postal_code": "00100",
        "residence_municipality": "Roma",
        "residence_province": "RM",
        "activity_at_residence": "yes",
        "records_at_activity_address": "yes",
        "start_date": "2026-09-05",
        "declaration_date": "2026-09-05",
        "email": "mario.rossi@example.test",
        "phone_prefix": "+39",
        "phone_number": "061234567",
        "property_tenure": "P",
        "cadastre_type": "F",
        "cadastre_sheet": "123",
        "cadastre_parcel": "456",
        "cadastre_subunit": "7",
        "wants_vies": "no",
    }
