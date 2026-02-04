from fastapi import FastAPI
from fast_api.routes import router

app = FastAPI()


app.include_router(router, prefix="/api")
