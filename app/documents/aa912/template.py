import os
from pathlib import Path

_DEFAULT_TEMPLATE = Path("var/templates/aa9_12.pdf")


class AA912TemplateNotInstalled(FileNotFoundError):
    pass


def load_aa912_template() -> bytes:
    """Load the administrator-installed official AA9/12 PDF template."""
    path = Path(os.environ.get("AA912_TEMPLATE_PATH", _DEFAULT_TEMPLATE))
    try:
        return path.read_bytes()
    except FileNotFoundError as exc:
        raise AA912TemplateNotInstalled(
            f"AA9/12 template not found at {path}. Install the official Agenzia delle Entrate PDF."
        ) from exc
