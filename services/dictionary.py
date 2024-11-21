from models.dictionary import DictionaryModel
from db.db_connector import session

def get_category(attr, value):
    """attr -> атрибути до моделі Dictionary (id, name)
        value -> значення за яким витягуємо дані
        
    """
    object = getattr(DictionaryModel, attr)
    return session.query(object).filter(object == value).first()