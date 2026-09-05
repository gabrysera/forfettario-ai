import json
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from app.documents.aa912.models import AA912OpeningProfile
from app.documents.aa912.template import TemplateProfile, ValidatedTemplate

_GOLDEN_DIR = Path(__file__).parent / "golden"


def profile(name: str = "aa912_home_owned_no_vies.json") -> AA912OpeningProfile:
    data = json.loads((_GOLDEN_DIR / name).read_text())
    return AA912OpeningProfile.model_validate(data)


def synthetic_template(*, pagesize: tuple[float, float] = A4) -> tuple[bytes, TemplateProfile]:
    buffer = BytesIO()
    pdf = Canvas(buffer, pagesize=pagesize)
    for page_number in range(1, 6):
        pdf.drawString(20, 20, f"TEMPLATE PAGE {page_number}")
        pdf.showPage()
    pdf.save()
    content = buffer.getvalue()
    return content, TemplateProfile(
        template_id="synthetic-test-template",
        sha256=sha256(content).hexdigest(),
        source_url="https://example.test/aa912.pdf",
        page_count=5,
        page_width=float(pagesize[0]),
        page_height=float(pagesize[1]),
    )


def validated_synthetic_template() -> ValidatedTemplate:
    content, template_profile = synthetic_template()
    return ValidatedTemplate(template_profile, content)
