from fastapi import FastAPI
from app.api.v1 import api
from app.core import config
from app.db.session import engine
from app.db.base_class import Base

def create_tables():
    Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("ENV") != "test":
        create_tables()
    yield
app = FastAPI(
    title=config.settings.PROJECT_NAME, 
    openapi_url=f"{config.settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.include_router(api.api_router, prefix=config.settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to FieldOps API"}
