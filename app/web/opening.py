from datetime import date

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from app.documents.aa912 import AA912OpeningData, render_aa912_opening
from app.documents.aa912.template import AA912TemplateNotInstalled, load_aa912_template
from app.web.templates import templates

router = APIRouter()


@router.get("/opening", response_class=HTMLResponse)
async def opening_form(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="opening.html",
        context={"today": date.today().isoformat(), "error": None, "values": {}},
    )


@router.post("/opening/aa912.pdf")
async def generate_aa912(request: Request) -> Response:
    form = await request.form()
    values = {key: str(value) for key, value in form.items()}

    try:
        data = AA912OpeningData.model_validate(
            {
                **values,
                "activity_at_residence": _checked(form, "activity_at_residence"),
                "accounting_records_at_activity_address": _checked(
                    form, "accounting_records_at_activity_address"
                ),
                "declaration_date": values.get("declaration_date") or None,
            }
        )
        pdf = render_aa912_opening(load_aa912_template(), data)
    except ValidationError as exc:
        return templates.TemplateResponse(
            request=request,
            name="opening.html",
            context={
                "today": date.today().isoformat(),
                "error": _validation_message(exc),
                "values": values,
            },
            status_code=422,
        )
    except AA912TemplateNotInstalled as exc:
        return Response(str(exc), status_code=503, media_type="text/plain")

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="aa9-12-bozza.pdf"'},
    )


def _checked(form: object, field: str) -> bool:
    return getattr(form, "get")(field) == "on"


def _validation_message(exc: ValidationError) -> str:
    first = exc.errors()[0]
    location = ".".join(str(part) for part in first["loc"])
    return f"{location}: {first['msg']}"
