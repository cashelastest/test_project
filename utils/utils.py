from datetime import datetime
import pandas as pd


def get_from_csv(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def handle_nan(value):
    if (value == 'nan' or 
        pd.isna(value) or 
        value is None or 
        (isinstance(value, float) and np.isnan(value))):
        return None
    return value


def parse_date(date_str):
    """Парсить дату та перевіяє на валідність"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), '%d.%m.%Y')
    except Exception as e:
        print(f"Помилка парсингу дати: {e} для значення: {date_str}")
        return None
    

def filter_by_month(items, month_attr, month):
    return [item for item in items if getattr(item, month_attr).month == month]


def safe_percent_counting(part, whole):
    return round(100*part/whole, 2) if whole != 0 else 0