from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"This is": "your life"}


@app.get("/income/{income}")
def read_income(income: int, q: Optional[str] = None):
    return {"income": income,
        "income class": income_class(income),
        "income percentile": income_percentile_range(income),
        "max_mortgage_payment": max_mortgage_payment(income),
        "max_debt_payment": max_debt_payment(income),
        "max_home_price": max_home_price(income),
        "max_car_payment": max_car_payment(income)
    }

def income_class(income):
    if income <= 40000:
        return "low"
    elif income > 40000 and income <= 120000:
        return "middle"
    elif income > 120000:
        return "high"

def income_percentile_range(income):
    # FROM https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h01ar.xlsx on 2021-02-07
    if income <= 28084:
        return "< 20th"
    elif income <= 53503:
        return "20th < income < 40th"
    elif income <= 86488:
        return "40th < income < 60th"
    elif income <= 142501:
        return "60th < income < 80th"
    elif income <=270002:
        return "80th < income < 95th"
    elif income < 270002:
        return "> 95th"

def max_mortgage_payment(income):
    return (income * 0.28) / 12

def max_debt_payment(income):
    return (income * 0.36) / 12

def max_home_price(income):
    max_payment = max_mortgage_payment(income)
    mir = 0.0275 / 12
    nmp = 12 * 30
    return max_payment * ((1+mir)**nmp-1) / (mir*(1+mir)**nmp)

def max_car_payment(income):
    return (income * 0.1) / 12