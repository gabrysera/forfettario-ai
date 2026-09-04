from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.tax_engine.types import Assessment, ConditionResult, ConditionStatus

REVENUE_LIMIT = Decimal("85000")
LABOR_COST_LIMIT = Decimal("20000")
EMPLOYMENT_INCOME_LIMIT = Decimal("35000")


class ForfettarioFacts(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    previous_year_revenue: Decimal | None = Field(default=None, ge=0)
    previous_year_labor_costs: Decimal | None = Field(default=None, ge=0)
    uses_special_vat_or_income_regime: bool | None = None
    italian_tax_resident: bool | None = None
    prevalently_sells_real_estate_land_or_new_vehicles: bool | None = None
    participates_in_partnership_association_or_family_business: bool | None = None
    controls_related_limited_company: bool | None = None
    works_prevalently_for_current_or_recent_employer: bool | None = None
    previous_year_employment_income: Decimal | None = Field(default=None, ge=0)
    employment_relationship_ended: bool | None = None


class StartupRateFacts(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    professional_business_activity_in_previous_three_years: bool | None = None
    mere_continuation_of_previous_employment_or_self_employment: bool | None = None
    continues_activity_previously_run_by_another_person: bool | None = None
    predecessor_previous_year_revenue: Decimal | None = Field(default=None, ge=0)


def assess_forfettario_access(facts: ForfettarioFacts) -> Assessment:
    return Assessment(
        conditions=(
            _max_amount(
                "FORF-ACCESS-001", facts.previous_year_revenue, REVENUE_LIMIT, "LAW190-C54"
            ),
            _max_amount(
                "FORF-ACCESS-002",
                facts.previous_year_labor_costs,
                LABOR_COST_LIMIT,
                "LAW190-C54",
            ),
            _must_be_false(
                "FORF-EXCL-001",
                facts.uses_special_vat_or_income_regime,
                "LAW190-C57-A",
            ),
            _supported_residency(facts.italian_tax_resident),
            _must_be_false(
                "FORF-EXCL-003",
                facts.prevalently_sells_real_estate_land_or_new_vehicles,
                "LAW190-C57-C",
            ),
            _must_be_false(
                "FORF-EXCL-004",
                facts.participates_in_partnership_association_or_family_business,
                "LAW190-C57-D",
            ),
            _must_be_false(
                "FORF-EXCL-005",
                facts.controls_related_limited_company,
                "LAW190-C57-D",
            ),
            _must_be_false(
                "FORF-EXCL-006",
                facts.works_prevalently_for_current_or_recent_employer,
                "LAW190-C57-DBIS",
            ),
            _employment_income_condition(facts),
        )
    )


def assess_startup_rate(facts: StartupRateFacts) -> Assessment:
    return Assessment(
        conditions=(
            _must_be_false(
                "FORF-STARTUP-001",
                facts.professional_business_activity_in_previous_three_years,
                "LAW190-C65-A",
            ),
            _must_be_false(
                "FORF-STARTUP-002",
                facts.mere_continuation_of_previous_employment_or_self_employment,
                "LAW190-C65-B",
            ),
            _predecessor_revenue_condition(facts),
        )
    )


def _max_amount(
    condition_id: str,
    amount: Decimal | None,
    limit: Decimal,
    source_id: str,
) -> ConditionResult:
    if amount is None:
        status = ConditionStatus.UNKNOWN
    else:
        status = ConditionStatus.PASS if amount <= limit else ConditionStatus.FAIL
    return ConditionResult(condition_id, status, (source_id,))


def _must_be_false(condition_id: str, value: bool | None, source_id: str) -> ConditionResult:
    if value is None:
        status = ConditionStatus.UNKNOWN
    else:
        status = ConditionStatus.PASS if not value else ConditionStatus.FAIL
    return ConditionResult(condition_id, status, (source_id,))


def _supported_residency(value: bool | None) -> ConditionResult:
    status = ConditionStatus.PASS if value is True else ConditionStatus.UNKNOWN
    return ConditionResult("FORF-EXCL-002", status, ("LAW190-C57-B",))


def _employment_income_condition(facts: ForfettarioFacts) -> ConditionResult:
    source_ids = ("LAW190-C57-DTER", "LAW207-2024-C12")
    if facts.employment_relationship_ended is True:
        return ConditionResult("FORF-EXCL-007", ConditionStatus.PASS, source_ids)
    if facts.employment_relationship_ended is None or facts.previous_year_employment_income is None:
        return ConditionResult("FORF-EXCL-007", ConditionStatus.UNKNOWN, source_ids)
    status = (
        ConditionStatus.PASS
        if facts.previous_year_employment_income <= EMPLOYMENT_INCOME_LIMIT
        else ConditionStatus.FAIL
    )
    return ConditionResult("FORF-EXCL-007", status, source_ids)


def _predecessor_revenue_condition(facts: StartupRateFacts) -> ConditionResult:
    if facts.continues_activity_previously_run_by_another_person is False:
        status = ConditionStatus.PASS
    elif (
        facts.continues_activity_previously_run_by_another_person is None
        or facts.predecessor_previous_year_revenue is None
    ):
        status = ConditionStatus.UNKNOWN
    else:
        status = (
            ConditionStatus.PASS
            if facts.predecessor_previous_year_revenue <= REVENUE_LIMIT
            else ConditionStatus.FAIL
        )
    return ConditionResult("FORF-STARTUP-003", status, ("LAW190-C65-C",))
