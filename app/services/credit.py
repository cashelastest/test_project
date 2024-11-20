from sqlalchemy import select
from models.credit import CreditsModel
from db.db_connector import session
from services.payment import get_payments_by_credit,get_body_percent_payments
import datetime



def get_credit_info(credit):
    """Повертає інформацію про кредит"""
    info= {}
    if credit.actual_return_date:

        info['Дата повернення кредиту'] = credit.actual_return_date
        info["Сума видачі"] = credit.body
        info["Нараховані відсотки"] = credit.percent
        payments = get_payments_by_credit(credit.id)

        payments = sum([payment.sum for payment in payments])
        

        info["Сума платежів за кредитом"] = payments
        
    else:
        info["Крайня дата повернення кредиту"] = credit.return_date
        today = datetime.date.today()
        print(credit.return_date)
        delta = today - credit.return_date
        info['Кількість днів прострочення кредиту'] = delta.days
        info["Сума видачі"] = credit.body
        info["Нараховані відсотки"] = credit.percent

        body_payments, percent_payments = get_body_percent_payments(credit.id)
        info["Сума платежів по тілу"] = round(body_payments,3)
        info["Сума платежів по відсоткам"] = percent_payments
    return info
def get_credits(user_id):
    """Отримання кредитів по Id користувача"""
    sel = select(CreditsModel).where(CreditsModel.user_id==user_id)
    return session.execute(sel).scalars().all()