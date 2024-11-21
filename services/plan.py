
from sqlalchemy import func
from models.plan import PlansModel
from db.db_connector import session

def get_plans_by_year(year:int):
    return (
        session.query(PlansModel)
        .filter(
            func.extract('year', PlansModel.period) == year,
        )
    ).all()


def check_plan(plan):
    data =session.query(PlansModel)\
    .filter(PlansModel.category_id == plan["category_id"],\
        PlansModel.period == plan["period"]).first()
    return data if data else None


def insert_xl_plans(plans):
    """Вставляє плани у базу даних"""
    for plan in plans:
        plan = plans[plan]
        insert_data = [PlansModel(
            period = plan["period"],
            sum = plan["sum"],
            category_id = plan["category_id"]
        ) for plan in plans.values()]
    session.add_all(insert_data)
    session.commit()
    return {"Success":"Плани успішно додані до бази данних"}


def get_plan_by_month(month,year):
    """Повертає плани за місяцем та роком"""
    return (session.query(PlansModel)
            .filter(func.extract("year", PlansModel.period)== year,
                    func.extract("month", PlansModel.period) == month
                    )
                )







