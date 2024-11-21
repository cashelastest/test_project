import datetime
from fastapi import APIRouter

from sqlalchemy import func
from fastapi import HTTPException

from models.credit import CreditsModel
from models.payment import PaymentModel
from db.db_connector import session
from services.plan import get_plans_by_year
from utils.utils import filter_by_month, safe_percent_counting



year_router = APIRouter(prefix="/year_performance", tags=["/year_perfomance"])


def get_credits_and_payments_in_year(year:int):
    """
    Дістає з бази даних кредити та платежі за рік
    Args:
            year: рік, за який хочуть отримати платежі та кредити
    """
    return (
        session.query(PaymentModel, CreditsModel)
        .join(CreditsModel)
        .filter(
            func.extract('year', PaymentModel.payment_date) == year,
            func.extract("year", CreditsModel.return_date) == year,)
    ).all()


@year_router.post("/")
def year_perf(year:int):
    """
    збирає дані, перевіряє їх та робить з них звіт за вказаний рік
    Args:
            year: рік, за який хочуть отримати платежі та кредити
    """
    
    result={}
    credits_and_payments = get_credits_and_payments_in_year(year)

    year_payments = [payment[0] for payment in credits_and_payments]
    year_credits = [credit[1] for credit in credits_and_payments]

    plans = get_plans_by_year(year)
    year_plans = [plan for plan in plans]

    year_credits_sum = sum(credit.body for credit in year_credits)
    year_payments_sum = sum(payment.sum for payment in year_payments)

    if year_credits_sum==0 and year_payments_sum==0:
        raise HTTPException(404, detail="Рік ще не занесений в базу даних")
    for month in range(1, 13):

        credits = filter_by_month(year_credits, "issuance_date", month)
        payments = filter_by_month(year_payments, "payment_date", month)

        plans = filter_by_month(year_plans, "period", month)
        suma_vydach = sum(
            credit.body for credit in credits
            if credit.body is not None
            )
        payment_sum = sum(
            payment.sum for payment in payments
            if payment.sum is not None
            )          
        plan_vydach = [
            plan.sum for plan in plans 
            if plan.category_id == 3
            and plan.sum is not None
            ]
        plan_zboru = [
            plan.sum for plan in plans 
            if plan.category_id == 4
              and plan.sum is not None
              ]
        plan_vydach_value = plan_vydach[0] if plan_vydach else 0
        plan_zboru_value = plan_zboru[0] if plan_zboru else 0

        done_percent =safe_percent_counting(suma_vydach,plan_vydach_value)
        zbir_percent = safe_percent_counting(payment_sum,plan_zboru_value)

        vydach_percent = safe_percent_counting(suma_vydach,year_credits_sum)
        payment_percent = safe_percent_counting(payment_sum,year_payments_sum)

        try:
            month_name = datetime.datetime(2024, month, 1).strftime("%B")
            result[month_name] = {
                "Місяць та рік": f"{month_name} {year}",
                "Кількість видач за місяць": len(credits),
                "Сума з плану по видачам за місяць": plan_vydach_value,
                "Сума видач за місяць": suma_vydach,
                "% виконання плану по збору за місяць": done_percent,
                "Кількість платежів на місяць": len(payments),
                "Сума з плану по збору за місяць": plan_zboru_value,
                "Сума платежів намісяць": payment_sum,
                "% Виконання плану по збору": zbir_percent,
                "% суми видач за місяць від суми видач за рік": vydach_percent,
                "% суми платежів за місяць від суми платежів за рік": payment_percent
            }
        except Exception as e:
            print(f"Помилка при обробці даних за місяць {month}: {str(e)}")
            return {"Error": f"Виникла технічна помилка при створенні звіту за місяць {month}: {str(e)}"}
        
    return result