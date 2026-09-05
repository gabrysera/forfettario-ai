from datetime import date
from io import BytesIO

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from app.documents.aa912 import AA912OpeningData, render_aa912_opening


def test_page_headers_stay_in_header_area() -> None:
    reader = PdfReader(BytesIO(render_aa912_opening(_blank_template(), _data())))

    assert 690 < _highest_single_r_y(reader, 1) < 710
    for page_index in (2, 3, 4):
        assert _highest_single_r_y(reader, page_index) > 780


def _highest_single_r_y(reader: PdfReader, page_index: int) -> float:
    y_positions: list[float] = []

    def visitor(
        text: str,
        _cm: list[float],
        text_matrix: list[float],
        _font: object,
        _font_size: float,
    ) -> None:
        if text.strip() == "R":
            y_positions.append(float(text_matrix[5]))

    reader.pages[page_index].extract_text(visitor_text=visitor)
    return max(y_positions)


def _data() -> AA912OpeningData:
    return AA912OpeningData(
        fiscal_code="RSSMRA80A01H501U",
        surname="Rossi",
        given_name="Mario",
        birth_date=date(1980, 1, 1),
        birth_municipality="Roma",
        birth_province="RM",
        residence_address="Via Roma 10",
        residence_postal_code="00100",
        residence_municipality="Roma",
        residence_province="RM",
        start_date=date(2026, 9, 5),
        declaration_date=date(2026, 9, 5),
    )


def _blank_template() -> bytes:
    buffer = BytesIO()
    pdf = Canvas(buffer, pagesize=A4)
    for _ in range(5):
        pdf.showPage()
    pdf.save()
    return buffer.getvalue()
