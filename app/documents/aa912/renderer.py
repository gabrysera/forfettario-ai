from datetime import date
from decimal import Decimal
from io import BytesIO

from pypdf import PageObject, PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from . import layout
from .layout import BoxedField, CenterField, MarkField, TextField
from .models import AA912Draft, PropertyTenure
from .template import ValidatedTemplate

_PAGE_HEIGHT = float(A4[1])


class DocumentOverflowError(ValueError):
    pass


def render_aa912(template: ValidatedTemplate, draft: AA912Draft) -> bytes:
    writer = PdfWriter(clone_from=BytesIO(template.pdf))

    for physical_page in range(2, template.profile.page_count + 1):
        overlay = _overlay(physical_page, draft)
        writer.pages[physical_page - 1].merge_page(overlay)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _overlay(physical_page: int, draft: AA912Draft) -> PageObject:
    buffer = BytesIO()
    pdf = Canvas(buffer, pagesize=A4)

    _boxed(pdf, layout.FISCAL_CODE_HEADERS[physical_page], draft.fiscal_code)
    _center(pdf, layout.PAGE_NUMBERS[physical_page], str(physical_page - 1))

    if physical_page == 2:
        _opening_page(pdf, draft)
    elif physical_page == 4:
        _quadro_i(pdf, draft)
    elif physical_page == 5:
        _signature_page(pdf, draft)

    pdf.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def _opening_page(pdf: Canvas, draft: AA912Draft) -> None:
    activity = draft.activity_address
    residence = draft.residence

    _mark(pdf, layout.OPENING_MARK)
    _boxed(pdf, layout.START_DATE, _date(draft.start_date))
    _text(pdf, layout.TAXPAYER_NAME, f"{draft.surname} {draft.given_name}")
    _boxed(pdf, layout.ATECO_CODE, draft.ateco_code)
    _text(pdf, layout.ACTIVITY_DESCRIPTION, draft.activity_description)
    _text(pdf, layout.ACTIVITY_ADDRESS, activity.address)
    _boxed(pdf, layout.ACTIVITY_POSTAL_CODE, activity.postal_code)
    _text(pdf, layout.ACTIVITY_MUNICIPALITY, activity.municipality)
    _boxed(pdf, layout.ACTIVITY_PROVINCE, activity.province)
    if draft.records_at_activity_address:
        _mark(pdf, layout.ACTIVITY_RECORDS_MARK)

    _center(pdf, layout.TAX_REGIME, draft.tax_regime_code)
    _boxed(pdf, layout.TITULAR_FISCAL_CODE, draft.fiscal_code)
    _text(pdf, layout.TITULAR_SURNAME, draft.surname)
    _text(pdf, layout.TITULAR_GIVEN_NAME, draft.given_name)
    _boxed(pdf, layout.BIRTH_DATE, _date(draft.birth_date))
    _text(pdf, layout.BIRTH_MUNICIPALITY, draft.birth_municipality)
    _boxed(pdf, layout.BIRTH_PROVINCE, draft.birth_province)
    _text(pdf, layout.RESIDENCE_ADDRESS, residence.address)
    if draft.records_at_activity_address and activity == residence:
        _mark(pdf, layout.RESIDENCE_RECORDS_MARK)
    _boxed(pdf, layout.RESIDENCE_POSTAL_CODE, residence.postal_code)
    _text(pdf, layout.RESIDENCE_MUNICIPALITY, residence.municipality)
    _boxed(pdf, layout.RESIDENCE_PROVINCE, residence.province)


def _quadro_i(pdf: Canvas, draft: AA912Draft) -> None:
    property_details = draft.activity_property

    _text(pdf, layout.EMAIL, draft.email)
    _text(pdf, layout.PHONE_PREFIX, draft.phone_prefix)
    _text(pdf, layout.PHONE_NUMBER, draft.phone_number)
    if draft.fax_prefix is not None and draft.fax_number is not None:
        _text(pdf, layout.FAX_PREFIX, draft.fax_prefix)
        _text(pdf, layout.FAX_NUMBER, draft.fax_number)
    if draft.website:
        _text(pdf, layout.WEBSITE, draft.website)

    _center(pdf, layout.PROPERTY_TENURE, property_details.tenure.value)
    _center(pdf, layout.CADASTRE_TYPE, property_details.cadastre_type.value)
    _center(pdf, layout.CADASTRE_SECTION, property_details.section or "")
    _center(pdf, layout.CADASTRE_SHEET, property_details.sheet)
    _center(pdf, layout.CADASTRE_PARCEL, property_details.parcel)
    _center(pdf, layout.CADASTRE_SUBUNIT, property_details.subunit or "")

    if property_details.tenure is PropertyTenure.DETENTION:
        registration_date = property_details.contract_registration_date
        registration_office = property_details.contract_registration_office
        registration_number = property_details.contract_registration_number
        if registration_date is None or registration_office is None or registration_number is None:
            raise RuntimeError("validated detention property is missing registration details")
        _boxed(pdf, layout.CONTRACT_DATE, _date(registration_date))
        _text(pdf, layout.CONTRACT_OFFICE, registration_office)
        _text(pdf, layout.CONTRACT_NUMBER, registration_number)
        if property_details.contract_registration_subnumber:
            _text(pdf, layout.CONTRACT_SUBNUMBER, property_details.contract_registration_subnumber)
        if property_details.contract_registration_series:
            _text(pdf, layout.CONTRACT_SERIES, property_details.contract_registration_series)

    if draft.intra_eu.wants_vies:
        purchases = draft.intra_eu.expected_purchases
        sales = draft.intra_eu.expected_sales
        if purchases is None or sales is None:
            raise RuntimeError("validated VIES plan is missing expected volumes")
        _boxed(pdf, layout.EU_PURCHASES, _euros(purchases))
        _boxed(pdf, layout.EU_SALES, _euros(sales))


def _signature_page(pdf: Canvas, draft: AA912Draft) -> None:
    for section in draft.compiled_sections:
        field = layout.COMPILED_SECTION_MARKS.get(section)
        if field is None:
            raise ValueError(f"unsupported compiled AA9/12 section: {section}")
        _mark(pdf, field)

    _center(pdf, layout.TOTAL_PAGES, str(draft.total_pages))
    if draft.declaration_date is not None:
        _boxed(pdf, layout.DECLARATION_DATE, _date(draft.declaration_date))
    _boxed(pdf, layout.SIGNER_FISCAL_CODE, draft.fiscal_code)
    # The declarant signature is intentionally never generated by software.


def _boxed(pdf: Canvas, field: BoxedField, value: str) -> None:
    text = _compact(value)
    if len(text) > field.max_chars:
        raise DocumentOverflowError(
            f"value does not fit boxed field on page {field.page}: {text!r}"
        )
    pdf.setFont("Helvetica", field.font_size)
    for index, character in enumerate(text):
        pdf.drawCentredString(field.x + index * field.step, _y(field.top), character)


def _text(pdf: Canvas, field: TextField, value: str) -> None:
    text = value.upper()
    _ensure_width(text, field.max_width, field.font_size, field.page)
    pdf.setFont("Helvetica", field.font_size)
    pdf.drawString(field.x, _y(field.top), text)


def _center(pdf: Canvas, field: CenterField, value: str) -> None:
    text = value.upper()
    if field.max_width is not None:
        _ensure_width(text, field.max_width, field.font_size, field.page)
    pdf.setFont("Helvetica", field.font_size)
    pdf.drawCentredString(field.x, _y(field.top), text)


def _mark(pdf: Canvas, field: MarkField) -> None:
    pdf.setFont("Helvetica-Bold", 8.0)
    pdf.drawCentredString(field.x, _y(field.top), "X")


def _ensure_width(text: str, max_width: float, font_size: float, page: int) -> None:
    if stringWidth(text, "Helvetica", font_size) > max_width:
        raise DocumentOverflowError(f"text does not fit AA9/12 field on page {page}: {text!r}")


def _date(value: date) -> str:
    return value.strftime("%d%m%Y")


def _euros(value: Decimal) -> str:
    return str(int(value))


def _compact(value: str) -> str:
    return value.upper().translate(str.maketrans("", "", ". /-"))


def _y(top: float) -> float:
    return _PAGE_HEIGHT - top
