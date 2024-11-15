from train_a import *


def insert_plans():
    data = get_from_csv("plans.csv")
    for plan in data:
        insert_query = insert(PlansModel).values(
            period = parse_date(plan[1]),
            sum = float(plan[2]),
            category_id = int(plan[3])

        )

        with engine.begin() as conn:
            conn.execute(insert_query)


def get_category_by_name(name):
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
    for plan in plans:
        plan = plans[plan]
        insert_query = insert(PlansModel).values(
            period = plan["period"],
            sum = plan["sum"],
            category_id = plan["category_id"]
        )

        with engine.begin() as conn:
            conn.execute(insert_query)
    return True