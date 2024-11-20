
from sqlalchemy import func, select,insert
from models.plan import PlansModel
from models.dictionary import DictionaryModel
from models.payment import PaymentModel
from models.credit import CreditsModel
from db.db_connector import session,engine
from datetime import datetime


def get_category_by_name(name):
    """Повертає id категорії операції з таблиці Dictionary"""
    select_query = select(DictionaryModel).where(DictionaryModel.name == name)
    with engine.begin() as conn:
        data = conn.execute(select_query)
        return data.fetchone()[1]
    


def check_plan(plan):
    print(plan)
    select_query = select(PlansModel).where((PlansModel.category_id == plan["category_id"]) & (PlansModel.period == plan["period"]))
    with engine.begin() as conn:
        data = conn.execute(select_query).first()

        return data is None
def insert_xl_plans(plans):
    """Вставляє плани у базу даних"""
    for plan in plans:
        plan = plans[plan]
        insert_query = insert(PlansModel).values(
            period = plan["period"],
            sum = plan["sum"],
            category_id = plan["category_id"]
        )

        with engine.begin() as conn:
            conn.execute(insert_query)
    return {"Success":"Плани успішно додані до бази данних"}




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
    

