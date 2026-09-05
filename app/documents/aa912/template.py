from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO

from pypdf import PdfReader


@dataclass(frozen=True, slots=True)
class TemplateProfile:
    template_id: str
    sha256: str
    source_url: str
    page_count: int
    page_width: float
    page_height: float


@dataclass(frozen=True, slots=True)
class ValidatedTemplate:
    profile: TemplateProfile
    pdf: bytes


class InvalidAA912Template(ValueError):
    pass


SUPPORTED_TEMPLATE = TemplateProfile(
    template_id="aa9-12-2025-06-04",
    sha256="a75a7ddab209b5355dc0ab40f78e6ba27d43806140ab60de1f9c8857dc32c599",
    source_url=(
        "https://www.agenziaentrate.gov.it/portale/documents/d/guest/"
        "modello-aa9_aa9_12-modello-pdf"
    ),
    page_count=5,
    page_width=595.276,
    page_height=841.89,
)


def validate_template(
    pdf: bytes,
    profile: TemplateProfile = SUPPORTED_TEMPLATE,
) -> ValidatedTemplate:
    digest = sha256(pdf).hexdigest()
    if digest != profile.sha256:
        raise InvalidAA912Template(
            f"unsupported AA9/12 template fingerprint: {digest}; expected {profile.sha256}"
        )

    reader = PdfReader(BytesIO(pdf))
    if len(reader.pages) != profile.page_count:
        raise InvalidAA912Template(
            f"expected {profile.page_count} pages, got {len(reader.pages)}"
        )

    for page_number, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - profile.page_width) > 0.5 or abs(height - profile.page_height) > 0.5:
            raise InvalidAA912Template(
                f"unexpected page geometry on page {page_number}: {width:.3f}x{height:.3f}"
            )

    return ValidatedTemplate(profile=profile, pdf=pdf)
