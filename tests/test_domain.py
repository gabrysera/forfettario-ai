from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain import ReviewStatus, TaxpayerProfile


def test_domain_models_reject_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        TaxpayerProfile.model_validate({"taxpayer_id": uuid4(), "unexpected": True})


def test_review_status_values_are_stable() -> None:
    assert ReviewStatus.UNSUPPORTED == "UNSUPPORTED"
