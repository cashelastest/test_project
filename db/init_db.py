from models.credit import CreditsModel
from models.dictionary import DictionaryModel
from models.user import UsersModel
from models.payment import PaymentModel
from models.plan import PlansModel
import pandas as pd
from datetime import datetime
from models.base import BaseModel
from sqlalchemy import insert
from db.db_connector import engine, session
from utils.utils import parse_date, get_from_csv, handle_nan

SRC_PATH  = "utils/src/"


def insert_dictionary():
    """переносить Dictionary зі csv до бд"""
    dictionaries = get_from_csv(SRC_PATH+"dictionary.csv")
    dictionary_objects = [DictionaryModel(name = dictionaries.loc[id, "name"]) for id in dictionaries.index]

    session.add_all(dictionary_objects)
    session.commit()

def insert_payments():
    """переносить платежі з csv до бази данних"""
    payments = get_from_csv(SRC_PATH + "payments.csv")

    payments_objects = [PaymentModel(
            sum=  float(payments.loc[id, "sum"]),
            payment_date = parse_date(payments.loc[id, "payment_date"]),
            credit_id = int(payments.loc[id, "credit_id"]),
            type_id = int(payments.loc[id, "type_id"])
        ) for id in payments.index]
    session.add_all(payments_objects)
    session.commit()


def insert_users():
    """переносить юзерів з csv до бази даних"""
    users = get_from_csv(SRC_PATH+ "users.csv")
    users_objects =[ UsersModel(
            login = users.loc[id, "login"],
            registration_date = datetime.strptime(users.loc[id, "registration_date"], "%d.%m.%Y")) for id in users.index]
    session.add_all(users_objects)
    session.commit()



def insert_credits():
    """переносить усі кредити з csv до бази даних"""
    credits = get_from_csv(SRC_PATH + "credits.csv")
    for id in credits.index:
        actual_return_date = credits.loc[id, "actual_return_date"]
        credits_object=CreditsModel(
            user_id = int(credits.loc[id, "user_id"]),
            issuance_date=parse_date(credits.loc[id, "issuance_date"]),
            return_date=parse_date(credits.loc[id, "return_date"]),
            actual_return_date=handle_nan(actual_return_date),
            body = int(credits.loc[id, "body"]),
            percent = float(credits.loc[id, "percent"]))
    
        session.add(credits_object)
        session.commit()


def insert_plans():
    """Переносить усі плани з csv до бази даних"""
    plans = get_from_csv(SRC_PATH + "plans.csv")

    plan_objects = [PlansModel(
        period = parse_date(plans.loc[id, "period"]),
        sum = float(plans.loc[id, "sum"]),
        category_id = int(plans.loc[id, "category_id"])) for id in plans.index]
    session.add_all(plan_objects)
    session.commit()





def init_db():
    BaseModel.metadata.create_all(bind=engine)

    
