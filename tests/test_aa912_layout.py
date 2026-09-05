from app.documents.aa912 import layout


def test_fiscal_code_headers_follow_real_template_geometry() -> None:
    assert layout.FISCAL_CODE_HEADERS[2].top == 145.0
    assert layout.FISCAL_CODE_HEADERS[3].top == 45.0
    assert layout.FISCAL_CODE_HEADERS[4].top == 45.0
    assert layout.FISCAL_CODE_HEADERS[5].top == 45.0


def test_quadro_i_fields_are_on_physical_page_four() -> None:
    fields = (
        layout.EMAIL,
        layout.PHONE_PREFIX,
        layout.PHONE_NUMBER,
        layout.PROPERTY_TENURE,
        layout.CADASTRE_SHEET,
        layout.CONTRACT_DATE,
        layout.EU_PURCHASES,
        layout.EU_SALES,
    )
    assert {field.page for field in fields} == {4}


def test_vies_volumes_stay_inside_the_operations_row() -> None:
    assert layout.EU_PURCHASES.top == 559.0
    assert layout.EU_SALES.top == 559.0


def test_signature_summary_includes_quadro_i() -> None:
    assert layout.COMPILED_SECTION_MARKS["I"].page == 5
    assert layout.TOTAL_PAGES.page == 5
