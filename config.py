from pydantic import BaseSettings, AnyUrl
from typing import Optional
import os

class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    OWNER_TELEGRAM_ID: Optional[int] = None

    # App / Domain
    DOMAIN: str = "http://localhost:8000"
    WEBHOOK_VERIFY_TOKEN: str = "verify123"

    # Instagram / Meta
    INSTAGRAM_CLIENT_ID: Optional[str] = None
    INSTAGRAM_CLIENT_SECRET: Optional[str] = None
    INSTAGRAM_REDIRECT_URI: Optional[str] = None
    FB_PAGE_LONG_LIVED_TOKEN: Optional[str] = None

    # WhatsApp Cloud
    WHATSAPP_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_BUSINESS_ACCOUNT_ID: Optional[str] = None

    # Twitter/X
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_BEARER: Optional[str] = None

    # Database
    DATABASE_URL: AnyUrl = "sqlite:///./socialpipe.db"

    # Runtime
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
