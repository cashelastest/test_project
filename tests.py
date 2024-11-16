from fastapi.testclient import TestClient
from main import app
from models import DictionaryModel, UsersModel,BaseModel,PaymentModel,CreditsModel,PlansModel,parse_date,get_from_csv
from sqlalchemy import insert
from db_connector import test_engine,test_session
from datetime import datetime,date
import os
import pytest


client = TestClient(app)

BaseModel.metadata.create_all(test_engine)

def insert_dictionary():
    """переносить Dictionary зі csv до бд"""
    data = get_from_csv("dictionary.csv")
    for dictionary in data:
        insert_query = insert(DictionaryModel).values(
            name= dictionary[1]

        )
        test_session.execute(insert_query)
        test_session.commit()


def insert_payments():
    """переносить платежі з csv до бази данних"""
    data = get_from_csv("payments.csv")
    for payment in data:
        insert_query = insert(PaymentModel).values(
            sum=  float(payment[4]),
            payment_date = parse_date(payment[2]),
            credit_id = int(payment[1]),
            type_id = int(payment[3])
        )
        test_session.execute(insert_query)
        test_session.commit()


def insert_users():
    """переносить юзерів з csv до бази даних"""
    data = get_from_csv("users.csv")
    for user in data:
        parsed_date = datetime.strptime(user[2], "%d.%m.%Y")

        insert_query = insert(UsersModel).values(
            login = user[1],
            registration_date = parsed_date)
        
        test_session.execute(insert_query)
        test_session.commit()


def insert_credits():
    """переносить усі кредити з csv до бази даних"""
    data = get_from_csv("credits.csv")
    for credit in data:
        insert_query = insert(CreditsModel).values(
        user_id = int(credit[1]),
        issuance_date=parse_date(credit[2]),
        return_date=parse_date(credit[3]),
        actual_return_date=parse_date(credit[4]),
        body = int(credit[5]),
        percent = float(credit[6]))

        test_session.execute(insert_query)
        test_session.commit()


def insert_plans():
    """Переносить усі плани з csv до бази даних"""
    data = get_from_csv("plans.csv")
    for plan in data:
        insert_query = insert(PlansModel).values(
            period = parse_date(plan[1]),
            sum = float(plan[2]),
            category_id = int(plan[3]))
        test_session.execute(insert_query)
        test_session.commit()

def test_prepare_data():
    """Переносить дані з csv файлів до бази даних"""


    insert_users()
    insert_dictionary()
    insert_credits()
    insert_payments()
    insert_plans()
    assert True


def test_user_credits_not_found():
    """Тест перевіряє кредити неіснуючого користувача"""
    response = client.get("/user_credits/99999/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Кредитів для цього юзера не знайдено'}

def test_user_credits_valid():
    """перевіряє кредити існуючого користувача"""
    response = client.get("/user_credits/1/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_plans_insert_invalid_file():
    """перевіряє при завантаженні неправильного файла"""
    files = {"file": ("test.txt", "invalid content", "text/plain")}
    response = client.post("/plans_insert", files=files)
    assert response.status_code == 404


def test_plans_perfomance():
    """перевіряє чи видаються плани за датою"""
    test_date = date(2021, 1, 12)
    response = client.post(
        "/plans_perfomance",
        params={"date": test_date.isoformat()}
    )
    print(response.json())
    assert response.status_code == 200

def test_year_performance():
    """тестує видачу  звіту за рік"""
    response = client.post(
        "/year_performance",
        params={"year": 2021}  
    )
    assert response.status_code == 200


    
def test_cleanup():
    BaseModel.metadata.drop_all(bind=test_engine)
    if os.path.exists("files"):
        for file in os.listdir("files"):
            os.remove(os.path.join("files", file))
        os.rmdir("files")

