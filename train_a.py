
import sqlalchemy as db
from sqlalchemy import Column, Integer,String,Date,Float, ForeignKey,insert,select
import csv
from sqlalchemy.orm import as_declarative
from datetime import datetime
engine = db.create_engine("mysql://root:Sobaka1@localhost:3306/credit_test_db")
metadata = db.MetaData()
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
    



def insert_users(data):
    for user in data:
        parsed_date = datetime.strptime(user[2], "%d.%m.%Y")
        insert_query = insert(UsersModel).values(
            login = user[1],
            registration_date = parsed_date

        )
        with engine.begin() as conn:
            conn.execute(insert_query)
    return "200"
def parse_date(date_str):
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str.strip(), '%d.%m.%Y')
    except ValueError as e:
        print(f"Date parsing error: {e} for value: {date_str}")
        return None
def insert_credits(data):
    for credit in data:

        insert_query = insert(CreditsModel).values(
        user_id = int(credit[1]),
        issuance_date=parse_date(credit[2]),
        return_date=parse_date(credit[3]),
        actual_return_date=parse_date(credit[4]),
        body = int(credit[5]),
        percent = float(credit[6])
            )
        with engine.begin() as conn:
            
                conn.execute(insert_query)

    return "200"


def get_credits(user_id):
    
    sel = select(CreditsModel).where(CreditsModel.user_id==user_id)
    with engine.begin() as conn:
        data = conn.execute(sel)
        data = data.fetchall()

    return data

# csv_users = get_from_csv("users.csv")
# csv_credits = get_from_csv("credits.csv")
# # print(insert_users(csv_users))
# print(insert_credits(csv_credits))