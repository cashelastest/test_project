from fastapi import HTTPException, APIRouter, UploadFile
import pandas as pd
from services.plan import get_plan_by_month,insert_xl_plans
from services.payment import get_payments_for_period
from services.credit import get_credits_for_period
from services.dictionary import get_category
from utils.plans_excel import get_plans_from_excel, check_data
from datetime import date,datetime
import io


plans_router = APIRouter(
    prefix="/plans",tags=["/plans"]
)

@plans_router.post("_insert/")
async def create_upload_file(file:UploadFile):
    """
    Проводить перевірку планів з книги, записує та за наявності помилок - повертає їх
    Args:
            file: Excel file з колонками (місяць плану, назва категорії плану, сума)
    """
 
    if not file.filename.endswith((".xls", ".xlsm", ".xlsx")):
        raise HTTPException(status_code=404, detail= "Неправильний формат файлу. Дозволені типи: .xlsx, .xls, .xlsm")
    contents = await file.read()
    data = pd.read_excel(io.BytesIO(contents))
    plans = get_plans_from_excel(data)
    passed = check_data(plans)
    if passed == True:
        return insert_xl_plans(plans)
    else:
        return passed


@plans_router.post("_perfomance/")
def plans_perfomance(date:date):
    """
    Повертає звіт про виконання планів
    за період з першого числа до введеної дати
    Args:
            date:дата за яку хочемо передивитись плани
    """
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
        category = get_category("name", plan.category_id)
        done_percent=round((suma/plan.sum)*100, 2)
        results[plan.id]={
            "Місяць плану": month_name,
            "Категорія плану":category,
            "Сума з плану":plan.sum,
            msg:suma,
            "% Виконання плану":done_percent
        }
    if results =={}:
        raise HTTPException(status_code=404, detail= "Планів за цей період не знайдено")
    return results
