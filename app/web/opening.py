import os
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from app.documents.aa912 import build_aa912_draft, render_aa912, validate_template
from app.documents.aa912.models import AA912OpeningProfile
from app.documents.aa912.renderer import DocumentOverflowError
from app.documents.aa912.template import InvalidAA912Template
from app.tax_engine.forfettario_2026 import ForfettarioFacts, assess_forfettario_access
from app.tax_engine.types import ConditionStatus
from app.web.templates import templates

router = APIRouter()
_DEFAULT_TEMPLATE_PATH = Path("data/templates/aa912.pdf")
_CONDITION_LABELS = {
    "FORF-ACCESS-001": "ricavi o compensi dell'anno precedente",
    "FORF-ACCESS-002": "spese per lavoro dell'anno precedente",
    "FORF-EXCL-001": "eventuali regimi IVA o reddituali speciali",
    "FORF-EXCL-002": "residenza fiscale",
    "FORF-EXCL-003": "cessioni prevalenti di immobili, terreni o veicoli nuovi",
    "FORF-EXCL-004": "partecipazioni in società, associazioni o imprese familiari",
    "FORF-EXCL-005": "controllo di società collegate all'attività",
    "FORF-EXCL-006": "attività prevalente verso datore di lavoro attuale o recente",
    "FORF-EXCL-007": "redditi da lavoro dipendente dell'anno precedente",
}


class InvalidFormData(ValueError):
    pass


class UnsupportedOpeningCase(ValueError):
    pass


@router.get("/opening", response_class=HTMLResponse)
async def opening_form(request: Request) -> Response:
    return _form_response(request, values={})


@router.post("/opening/aa912.pdf")
async def generate_aa912(request: Request) -> Response:
    form = await request.form()
    values = {key: str(value) for key, value in form.items()}

    try:
        _require_supported_opening(values)
        profile = AA912OpeningProfile.model_validate(_profile_values(values))
        template = validate_template(_template_path().read_bytes())
        pdf = render_aa912(template, build_aa912_draft(profile))
    except InvalidFormData:
        return _form_response(request, values, "Completa tutti i campi richiesti.", 422)
    except UnsupportedOpeningCase as exc:
        return _form_response(request, values, str(exc), 422)
    except ValidationError as exc:
        return _form_response(request, values, _validation_message(exc), 422)
    except (FileNotFoundError, InvalidAA912Template):
        return _form_response(
            request,
            values,
            "Il modello AA9/12 ufficiale non è disponibile o non è la versione supportata.",
            503,
        )
    except DocumentOverflowError:
        return _form_response(
            request,
            values,
            "Un dato non entra nel relativo campo AA9/12. Controlla i dati inseriti.",
            422,
        )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="aa9-12-da-controllare.pdf"'},
    )


def _require_supported_opening(values: dict[str, str]) -> None:
    if not _required_bool(values, "confirms_software_activity"):
        raise UnsupportedOpeningCase(
            "La v0 automatica supporta solo l'attività prevalente di programmazione software. "
            "Il PDF non è stato generato."
        )

    facts = ForfettarioFacts.model_validate(
        {
            "previous_year_revenue": _required(values, "previous_year_revenue"),
            "previous_year_labor_costs": _required(values, "previous_year_labor_costs"),
            "uses_special_vat_or_income_regime": _required_bool(
                values, "uses_special_vat_or_income_regime"
            ),
            "italian_tax_resident": _required_bool(values, "italian_tax_resident"),
            "prevalently_sells_real_estate_land_or_new_vehicles": _required_bool(
                values, "prevalently_sells_real_estate_land_or_new_vehicles"
            ),
            "participates_in_partnership_association_or_family_business": _required_bool(
                values, "participates_in_partnership_association_or_family_business"
            ),
            "controls_related_limited_company": _required_bool(
                values, "controls_related_limited_company"
            ),
            "works_prevalently_for_current_or_recent_employer": _required_bool(
                values, "works_prevalently_for_current_or_recent_employer"
            ),
            "previous_year_employment_income": _required(
                values, "previous_year_employment_income"
            ),
            "employment_relationship_ended": _required_bool(
                values, "employment_relationship_ended"
            ),
        }
    )
    assessment = assess_forfettario_access(facts)
    if assessment.eligible is True:
        return

    issues = [
        _CONDITION_LABELS.get(condition.condition_id, condition.condition_id)
        for condition in assessment.conditions
        if condition.status is not ConditionStatus.PASS
    ]
    details = ", ".join(issues)
    raise UnsupportedOpeningCase(
        "Le risposte non permettono di validare automaticamente l'accesso al regime forfettario. "
        f"Da verificare: {details}. Il PDF non è stato generato."
    )


def _profile_values(values: dict[str, str]) -> dict[str, object]:
    activity_at_residence = _required_bool(values, "activity_at_residence")
    wants_vies = _required_bool(values, "wants_vies")
    tenure = _required(values, "property_tenure")

    activity_address = None
    if not activity_at_residence:
        activity_address = {
            "address": _required(values, "activity_address"),
            "postal_code": _required(values, "activity_postal_code"),
            "municipality": _required(values, "activity_municipality"),
            "province": _required(values, "activity_province"),
        }

    property_values: dict[str, object] = {
        "tenure": tenure,
        "cadastre_type": _required(values, "cadastre_type"),
        "section": _optional(values, "cadastre_section"),
        "sheet": _required(values, "cadastre_sheet"),
        "parcel": _required(values, "cadastre_parcel"),
        "subunit": _optional(values, "cadastre_subunit"),
    }
    if tenure == "D":
        property_values.update(
            contract_registration_date=_required(values, "contract_registration_date"),
            contract_registration_office=_required(values, "contract_registration_office"),
            contract_registration_number=_required(values, "contract_registration_number"),
            contract_registration_subnumber=_optional(values, "contract_registration_subnumber"),
            contract_registration_series=_optional(values, "contract_registration_series"),
        )

    intra_eu: dict[str, object] = {"wants_vies": wants_vies}
    if wants_vies:
        intra_eu.update(
            expected_purchases=_required(values, "expected_eu_purchases"),
            expected_sales=_required(values, "expected_eu_sales"),
        )

    return {
        "fiscal_code": _required(values, "fiscal_code"),
        "surname": _required(values, "surname"),
        "given_name": _required(values, "given_name"),
        "birth_date": _required(values, "birth_date"),
        "birth_municipality": _required(values, "birth_municipality"),
        "birth_province": _required(values, "birth_province"),
        "residence": {
            "address": _required(values, "residence_address"),
            "postal_code": _required(values, "residence_postal_code"),
            "municipality": _required(values, "residence_municipality"),
            "province": _required(values, "residence_province"),
        },
        "activity_at_residence": activity_at_residence,
        "activity_address": activity_address,
        "records_at_activity_address": _required_bool(values, "records_at_activity_address"),
        "start_date": _required(values, "start_date"),
        "declaration_date": _optional(values, "declaration_date"),
        "email": _required(values, "email"),
        "phone_prefix": _required(values, "phone_prefix"),
        "phone_number": _required(values, "phone_number"),
        "fax_prefix": _optional(values, "fax_prefix"),
        "fax_number": _optional(values, "fax_number"),
        "website": _optional(values, "website"),
        "activity_property": property_values,
        "intra_eu": intra_eu,
    }


def _form_response(
    request: Request,
    values: dict[str, str],
    error: str | None = None,
    status_code: int = 200,
) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="opening.html",
        context={"today": date.today().isoformat(), "error": error, "values": values},
        status_code=status_code,
    )


def _template_path() -> Path:
    configured = os.environ.get("AA912_TEMPLATE_PATH")
    return Path(configured) if configured else _DEFAULT_TEMPLATE_PATH


def _required(values: dict[str, str], field: str) -> str:
    value = values.get(field, "").strip()
    if not value:
        raise InvalidFormData(field)
    return value


def _optional(values: dict[str, str], field: str) -> str | None:
    return values.get(field, "").strip() or None


def _required_bool(values: dict[str, str], field: str) -> bool:
    value = _required(values, field)
    if value not in {"yes", "no"}:
        raise InvalidFormData(field)
    return value == "yes"


def _validation_message(exc: ValidationError) -> str:
    field = ".".join(str(part) for part in exc.errors()[0]["loc"])
    messages = {
        "previous_year_revenue": "Controlla ricavi o compensi dell'anno precedente.",
        "previous_year_labor_costs": "Controlla le spese per lavoro dell'anno precedente.",
        "previous_year_employment_income": (
            "Controlla il reddito da lavoro dipendente dell'anno precedente."
        ),
        "fiscal_code": "Controlla il codice fiscale.",
        "birth_province": "Controlla la provincia di nascita.",
        "residence.postal_code": "Inserisci un CAP di 5 cifre.",
        "residence.province": "Controlla la provincia di residenza.",
        "activity_address.postal_code": "Inserisci un CAP di 5 cifre per il luogo di lavoro.",
        "activity_address.province": "Controlla la provincia del luogo di lavoro.",
        "records_at_activity_address": (
            "La v0 automatica supporta solo la documentazione fiscale conservata nel luogo "
            "dell'attività. Questo caso richiede un percorso più completo."
        ),
        "email": "Controlla l'indirizzo email.",
        "intra_eu": "Controlla i dati relativi alle operazioni con altri Paesi UE.",
        "activity_property": "Controlla i dati dell'immobile e, se applicabile, del contratto.",
    }
    return messages.get(field, "Controlla i dati inseriti nei campi evidenziati.")
