from sqlalchemy import Column, ForeignKey, Date, Integer, Float
from models.base import BaseModel


class CreditsModel(BaseModel):
    __tablename__ = "credits"


    user_id = Column(ForeignKey('users.id'))
    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date)
    body = Column(Integer)
    percent = Column(Float)