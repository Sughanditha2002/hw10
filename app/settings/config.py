# app/settings/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "postgresql://user:password@localhost/dbname"
    debug: bool = True
    max_login_attempts: int = 5

settings = Settings()