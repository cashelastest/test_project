from models.payment import PaymentModel
from db.db_connector import session
from datetime import date

def get_payments_by_credit(credit_id:int):
    """
    Отримує та повертає усі платежі по цьому кредиту
    Args:
            credit_id: id кредиту користувача
    """
    try:
        return session.query(PaymentModel).filter(PaymentModel.credit_id == credit_id)
    except Exception as e:
        print(f"Помилка при отриманні платежів по id кредиту({credit_id}): {e}") 
        return []


def get_body_percent_payments(credit_id:int):
    """
    Повертає суму платежів по тілу та по відсоткам
    Args:
            credit_id: id кредиту
    """
    try:
        payments = (session.query(PaymentModel)
            .filter(PaymentModel.credit_id == credit_id)
            .all())
        body_sum = sum(payment.sum for payment in payments if payment.type_id == 1)
        percent_sum = sum(payment.sum for payment in payments if payment.type_id ==2)
        return body_sum,percent_sum    
    except Exception as e:
        print(f"Помилка при сумуванні платежів: {e}\n id кредиту:{credit_id}")
        return 0.0, 0.0
    


def get_payments_for_period(start:date,end:date):
    """
    Повертає усі платежі за період
    Args:
            start: перша дата платежу
            finish: поточна(кінцева) дата
    """
    return(session.query(PaymentModel)
            .filter(PaymentModel.payment_date.between(start,end))
            )
    
