from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Validador de CPF"
    app_version: str = "1.0.0"

settings = Settings()
