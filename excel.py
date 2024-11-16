import openpyxl
from plans import get_category_by_name,check_plan,insert_xl_plans
from models import parse_date

def get_plans_from_excel(filename):
    """Дістає дані з основного листа надісланої книги"""
    try:
        book = openpyxl.open(f"{filename}", read_only=True)
    except Exception as e:
        print("Помилка при відкритті файлу")
        return {"Error": "Помилка при відкритті файлу"}

    sheet = book.active

    xl_plan = {}
    for row in range(1, sheet.max_row):
        category_id = get_category_by_name(sheet[row][1].value)

        xl_plan[row]={
        "period": parse_date(sheet[row][0].value),
        "category_id":category_id,
        "sum":sheet[row][2].value
        }
    return xl_plan
def check_data(plans):
    """перевіряє валідність даних, при помилці - повертає їх"""
    for plan in plans:
    
        if check_plan(plans[plan])==False:
            return f"Помилка: план з id:{plan} вже існує в базі даних"
        
        if plans[plan]["period"].day != 1:
            return f"Помилка: План з id: {plan} має неправильну дату\nвона має починатись з 1 числа"
        if plans[plan]["sum"] is None:
            return "Помилка: порожній стовпець sum"
    return True


def download_plans(filename):
    """приймає назву книги, парсить її, перевіряє данні та
      додає до бази данних.У разі помилки - повертає її
    """

    plans = get_plans_from_excel(filename)

    data = check_data(plans)

    if data == True:
        return insert_xl_plans(plans)
    else:
        return data
    
        
