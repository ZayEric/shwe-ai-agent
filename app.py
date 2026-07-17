from fastapi import FastAPI
from routers.blacklist import router
from routers import screening

app=FastAPI()

app.include_router(router)
app.include_router(screening.router)
