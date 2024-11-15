from fastapi import FastAPI, UploadFile
import datetime
from train_a import get_credits
from train_excel import download_plans
from payments import get_payments_by_credit,get_body_percent_payments
import shutil
import os
from plans_perfomance import plans_perfomance
from years_perfomance import year_perf
app = FastAPI()


@app.get("/")
def home():
    return {"hello":"world"}

@app.get("/user_credits/{user_id}/")
def plan(user_id):
    credits = get_credits(user_id = user_id)
    print(len(credits))
    response = {}
    
    for credit in credits:
        answer = [credit[1], True if credit[3] else False]

        info = op(credit)
        answer.append(info)
        response[credit.id] = answer


    return response if response else "Credits not Found"

def op(credit):

    info= {}
    if credit[3]:

        info['Дата повернення кредиту'] = credit[3]
        info["Сума видачі"] = credit[4]
        info["Нараховані відсотки"] = credit[5]
        payments = get_payments_by_credit(credit[6])

        payments = sum([a[2] for a in payments])
        

        info["Сума платежів за кредитом"] = payments
        
    else:
        info["Крайня дата повернення кредиту"] = credit[2]
        today = datetime.date.today()
        print(credit[2])
        delta = today - credit[2]
        info['Кількість днів прострочення кредиту'] = delta.days
        info["Сума видачі"] = credit[4]
        info["Нараховані відсотки"] = credit[5]

        body_payments, percent_payments = get_body_percent_payments(credit[6])
        info["Сума платежів по тілу"] = round(body_payments,3)
        info["Сума платежів по відсоткам"] = percent_payments
    return info

@app.post("/plans_insert")
def create_upload_file(file:UploadFile):
    if not os.path.exists("files"):
        os.makedirs("files")

    file_location = f"files/{file.filename}"
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        print(e)
        return e
    
    
    return download_plans(file_location)


@app.post("/plans_perfomance")
def plan_perfomance(date:datetime.date):
    result = plans_perfomance(date)
    if result =={}:
        return {"ERROR":"Ми нічого не знайшли"}
    return result

@app.post("/year_performance")
def year_perfomance(year):
    return year_perf(year)