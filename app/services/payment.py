from sqlalchemy import select
from models.payment import PaymentModel
from db.db_connector import session, engine

def get_payments_by_credit(credit_id):
    """Повертає усі платежі по цьому кредиту"""
    try:
        select_query = select(PaymentModel).where(PaymentModel.credit_id == credit_id)
        return session.execute(select_query).scalars().all()
    except Exception as e:
        print(f"Помилка при отриманні платежів по id кредиту({credit_id}): {e}") 
        return []


def get_body_percent_payments(credit_id):
    """Повертає суму платежів по тілу та по відсоткам"""
    select_body_query = select(PaymentModel).where(
        PaymentModel.credit_id == credit_id,
        PaymentModel.type_id == 1
    )
    select_percent_query = select(PaymentModel).where(
        
        PaymentModel.type_id == 2
    )
    
    try:
        with engine.begin() as conn:
            body_data = conn.execute(select_body_query)
            percent_data = conn.execute(select_percent_query)
            body_sum = sum(payment.sum for payment in body_data)
            percent_sum = sum(payment.sum for payment in percent_data)

    
    except Exception as e:
        print(f"Помилка при сумуванні платежів: {e}\n id кредиту:{credit_id}")
        return 0.0, 0.0
    return (session.query(PaymentModel)
            .filter(PaymentModel.credit_id == credit_id)
            .all()
    )