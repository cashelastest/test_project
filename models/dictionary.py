from sqlalchemy import Column, String
from models.base import BaseModel

class DictionaryModel(BaseModel):
    __tablename__ ='dictionary'
    name = Column(String(50))