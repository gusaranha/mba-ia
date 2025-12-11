from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Calculadora de Frete"
    app_version: str = "1.0.0"

settings = Settings()
