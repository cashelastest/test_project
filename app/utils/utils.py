from datetime import datetime
import csv

def get_from_csv(filename):
    with open (f"utils/src/{filename}", "r",encoding="utf-8") as file:
        data = csv.reader(file, delimiter="\t")
        data_csv = []
        next(data)
        for row in data:

            data_csv.append(row)
        return data_csv
    




def parse_date(date_str):
    """Парсить дату та перевіяє на валідність"""
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str.strip(), '%d.%m.%Y')
    except Exception as e:
        print(f"Помилка парсингу дати: {e} для значення: {date_str}")
        return None
