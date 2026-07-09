from fastapi import FastAPI

from routers.blacklist import router

app=FastAPI()

app.include_router(router)
