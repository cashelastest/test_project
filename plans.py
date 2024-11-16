from models import PlansModel,DictionaryModel
from db_connector import engine
from sqlalchemy import select,insert

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