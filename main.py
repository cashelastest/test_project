from fastapi import FastAPI
from db.init_db import init_db
from routes.users import user_router
from routes.plans import plans_router
from routes.year_perfomance import year_router
app = FastAPI()

def startup_event():
    init_db()

app.add_event_handler("startup", startup_event)
app.include_router(plans_router)

app.include_router(user_router)

app.include_router(year_router)
