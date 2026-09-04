import json
from pathlib import Path

import pytest

from app.tax_engine.forfettario_2026 import (
    ForfettarioFacts,
    StartupRateFacts,
    assess_forfettario_access,
    assess_startup_rate,
)
from app.tax_engine.types import Assessment, ConditionStatus


@pytest.mark.parametrize(
    ("revenue", "expected"),
    [("85000", True), ("85000.01", False)],
)
def test_revenue_limit_boundary(revenue: str, expected: bool) -> None:
    facts = _eligible_facts(previous_year_revenue=revenue)
    assert assess_forfettario_access(facts).eligible is expected


@pytest.mark.parametrize(
    ("labor_costs", "expected"),
    [("20000", True), ("20000.01", False)],
)
def test_labor_cost_limit_boundary(labor_costs: str, expected: bool) -> None:
    facts = _eligible_facts(previous_year_labor_costs=labor_costs)
    assert assess_forfettario_access(facts).eligible is expected


@pytest.mark.parametrize(
    ("employment_income", "expected"),
    [("35000", True), ("35000.01", False)],
)
def test_2026_employment_income_limit(employment_income: str, expected: bool) -> None:
    facts = _eligible_facts(previous_year_employment_income=employment_income)
    assert assess_forfettario_access(facts).eligible is expected


def test_employment_income_limit_is_irrelevant_after_employment_ends() -> None:
    facts = _eligible_facts(
        previous_year_employment_income="100000",
        employment_relationship_ended=True,
    )
    assert assess_forfettario_access(facts).eligible is True


def test_unknown_material_fact_prevents_positive_eligibility() -> None:
    facts = _eligible_facts(controls_related_limited_company=None)
    assessment = assess_forfettario_access(facts)
    assert assessment.eligible is None
    assert _status(assessment, "FORF-EXCL-005") is ConditionStatus.UNKNOWN


def test_nonresident_case_is_not_incorrectly_rejected() -> None:
    facts = _eligible_facts(italian_tax_resident=False)
    assessment = assess_forfettario_access(facts)
    assert assessment.eligible is None
    assert _status(assessment, "FORF-EXCL-002") is ConditionStatus.UNKNOWN


def test_startup_rate_happy_path() -> None:
    facts = StartupRateFacts(
        professional_business_activity_in_previous_three_years=False,
        mere_continuation_of_previous_employment_or_self_employment=False,
        continues_activity_previously_run_by_another_person=False,
    )
    assert assess_startup_rate(facts).eligible is True


def test_startup_rate_requires_predecessor_revenue_when_activity_is_continued() -> None:
    facts = StartupRateFacts(
        professional_business_activity_in_previous_three_years=False,
        mere_continuation_of_previous_employment_or_self_employment=False,
        continues_activity_previously_run_by_another_person=True,
    )
    assert assess_startup_rate(facts).eligible is None


def test_synthetic_golden_taxpayer() -> None:
    fixture = json.loads(
        (Path(__file__).parent / "golden" / "forfettario_developer_2026.json").read_text()
    )
    access = assess_forfettario_access(ForfettarioFacts.model_validate(fixture["access_facts"]))
    startup = assess_startup_rate(StartupRateFacts.model_validate(fixture["startup_facts"]))
    assert access.eligible is fixture["expected"]["forfettario_access"]
    assert startup.eligible is fixture["expected"]["startup_rate"]


def _eligible_facts(**overrides: object) -> ForfettarioFacts:
    values: dict[str, object] = {
        "previous_year_revenue": "0",
        "previous_year_labor_costs": "0",
        "uses_special_vat_or_income_regime": False,
        "italian_tax_resident": True,
        "prevalently_sells_real_estate_land_or_new_vehicles": False,
        "participates_in_partnership_association_or_family_business": False,
        "controls_related_limited_company": False,
        "works_prevalently_for_current_or_recent_employer": False,
        "previous_year_employment_income": "0",
        "employment_relationship_ended": False,
    }
    values.update(overrides)
    return ForfettarioFacts.model_validate(values)


def _status(assessment: Assessment, condition_id: str) -> ConditionStatus:
    return next(
        condition.status for condition in assessment.conditions if condition.condition_id == condition_id
    )
