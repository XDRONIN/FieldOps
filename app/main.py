from fastapi import FastAPI
from app.api.v1 import api
from app.core import config
from app.db.session import engine
from app.db.base_class import Base
# This is to create the tables in the database
# In a real application, you would use Alembic for migrations
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=config.settings.PROJECT_NAME, openapi_url=f"{config.settings.API_V1_STR}/openapi.json"
)

app.include_router(api.api_router, prefix=config.settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to FieldOps API"}
