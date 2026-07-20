from fastapi import FastAPI
from routers.blacklist import router
from routers import screening
from routers import customer_insight

app = FastAPI()

app.include_router(router)
app.include_router(screening.router)
app.include_router(customer_insight.router)
