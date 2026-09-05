from datetime import date

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from starlette.datastructures import FormData

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
                "fiscal_code": values.get("fiscal_code"),
                "surname": values.get("surname"),
                "given_name": values.get("given_name"),
                "birth_date": values.get("birth_date"),
                "birth_municipality": values.get("birth_municipality"),
                "birth_province": values.get("birth_province"),
                "residence_address": values.get("residence_address"),
                "residence_postal_code": values.get("residence_postal_code"),
                "residence_municipality": values.get("residence_municipality"),
                "residence_province": values.get("residence_province"),
                "activity_at_residence": _checked(form, "activity_at_residence"),
                "activity_address": _optional(values, "activity_address"),
                "activity_postal_code": _optional(values, "activity_postal_code"),
                "activity_municipality": _optional(values, "activity_municipality"),
                "activity_province": _optional(values, "activity_province"),
                "accounting_records_at_activity_address": _checked(
                    form, "accounting_records_at_activity_address"
                ),
                "start_date": values.get("start_date"),
                "declaration_date": _optional(values, "declaration_date"),
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


def _checked(form: FormData, field: str) -> bool:
    return form.get(field) == "on"


def _optional(values: dict[str, str], field: str) -> str | None:
    return values.get(field) or None


def _validation_message(exc: ValidationError) -> str:
    first = exc.errors()[0]
    location = ".".join(str(part) for part in first["loc"])
    return f"{location}: {first['msg']}"
