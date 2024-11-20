from fastapi import HTTPException, APIRouter, UploadFile
import os 
import shutil
from utils.plans_excel import download_plans
from services.plan import get_plan_by_month,get_credits_for_period,get_payments_for_period,get_category_by_id
from datetime import date,datetime
plans_router = APIRouter(
    prefix="/plans",tags=["plans"]
)

@plans_router.post("_insert")
def create_upload_file(file:UploadFile):
    if not os.path.exists("files"):
        os.makedirs("files")

    file_location = f"files/{file.filename}"
    if not file.filename.endswith((".xls", ".xlsm", ".xlsx")):
        raise HTTPException(status_code=404, detail= "Неправильний формат файлу. Дозволені типи: .xlsx, .xls, .xlsm")
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail= "Помилка при завантаженні файла. Спробуйте інший")
    
    return download_plans(file_location)




@plans_router.post("_perfomance/")
def plans_perfomance(date:date):
    """Повертає інфу про виконання планів за період"""
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
        category = get_category_by_id(plan.category_id)
        done_percent=round((suma/plan.sum)*100, 2)
       
        results[plan.id]={
            "Місяць плану": month_name,
            "Категорія плану":category.name,
            "Сума з плану":plan.sum,
            msg:suma,
            "% Виконання плану":done_percent
        }
    if results =={}:
        raise HTTPException(status_code=404, detail= "Планів за цей період не знайдено")
    return results
