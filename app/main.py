from fastapi import FastAPI
from db.init_db import init_db
from routes.users import user_router
from routes.plans import plans_router
from routes.year_perfomance import year_router
app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()
app.include_router(plans_router)

app.include_router(user_router)

app.include_router(year_router)
# app.include_router(routes.plans_perfomance)
# app.include_router(routes.year_perfomance)
# @app.get("/user_credits/{user_id}/")
# def a(user_id):
#     return user_credits(user_id)



# @app.post("/plans_insert")
# def b(file:UploadFile):
#     return create_upload_file(file)

# @app.post("/plans_perfomance")
# def c (date:date):
#     return plan_perfomance(date)

# @app.post("/year_performance")
# def d(year:int):
#     return year_perfomance(year)