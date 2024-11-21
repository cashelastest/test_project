import os
from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy.orm import Session
load_dotenv()


DB_CONFIG = {
    'username': os.getenv('DB_USERNAME',"root"),
    'password': os.getenv('DB_PASSWORD', "Sobaka1"),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '3306'),
    'database': os.getenv('DB_NAME', 'credit_test_db')
}

TEST_DB_CONFIG = {
    'username': os.getenv('TEST_DB_USERNAME'),
    'password': os.getenv('TEST_DB_PASSWORD'),
    'host': os.getenv('TEST_DB_HOST', 'localhost'),
    'port': os.getenv('TEST_DB_PORT', '3306'),
    'database': os.getenv('TEST_DB_NAME')
}

def get_db_url(test):
    """
    Отримує посилання для підключення
    Args:
            test: тип бази даних (test або default)
    """

    config = TEST_DB_CONFIG if test else DB_CONFIG

    return f"mysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"



engine = db.create_engine(get_db_url(False))
session = Session(engine)
test_engine = db.create_engine(get_db_url(True))
test_session = Session(test_engine)


metadata = db.MetaData()

