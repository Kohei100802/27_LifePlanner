from pydantic_settings import BaseSettings
from pydantic import AnyUrl, EmailStr


class Settings(BaseSettings):
    app_name: str = "LifePlanWebApp"
    secret_key: str = "change-me"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 7027
    database_url: str = "sqlite:///./data/app.db"
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    mail_from: EmailStr | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()  # type: ignore
