from sqlalchemy import Integer
from sqlalchemy.orm import as_declarative
from db.db_connector import db


@as_declarative()
class BaseModel:
    id = db.Column("id",Integer,autoincrement=True, primary_key=True)


