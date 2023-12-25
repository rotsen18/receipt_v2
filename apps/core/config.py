import secrets
from typing import List, Optional

from pydantic import AnyHttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 8 hours = 8 hours
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '['http://localhost', 'http://localhost:4200', 'http://localhost:3000', \
    # 'http://localhost:8080', 'http://local.dockertoolbox.tiangolo.com']'

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | str] = []
    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = '/app/app/email-templates/build'
    EMAILS_ENABLED: bool = False

    USERS_OPEN_REGISTRATION: bool = False
    ALGORITHM: str = 'HS256'
    SWAGGER_URL: str = '/api/docs'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
