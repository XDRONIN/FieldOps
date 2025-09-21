import os
from functools import lru_cache

class Settings:
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fieldops"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "yourpassword"

    TEST_DATABASE_URL: str = "sqlite:///./test.db"

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV == "test":
            return self.TEST_DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # JWT
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # File Uploads
    UPLOAD_DIR: str = "./uploads"

    # Environment
    ENV: str = "development"

    # Project
    PROJECT_NAME: str = "FieldOps"
    API_V1_STR: str = "/api/v1"

class TestSettings(Settings):
    ENV: str = "test"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"
    UPLOAD_DIR: str = "./uploads_test"


@lru_cache()
def get_settings():
    if os.environ.get("ENV") == "test":
        return TestSettings()
    return Settings()

settings = get_settings()
