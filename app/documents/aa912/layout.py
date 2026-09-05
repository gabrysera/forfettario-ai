from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TextField:
    page: int
    x: float
    top: float
    max_width: float
    font_size: float = 8.5


@dataclass(frozen=True, slots=True)
class BoxedField:
    page: int
    x: float
    top: float
    max_chars: int
    step: float = 14.4
    font_size: float = 8.0


@dataclass(frozen=True, slots=True)
class MarkField:
    page: int
    x: float
    top: float


@dataclass(frozen=True, slots=True)
class CenterField:
    page: int
    x: float
    top: float
    font_size: float = 8.0


# Physical PDF pages. Page 1 is the privacy notice and is not part of the numbered declaration.
FISCAL_CODE_HEADERS = {
    2: BoxedField(2, 237.0, 145.0, 16),
    3: BoxedField(3, 237.0, 45.0, 16),
    4: BoxedField(4, 237.0, 45.0, 16),
    5: BoxedField(5, 235.0, 45.0, 16),
}
PAGE_NUMBERS = {
    2: CenterField(2, 546.0, 145.0),
    3: CenterField(3, 546.0, 45.0),
    4: CenterField(4, 546.0, 45.0),
    5: CenterField(5, 550.0, 45.0),
}

# Page 2 - Quadri A, B, C.
OPENING_MARK = MarkField(2, 122.5, 193.5)
START_DATE = BoxedField(2, 464.0, 201.5, 8)
TAXPAYER_NAME = TextField(2, 120.0, 334.0, 430.0)
ATECO_CODE = BoxedField(2, 160.5, 420.8, 6)
ACTIVITY_DESCRIPTION = TextField(2, 258.0, 420.5, 295.0, 8.0)
ACTIVITY_ADDRESS = TextField(2, 120.0, 482.0, 425.0)
ACTIVITY_POSTAL_CODE = BoxedField(2, 120.0, 496.8, 5)
ACTIVITY_MUNICIPALITY = TextField(2, 193.0, 496.5, 345.0)
ACTIVITY_PROVINCE = BoxedField(2, 548.0, 496.8, 2)
ACTIVITY_RECORDS_MARK = MarkField(2, 556.5, 477.8)
TAX_REGIME = CenterField(2, 323.5, 548.0)
TITULAR_FISCAL_CODE = BoxedField(2, 162.0, 626.0, 16)
TITULAR_SURNAME = TextField(2, 350.0, 630.0, 105.0)
TITULAR_GIVEN_NAME = TextField(2, 460.0, 630.0, 95.0)
BIRTH_DATE = BoxedField(2, 120.0, 650.8, 8)
BIRTH_MUNICIPALITY = TextField(2, 237.0, 650.5, 300.0)
BIRTH_PROVINCE = BoxedField(2, 548.0, 650.8, 2)
RESIDENCE_ADDRESS = TextField(2, 120.0, 677.5, 425.0)
RESIDENCE_RECORDS_MARK = MarkField(2, 556.5, 677.3)
RESIDENCE_POSTAL_CODE = BoxedField(2, 120.0, 701.8, 5)
RESIDENCE_MUNICIPALITY = TextField(2, 193.0, 701.5, 345.0)
RESIDENCE_PROVINCE = BoxedField(2, 548.0, 701.8, 2)

# Page 4 - Quadro I.
EMAIL = TextField(4, 115.0, 463.0, 245.0, 8.0)
PHONE = TextField(4, 400.0, 463.0, 58.0, 8.0)
FAX = TextField(4, 498.0, 463.0, 58.0, 8.0)
WEBSITE = TextField(4, 115.0, 487.0, 430.0, 8.0)
PROPERTY_TENURE = CenterField(4, 146.0, 511.0)
CADASTRE_TYPE = CenterField(4, 208.0, 511.0)
CADASTRE_SECTION = CenterField(4, 271.0, 511.0)
CADASTRE_SHEET = CenterField(4, 336.0, 511.0)
CADASTRE_PARCEL = CenterField(4, 430.0, 511.0)
CADASTRE_SUBUNIT = CenterField(4, 520.0, 511.0)
CONTRACT_DATE = BoxedField(4, 247.0, 539.0, 8, 14.4)
CONTRACT_OFFICE = TextField(4, 362.0, 539.0, 40.0, 7.5)
CONTRACT_NUMBER = TextField(4, 406.0, 539.0, 80.0, 7.5)
CONTRACT_SUBNUMBER = TextField(4, 492.0, 539.0, 38.0, 7.5)
CONTRACT_SERIES = TextField(4, 535.0, 539.0, 12.0, 7.5)
EU_PURCHASES = BoxedField(4, 115.0, 568.0, 9, 12.0, 7.5)
EU_SALES = BoxedField(4, 312.0, 568.0, 9, 12.0, 7.5)

# Page 5 - compiled sections and signature area.
COMPILED_SECTION_MARKS = {
    "A": MarkField(5, 287.0, 92.8),
    "B": MarkField(5, 309.0, 92.8),
    "C": MarkField(5, 330.0, 92.8),
    "I": MarkField(5, 459.5, 92.8),
}
TOTAL_PAGES = CenterField(5, 550.0, 93.0)
DECLARATION_DATE = BoxedField(5, 137.0, 133.8, 8, 10.8)
SIGNER_FISCAL_CODE = BoxedField(5, 344.0, 133.8, 16)
