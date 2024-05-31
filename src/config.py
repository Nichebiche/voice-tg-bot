from pydantic import BaseSettings

class Settings(BaseSettings):
    telegram_token: str
    openai_api_key: str

    class Config:
        env_file = '.env'

settings = Settings()
