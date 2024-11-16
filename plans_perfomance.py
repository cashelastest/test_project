from models import CreditsModel,PaymentModel,DictionaryModel,PlansModel
from db_connector import session,engine 
from sqlalchemy import func,select
from datetime import datetime

def get_plan_by_month(month,year):
    """Повертає плани за місяцем та роком"""
    select_query = select(PlansModel).where(
        func.extract('month',PlansModel.period) == month,
        func.extract('year', PlansModel.period) == year
        )

    return session.execute(select_query).scalars().all()


def get_credits_for_period(start,end):
    """Повертає усі кредити за період"""
    select_query = select(CreditsModel).where(CreditsModel.issuance_date.between(start,end))
    return session.execute(select_query).scalars().all()


def get_payments_for_period(start,end):
    """Повертає усі платежі за період"""
    select_query = select(PaymentModel).where(PaymentModel.payment_date.between(start,end))
    with engine.begin() as conn:
        result = conn.execute(select_query)
        if not result:
            return None
    return result


def get_category_by_id(id):
    """Повертає назву категорії по її id"""

    select_query = select(DictionaryModel).where(DictionaryModel.id == id)
    return session.execute(select_query).scalars().first()
    

def plans_perfomance(date):
    """Повертає інфу про виконання планів за період"""
    month,year = date.month,date.year
    month_name = datetime(2024, month,1).strftime("%B")
    plans = get_plan_by_month(month,year)

    results = {}

    for plan in plans:
        if plan.category_id == 3:
            msg = "Сума видаих кредитів"
            credits = get_credits_for_period(plan.period,date)
            suma = sum(credit.body for credit in credits)


        elif plan.category_id ==4:
            msg = "Сума платежів"
            payments = get_payments_for_period(plan.period,date)
            suma = sum(payment.sum for payment in payments)
            print(suma)
        category = get_category_by_id(plan.category_id)
        done_percent=round((suma/plan.sum)*100, 2)
       
        results[plan.id]={
            "Місяць плану": month_name,
            "Категорія плану":category.name,
            "Сума з плану":plan.sum,
            msg:suma,
            "% Виконання плану":done_percent
        }

    return results
