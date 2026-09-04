from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

_templates = Jinja2Templates(directory=Path(__file__).parent / "web" / "templates")


def create_app() -> FastAPI:
    app = FastAPI(title="Forfettario AI", docs_url=None, redoc_url=None)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request) -> HTMLResponse:
        return _templates.TemplateResponse(request, "index.html")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
