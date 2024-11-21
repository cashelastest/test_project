from fastapi import HTTPException, APIRouter
from services.credit import get_credits
from services.credit import get_credit_info


user_router = APIRouter(prefix="/user_credits")


@user_router.get("/{user_id}/")
def user_credits(user_id:int)->dict:
    """
    Повертає звіт по кредитам користувача

    Args: 
            user_id: id користувача, кредити якого хочемо отримати
    """
    credits = get_credits(user_id = user_id)
    if not credits:
        raise HTTPException(status_code=404, detail= "Кредитів для цього юзера не знайдено")
    response = {}
    for credit in credits:
        is_closed = credit.actual_return_date is not None
        answer = [credit.issuance_date, is_closed]

        info = get_credit_info(credit)
        answer.append(info)
        response[credit.id] = answer

    return response 
