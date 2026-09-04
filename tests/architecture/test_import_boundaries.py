import ast
from pathlib import Path

CORE_BOUNDARIES = {
    Path("app/domain"): {
        "app.ai",
        "app.documents",
        "app.storage",
        "app.tax_engine",
        "app.web",
        "azure",
        "fastapi",
        "openai",
    },
    Path("app/tax_engine"): {
        "app.ai",
        "app.documents",
        "app.storage",
        "app.web",
        "azure",
        "fastapi",
        "openai",
    },
    Path("app/documents"): {
        "app.ai",
        "app.storage",
        "app.web",
        "azure",
        "fastapi",
        "openai",
    },
}


def test_core_modules_keep_infrastructure_out() -> None:
    violations: list[str] = []

    for root, forbidden_prefixes in CORE_BOUNDARIES.items():
        for path in root.rglob("*.py"):
            for imported in _imports(path):
                if any(_matches(imported, prefix) for prefix in forbidden_prefixes):
                    violations.append(f"{path}: forbidden import {imported}")

    assert not violations, "\n".join(violations)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _matches(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(f"{prefix}.")
