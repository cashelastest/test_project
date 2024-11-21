from sqlalchemy import Date,Column, Float, ForeignKey
from models.base import BaseModel

class PlansModel(BaseModel):
    __tablename__ = "plans"

    period = Column(Date)
    sum = Column(Float)
    category_id = Column(ForeignKey('dictionary.id'))