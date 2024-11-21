from fastapi import HTTPException
from services.plan import check_plan
from services.dictionary import get_category
from utils.utils import parse_date




def get_plans_from_excel(data):
    """Дістає дані з основного листа надісланої книги"""
    excel_plan = {}

    for id in data.index:
        try:
            category_name = data.loc[id, 'назва категорії плану']
        except Exception as e:
            print(f"Error in sheets name: {e}")
            raise HTTPException(status_code=404, detail="Неправильно названі колонки в листі. Мають бути: місяць плану, назва категорії плану, сума")
        category_id = get_category("id",category_name)
        month = data.loc[id, 'місяць плану']
        
        excel_plan[id] = {
            "period": parse_date(month),
            "category_id": category_id,
            "sum": float(data.loc[id, 'сума'])
        }
    return excel_plan


def check_data(plans):
    """перевіряє валідність даних, при помилці - повертає їх"""
    for plan in plans:

        is_in_database = check_plan(plans[plan])

        if is_in_database!=None:
            return f"Помилка: план з id:{plan} вже існує в базі даних"
        
        if plans[plan]["period"].day != 1:
            return f"Помилка: План з id: {plan} має неправильну дату\nвона має починатись з 1 числа"
        if plans[plan]["sum"] is None:
            return "Помилка: порожній стовпець sum"
    return True


