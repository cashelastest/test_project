from models.payment import PaymentModel
from db.db_connector import session


def get_payments_by_credit(credit_id):
    """Повертає усі платежі по цьому кредиту"""
    try:
        return session.query(PaymentModel).filter(PaymentModel.credit_id == credit_id)
    except Exception as e:
        print(f"Помилка при отриманні платежів по id кредиту({credit_id}): {e}") 
        return []


def get_body_percent_payments(credit_id):
    """Повертає суму платежів по тілу та по відсоткам"""
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
    


def get_payments_for_period(start,end):
    """Повертає усі платежі за період"""
    return(session.query(PaymentModel)
            .filter(PaymentModel.payment_date.between(start,end))
            )
    
