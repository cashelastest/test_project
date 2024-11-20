from models.credit import CreditsModel
from models.dictionary import DictionaryModel
from models.user import UsersModel
from models.payment import PaymentModel
from models.plan import PlansModel

from datetime import datetime
from models.base import BaseModel
from sqlalchemy import insert
from db.db_connector import engine, session
from utils.utils import parse_date, get_from_csv


def insert_dictionary():
    """переносить Dictionary зі csv до бд"""
    data = get_from_csv("dictionary.csv")
    for dictionary in data:
        insert_query = insert(DictionaryModel).values(
            name= dictionary[1]

        )
        session.execute(insert_query)
        session.commit()

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
        session.execute(insert_query)
        session.commit()


def insert_users():
    """переносить юзерів з csv до бази даних"""
    data = get_from_csv("users.csv")
    for user in data:
        parsed_date = datetime.strptime(user[2], "%d.%m.%Y")

        insert_query = insert(UsersModel).values(
            login = user[1],
            registration_date = parsed_date)
        
        session.execute(insert_query)
        session.commit()


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

        session.execute(insert_query)
        session.commit()


def insert_plans():
    """Переносить усі плани з csv до бази даних"""
    data = get_from_csv("plans.csv")
    for plan in data:
        insert_query = insert(PlansModel).values(
            period = parse_date(plan[1]),
            sum = float(plan[2]),
            category_id = int(plan[3]))
        session.execute(insert_query)
        session.commit()



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

        session.execute(insert_query)
        session.commit()

def init_db():

    BaseModel.metadata.create_all(bind=engine)