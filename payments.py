from train_a import *

def insert_payments():
    data = get_from_csv("payments.csv")
    for payment in data:
        print(payment) #['1', '2', '14.01.2020', '2', '1837.50']
        insert_query = insert(PaymentModel).values(
            sum=  float(payment[4]),
            payment_date = parse_date(payment[2]),
            credit_id = int(payment[1]),
            type_id = int(payment[3])
        )
        with engine.begin() as conn:
            conn.execute(insert_query)

def insert_dictionary():
    data = get_from_csv("dictionary.csv")
    for dictionary in data:
        insert_query = insert(DictionaryModel).values(
            name= dictionary[1]

        )
        with engine.begin() as conn:
            conn.execute(insert_query)
def get_payments_by_credit(credit_id):
    select_query = select(PaymentModel).where(PaymentModel.credit_id == credit_id)
    with engine.begin() as conn:
        data = conn.execute(select_query)
        return data.fetchall()

def get_body_percent_payments(credit_id):
    select_body_query = select(PaymentModel).where(PaymentModel.credit_id == credit_id, PaymentModel.type_id == 1)
    select_percent_query = select(PaymentModel).where(PaymentModel.credit_id == id, PaymentModel.type_id ==2)
    with engine.begin() as conn:
        body_data = conn.execute(select_body_query)
        percent_data = conn.execute(select_percent_query)
        body_sum = sum(payment.sum for payment in body_data)
        percent_sum = sum(payment.sum for payment in percent_data)
        
    return body_sum,percent_sum