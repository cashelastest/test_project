from models import session,CreditsModel,PaymentModel,PlansModel
from sqlalchemy import func,select
import datetime
def get_credits_month_year(month,year):
    """Повертає усі кредити за обраний місяць"""
    select_query = select(CreditsModel).where(func.extract('month', CreditsModel.issuance_date) == month,
                                              func.extract('year', CreditsModel.issuance_date) == year
                                              )
    return session.execute(select_query).scalars().all()

def get_payments_month_year(month,year):
    """Повертає усі платежі за обраний місяць"""
    select_query = select(PaymentModel).where(func.extract('month', PaymentModel.payment_date) == month,
                                              func.extract('year', PaymentModel.payment_date) == year
                                              )
    return session.execute(select_query).scalars().all()

def get_plans_month_year(month,year):
    """Повертає усі плани за обраний місяць"""
    select_query = select(PlansModel).where(func.extract('month', PlansModel.period) == month,
                                              func.extract('year', PlansModel.period) == year
                                              )
    return session.execute(select_query).scalars().all()

def get_credits_year(year):
    """Повертає усі кредити за обраний рік"""
    select_query = select(CreditsModel).where(func.extract('year', CreditsModel.issuance_date) == year)
    return session.execute(select_query).scalars().all()
def get_payments_year(year):
    """Повертає усі платежі за рік"""
    select_query = select(PaymentModel).where(func.extract('year', PaymentModel.payment_date) == year)
    return session.execute(select_query).scalars().all()

def year_perf(year):
    """бере усі дані, валідує їх та робить з них звіт за вказаний рік"""
    result = {}

    year_credits = get_credits_year(year)
    year_credits_sum = sum(credit.body for credit in year_credits)

    year_payments = get_payments_year(year)
    year_payments_sum = sum(payment.sum for payment in year_payments)
    if year_credits_sum ==0 and year_payments_sum==0:
        return {"Error":"Такого року нема в базі данних"}

    year_credits_sum = sum(credit.body for credit in year_credits if credit.body is not None)
    year_payments_sum = sum(payment.sum for payment in year_payments if payment.sum is not None)

    for month in range(1, 13):
        try:
            credits = get_credits_month_year(month, year)
            payments = get_payments_month_year(month, year)
            plans = get_plans_month_year(month, year)
            
            
            suma_vydach = sum(credit.body for credit in credits if credit.body is not None)
            payment_sum = sum(payment.sum for payment in payments if payment.sum is not None)
            
            plan_vydach = [plan.sum for plan in plans if plan.category_id == 3 and plan.sum is not None]
            plan_zboru = [plan.sum for plan in plans if plan.category_id == 4 and plan.sum is not None]
            
            
            plan_vydach_value = plan_vydach[0] if plan_vydach else 0
            plan_zboru_value = plan_zboru[0] if plan_zboru else 0
            
            
            done_percent = round(100 * suma_vydach / plan_vydach_value, 2) if plan_vydach_value != 0 else 0
            zbir_percent = round(100 * payment_sum / plan_zboru_value, 2) if plan_zboru_value != 0 else 0
            
            
            vydach_percent = round(100 * suma_vydach / year_credits_sum, 2) if year_credits_sum != 0 else 0
            payment_percent = round(100 * payment_sum / year_payments_sum, 2) if year_payments_sum != 0 else 0
            
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