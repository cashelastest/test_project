from datetime import datetime
import pandas as pd
import numpy as np

def get_from_csv(filename:str):
    """
    Читає csv файл та повертаэ DataFrame
    Args:
            filename:ім'я csv файла
    """
    data = pd.read_csv(filename, sep="\t")
    return data


def handle_nan(value):
    """
    Перевіряє, чи не дорівнює значення nan
    """
    if (value == 'nan' or 
        pd.isna(value) or 
        value is None or 
        (isinstance(value, float) and np.isnan(value))):
        return None
    return value


def parse_date(date_str:str):
    """
    Парсить дату та перевіяє на валідність
    Args: 
            date_str: дату,котру парсимо
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), '%d.%m.%Y')
    except Exception as e:
        print(f"Помилка парсингу дати: {e} для значення: {date_str}")
        return None
    

def filter_by_month(items:object, attr:str, month:int):
    """
    Фільтрує за вказаним місяцем
    Args:
            items: список з моделей
            attr: атрибут,який будем додавати
            month: обраний місяць
    """
    return [item for item in items if getattr(item, attr).month == month]


def safe_percent_counting(part, whole):
    return round(100*part/whole, 2) if whole != 0 else 0