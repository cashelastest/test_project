from fastapi.testclient import TestClient
from main import app
from models.base import BaseModel
from models.credit import CreditsModel
from models.dictionary import DictionaryModel
from models.payment import PaymentModel
from models.plan import PlansModel
from models.user import UsersModel
from db.db_connector import test_engine,test_session
from datetime import datetime,date
from utils.utils import get_from_csv,parse_date, handle_nan
import os
from pathlib import Path
import logging
import time

logger = logging.getLogger(__name__)

client = TestClient(app)

BaseModel.metadata.create_all(test_engine)
response = client.get("/users_credits/99999/")

BASE_DIR = Path(__file__).resolve().parent.parent

SRC_PATH = BASE_DIR / "utils" / "src"


def insert_dictionary():
    """переносить Dictionary зі csv до бд"""
    dictionaries = get_from_csv(SRC_PATH / "dictionary.csv")
    dictionary_objects = [DictionaryModel(name = dictionaries.loc[id, "name"]) for id in dictionaries.index]

    test_session.add_all(dictionary_objects)
    test_session.commit()

def insert_payments():
    """переносить платежі з csv до бази данних"""
    payments = get_from_csv(SRC_PATH / "payments.csv")

    payments_objects = [PaymentModel(
            sum=  float(payments.loc[id, "sum"]),
            payment_date = parse_date(payments.loc[id, "payment_date"]),
            credit_id = int(payments.loc[id, "credit_id"]),
            type_id = int(payments.loc[id, "type_id"])
        ) for id in payments.index]
    test_session.add_all(payments_objects)
    test_session.commit()


def insert_users():
    """переносить юзерів з csv до бази даних"""
    users = get_from_csv(SRC_PATH /  "users.csv")
    users_objects =[ UsersModel(
            login = users.loc[id, "login"],
            registration_date = datetime.strptime(users.loc[id, "registration_date"], "%d.%m.%Y")) for id in users.index]
    test_session.add_all(users_objects)
    test_session.commit()


def insert_credits():
    """переносить усі кредити з csv до бази даних"""
    credits = get_from_csv(SRC_PATH / "credits.csv")
    for id in credits.index:
        actual_return_date = credits.loc[id, "actual_return_date"]
        credits_object=CreditsModel(
            user_id = int(credits.loc[id, "user_id"]),
            issuance_date=parse_date(credits.loc[id, "issuance_date"]),
            return_date=parse_date(credits.loc[id, "return_date"]),
            actual_return_date=handle_nan(actual_return_date),
            body = int(credits.loc[id, "body"]),
            percent = float(credits.loc[id, "percent"]))
    
        test_session.add(credits_object)
        test_session.commit()


def insert_plans():
    """Переносить усі плани з csv до бази даних"""
    plans = get_from_csv(SRC_PATH / "plans.csv")

    plan_objects = [PlansModel(
        period = parse_date(plans.loc[id, "period"]),
        sum = float(plans.loc[id, "sum"]),
        category_id = int(plans.loc[id, "category_id"])) for id in plans.index]
    test_session.add_all(plan_objects)
    test_session.commit()


def test_prepare_data():
    """Переносить дані з csv файлів до бази даних"""


    insert_users()
    insert_dictionary()
    insert_credits()
    insert_payments()
    insert_plans()
    print(response.json())

    assert True


def test_user_credits_not_found():
    """Тест перевіряє кредити неіснуючого користувача"""
    response = client.get("/user_credits/99999/")
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {'detail': 'Кредитів для цього юзера не знайдено'}

def test_user_credits_valid():
    """перевіряє кредити існуючого користувача"""
    response = client.get("/user_credits/12/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_plans_insert_invalid_file():
    """перевіряє при завантаженні неправильного файла"""
    files = {"file": ("files/test.txt", "invalid content", "text/plain")}
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
        params={'year':2021}
    )
    print(response.json())
    assert response.status_code == 200

    
def test_cleanup():
    BaseModel.metadata.drop_all(bind=test_engine)

