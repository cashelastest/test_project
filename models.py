
import sqlalchemy as db
from sqlalchemy import Column, Integer,String,Date,Float, ForeignKey,select
import csv
from sqlalchemy.orm import as_declarative
from datetime import datetime
from db_connector import engine,session

@as_declarative()
class BaseModel:
    id = db.Column("id",Integer,autoincrement=True, primary_key=True)

class UsersModel(BaseModel):
    __tablename__ = "users"
    login = Column(String(50))
    registration_date = Column(Date)

class CreditsModel(BaseModel):
    __tablename__ = "credits"


    user_id = Column(ForeignKey('users.id'))
    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date)
    body = Column(Integer)
    percent = Column(Float)
class DictionaryModel(BaseModel):
    __tablename__ ='dictionary'
    name = Column(String(50))
    
class PaymentModel(BaseModel):
    __tablename__ = "payments"


    credit_id = Column(ForeignKey('credits.id'))
    payment_date = Column(Date)
    sum = Column(Float)
    type_id = Column(ForeignKey('dictionary.id'))

class PlansModel(BaseModel):
    __tablename__ = "plans"

    period = Column(Date)
    sum = Column(Float)
    category_id = Column(ForeignKey('dictionary.id'))


BaseModel.metadata.create_all(engine)


def get_from_csv(filename):
    with open (f"src/{filename}", "r",encoding="utf-8") as file:
        data = csv.reader(file, delimiter="\t")
        data_csv = []
        next(data)
        for row in data:

            data_csv.append(row)
        return data_csv
    




def parse_date(date_str):
    """Парсить дату та перевіяє на валідність"""
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str.strip(), '%d.%m.%Y')
    except Exception as e:
        print(f"Помилка парсингу дати: {e} для значення: {date_str}")
        return None



def get_credits(user_id):
    """Отримання кредитів по Id користувача"""
    sel = select(CreditsModel).where(CreditsModel.user_id==user_id)
    return session.execute(sel).scalars().all()

