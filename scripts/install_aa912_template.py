import shutil
import sys
from pathlib import Path

from pypdf import PdfReader

_TARGET = Path("var/templates/aa9_12.pdf")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python scripts/install_aa912_template.py /path/to/official-aa9-12.pdf"
        )

    source = Path(sys.argv[1])
    reader = PdfReader(source)
    if len(reader.pages) != 5:
        raise SystemExit(f"unexpected AA9/12 template: expected 5 pages, got {len(reader.pages)}")

    _TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, _TARGET)
    print(f"installed AA9/12 template at {_TARGET}")


if __name__ == "__main__":
    main()
