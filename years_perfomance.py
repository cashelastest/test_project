from train_a import *
from sqlalchemy import func
import datetime
def get_credits_month_year(month,year):
    select_query = select(CreditsModel).where(func.extract('month', CreditsModel.issuance_date) == month,
                                              func.extract('year', CreditsModel.issuance_date) == year
                                              )
    with engine.begin() as conn:
        data = conn.execute(select_query)
    return data.fetchall()

def get_payments_month_year(month,year):
    select_query = select(PaymentModel).where(func.extract('month', PaymentModel.payment_date) == month,
                                              func.extract('year', PaymentModel.payment_date) == year
                                              )
    with engine.begin() as conn:
        data = conn.execute(select_query)
    return data.fetchall()
def get_plans_month_year(month,year):
    select_query = select(PlansModel).where(func.extract('month', PlansModel.period) == month,
                                              func.extract('year', PlansModel.period) == year
                                              )
    with engine.begin() as conn:
        data = conn.execute(select_query)
    return data.fetchall()

def get_credits_year(year):
    select_query = select(CreditsModel).where(func.extract('year', CreditsModel.issuance_date) == year)
    with engine.begin() as conn:
        data = conn.execute(select_query)
    return data.fetchall()
def get_payments_year(year):
    select_query = select(PaymentModel).where(func.extract('year', PaymentModel.payment_date) == year)
    with engine.begin() as conn:
        data = conn.execute(select_query)
    return data.fetchall()


def year_perf(year):
    result = {}

    year_credits = get_credits_year(year)
    year_credits_sum = sum(a[4] for a in year_credits)

    year_payments = get_payments_year(year)

    year_payments_sum = sum(payment[2] for payment in year_payments)


    for month in range(1,13):
        credits = get_credits_month_year(month,year)
        payments = get_payments_month_year(month,year)
        plans = get_plans_month_year(month,year)


        suma_vydach = sum(credit[4] for credit in credits)
        plan_vydach = [plan[1] for plan in plans if plan[2]==3]

        plan_zboru = [plan[1] for plan in plans if plan[2]==4]
        payment_sum = sum(payment[2] for payment in payments)


        month_name = datetime.datetime(2024, month,1).strftime("%B")
        try:
            result[month_name] = {
                "Місяць та рік": f"{month_name} {year}",
                "Кількість видач за місяць":len(credits),
                "Сума з плану по видачам за місяць": plan_vydach[0],
                "Сума видач за місяць": suma_vydach,
                "% виконання плану по збору за місяць":round(100*suma_vydach/plan_vydach[0],2),
                "Кількість платежів на місяць":len(payments),
                "Сума з плану по збору за місяць":plan_zboru[0],
                "Сума платежів намісяць":payment_sum,
                "% Виконання плану по збору":round(100*payment_sum/plan_zboru[0]),
                "% суми видач за місяць від суми видач за рік ": round(100*suma_vydach/year_credits_sum,2),
                "% суми платежів за місяць від суми платежів за рік":round(100*payment_sum/year_payments_sum,2)

            }
        except Exception as e:
            print(e)
            return {"ERROR": "Такого року не існує в нашій базі данних"}
    return result