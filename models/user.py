from models.base import BaseModel
from sqlalchemy import Column, String, Date

class UsersModel(BaseModel):
    __tablename__ = "users"
    login = Column(String(50))
    registration_date = Column(Date)