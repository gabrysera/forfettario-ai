from argparse import ArgumentParser
from pathlib import Path

from app.documents.aa912 import validate_template

_DEFAULT_DESTINATION = Path("data/templates/aa912.pdf")


def main() -> None:
    parser = ArgumentParser(description="Install the supported official AA9/12 PDF template.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--destination", type=Path, default=_DEFAULT_DESTINATION)
    args = parser.parse_args()

    pdf = args.source.read_bytes()
    validate_template(pdf)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_bytes(pdf)


if __name__ == "__main__":
    main()
