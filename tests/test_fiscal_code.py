from app.domain.fiscal_code import is_valid_fiscal_code


def test_valid_fiscal_code_checksum() -> None:
    assert is_valid_fiscal_code("RSSMRA80A01H501U")
    assert is_valid_fiscal_code("rssmra80a01h501u")


def test_invalid_fiscal_code_checksum() -> None:
    assert not is_valid_fiscal_code("RSSMRA80A01H501A")
    assert not is_valid_fiscal_code("SHORT")
