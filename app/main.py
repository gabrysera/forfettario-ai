from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from app.web.opening import router as opening_router
from app.web.templates import templates


def create_app() -> FastAPI:
    app = FastAPI(title="Forfettario AI", docs_url=None, redoc_url=None)
    app.include_router(opening_router)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request) -> Response:
        return templates.TemplateResponse(request=request, name="index.html")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
