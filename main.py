from fastapi import FastAPI, UploadFile,HTTPException
from datetime import datetime,date 
from models import get_credits
from excel import download_plans
from payments import get_payments_by_credit,get_body_percent_payments
import shutil
import os
from plans_perfomance import plans_perfomance
from years_perfomance import year_perf

app = FastAPI()


@app.get("/user_credits/{user_id}/")
def user_credits(user_id):

    credits = get_credits(user_id = user_id)
    if not credits:
        raise HTTPException(status_code=404, detail= "Кредитів для цього юзера не знайдено")
    response = {}
    
    for credit in credits:
        is_closed = credit.actual_return_date is not None
        answer = [credit.issuance_date, is_closed]

        info = get_info(credit)
        answer.append(info)
        response[credit.id] = answer


    return response 

def get_info(credit):
    """Повертає інформацію про кредит"""
    info= {}
    if credit.actual_return_date:

        info['Дата повернення кредиту'] = credit.actual_return_date
        info["Сума видачі"] = credit.body
        info["Нараховані відсотки"] = credit.percent
        payments = get_payments_by_credit(credit.id)

        payments = sum([payment.sum for payment in payments])
        

        info["Сума платежів за кредитом"] = payments
        
    else:
        info["Крайня дата повернення кредиту"] = credit.return_date
        today = datetime.date.today()
        print(credit.return_date)
        delta = today - credit.return_date
        info['Кількість днів прострочення кредиту'] = delta.days
        info["Сума видачі"] = credit.body
        info["Нараховані відсотки"] = credit.percent

        body_payments, percent_payments = get_body_percent_payments(credit.id)
        info["Сума платежів по тілу"] = round(body_payments,3)
        info["Сума платежів по відсоткам"] = percent_payments
    return info



@app.post("/plans_insert")
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


@app.post("/plans_perfomance")
def plan_perfomance(date:date):
    result = plans_perfomance(date)
    if result =={}:
        raise HTTPException(status_code=404, detail= "Планів за цей період не знайдено")
    return result

@app.post("/year_performance")
def year_perfomance(year:int):
    result = year_perf(year)
    if "Error" in result:
        raise HTTPException(status_code=404, detail= result['Error'])
    return result