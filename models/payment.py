from sqlalchemy import Column, ForeignKey, Float, Date
from models.base import BaseModel

class PaymentModel(BaseModel):
    __tablename__ = "payments"


    credit_id = Column(ForeignKey('credits.id'))
    payment_date = Column(Date)
    sum = Column(Float)
    type_id = Column(ForeignKey('dictionary.id'))
