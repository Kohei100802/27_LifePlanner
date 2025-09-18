from __future__ import annotations
from pydantic import BaseModel, Field


class Step1(BaseModel):
    name: str = Field(min_length=1)
    family: str | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    birth_day: int | None = None


class Step2(BaseModel):
    main_annual_income: float = Field(ge=0)
    spouse_annual_income: float | None = Field(default=0, ge=0)


class Step3(BaseModel):
    living_monthly: float = Field(ge=0)
    housing_monthly: float = Field(ge=0)
    insurance_monthly: float = Field(ge=0)
    education_monthly: float = Field(ge=0)
    others_monthly: float = Field(ge=0)


class Step4(BaseModel):
    savings: float = Field(ge=0)
    investments: float = Field(ge=0)
    real_estate_value: float = Field(ge=0)
    mortgage_balance: float = Field(ge=0)
    other_loans: float = Field(ge=0)


class Step5(BaseModel):
    big_plans: str | None = None


class Step6(BaseModel):
    return_rate: float = Field(ge=-10, le=50, default=3.0)
    pension_annual: float = Field(ge=0, default=0)
    use_nisa: bool = False
    use_ideco: bool = False
    inflation_rate: float = Field(ge=-10, le=50, default=1.0)
    tax_rate: float = Field(ge=0, le=55, default=20.0)
