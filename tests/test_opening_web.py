from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from pypdf import PdfReader

from app.main import create_app
from tests.aa912_support import profile, validated_synthetic_template


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
    text = _compact(PdfReader(BytesIO(response.content)).pages[1].extract_text())
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
    opening = profile()
    premises = opening.activity_property
    return {
        "fiscal_code": opening.fiscal_code,
        "surname": opening.surname,
        "given_name": opening.given_name,
        "birth_date": opening.birth_date.isoformat(),
        "birth_municipality": opening.birth_municipality,
        "birth_province": opening.birth_province,
        "residence_address": opening.residence.address,
        "residence_postal_code": opening.residence.postal_code,
        "residence_municipality": opening.residence.municipality,
        "residence_province": opening.residence.province,
        "activity_at_residence": "yes",
        "records_at_activity_address": "yes",
        "start_date": opening.start_date.isoformat(),
        "declaration_date": opening.declaration_date.isoformat()
        if opening.declaration_date
        else "",
        "email": opening.email,
        "phone_prefix": opening.phone_prefix,
        "phone_number": opening.phone_number,
        "property_tenure": premises.tenure.value,
        "cadastre_type": premises.cadastre_type.value,
        "cadastre_sheet": premises.sheet,
        "cadastre_parcel": premises.parcel,
        "cadastre_subunit": premises.subunit or "",
        "wants_vies": "no",
    }


def _compact(text: str) -> str:
    return "".join(text.split())
