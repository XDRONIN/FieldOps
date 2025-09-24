import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    TEST_DATABASE_URL: str = "sqlite:///./test.db"

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV == "test":
            return self.TEST_DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # File Uploads
    UPLOAD_DIR: str = "./uploads"

    # Environment
    ENV: str = "development"

    # Project
    PROJECT_NAME: str = "FieldOps"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"


class TestSettings(Settings):
    ENV: str = "test"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"
    UPLOAD_DIR: str = "./uploads_test"


@lru_cache()
def get_settings():
    if os.environ.get("ENV") == "test":
        return TestSettings()
    return Settings()


# Create a settings instance that can be imported
settings = get_settings()

