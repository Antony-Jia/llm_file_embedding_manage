from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "File Embedding Platform"
    database_url: str = "sqlite:///./app.db"
    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
