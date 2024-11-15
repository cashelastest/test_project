from train_a import *
from sqlalchemy import func
from datetime import datetime

def get_plan_by_month(month,year):
    select_query = select(PlansModel).where(
        func.extract('month',PlansModel.period) == month,
        func.extract('year', PlansModel.period) == year
        )
    with engine.begin() as conn:
        data = conn.execute(select_query).all()
    return data

def get_credits_for_period(start,end):
    select_query = select(CreditsModel).where(CreditsModel.issuance_date.between(start,end))
    with engine.begin() as conn:
        data = conn.execute(select_query).all()
    return data

def get_payments_for_period(start,end):
    select_query = select(PaymentModel).where(PaymentModel.payment_date.between(start,end))
    with engine.begin() as conn:
        data = conn.execute(select_query).all()
    return data

def get_category_by_id(id):
    select_query = select(DictionaryModel).where(DictionaryModel.id == id)
    with engine.begin() as conn:
        result = conn.execute(select_query).fetchone()
        if result is None:
            return None
        return result.name 
    

def plans_perfomance(date):
    month,year = date.month,date.year
    month_name = datetime(2024, month,1).strftime("%B")
    plans = get_plan_by_month(month,year)
    
    results = {}
    for plan in plans:
        if plan[2] == 3:
            msg = "Сума видаих кредитів"
            credits = get_credits_for_period(plan[0],date)
            suma = sum(a[4] for a in credits)
            category = get_category_by_id(plan[3])



            print(suma)

        elif plan[2] ==4:
            msg = "Сума платежів"
            payments = get_payments_for_period(plan[0],date)
            
            suma = sum(a[2] for a in payments)
            print(suma)
        category = get_category_by_id(plan[2])
        done_percent=round((suma/plan[1])*100, 2)
       
        results[plan[3]]={
            "Місяць плану": month_name,
            "Категорія плану":category,
            "Сума з плану":plan[1],
            msg:suma,
            "% Виконання плану":done_percent

        
        }
    return results




today = datetime(2021, 1, 17)
plans_perfomance(today)