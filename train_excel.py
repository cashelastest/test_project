import openpyxl
from plans import get_category_by_name,check_plan,insert_xl_plans
from train_a import parse_date, PlansModel

def get_get_plans_from_excel(filename):
    book = openpyxl.open(f"{filename}", read_only=True)


    sheet = book.active

    xl_plan = {}
    for row in range(1, sheet.max_row):
        category_id = get_category_by_name(sheet[row][1].value)
        print(category_id)

        xl_plan[row]={
        "period": parse_date(sheet[row][0].value),
        "category_id":category_id,
        "sum":sheet[row][2].value
        }
    return xl_plan
def check_data(plans):

    for plan in plans:
    
        if check_plan(plans[plan])==False:
            return f"Error: plan with id:{plan} exists in database"
        
        if plans[plan]["period"].day != 1:
            return f"Error: plan with id: {plan} has invalid date"
        if plans[plan]["sum"] is None:
            return "Error: Column sum is empty"
    return True


def download_plans(filename):
    plans = get_get_plans_from_excel(filename)

    data = check_data(plans)

    if data == True:
        return insert_xl_plans(plans)
    else:
        return data
    
        
